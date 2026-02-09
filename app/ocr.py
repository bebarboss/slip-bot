import cv2
import numpy as np
import os

from scb import scb_data

LOGO_DIR = "logos"
ORB_FEATURES = 1000
MATCH_THRESHOLD = 12

orb = cv2.ORB_create(nfeatures=ORB_FEATURES)

def load_logos():
    logos = {}
    for file in os.listdir(LOGO_DIR):
        name = os.path.splitext(file)[0]
        path = os.path.join(LOGO_DIR, file)
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            continue
        kp, des = orb.detectAndCompute(img, None)
        if des is not None:
            logos[name] = {
                "image": img,
                "kp": kp,
                "des": des
            }
    return logos

LOGOS = load_logos()

def crop_logo_zone(img):
    h, w = img.shape[:2]
    return img[0:int(h * 0.13), 0:int(w * 5)]

def orb_match(img_gray, logo_des):
    kp, des = orb.detectAndCompute(img_gray, None)
    if des is None:
        return 0
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(des, logo_des)
    return len(matches)

def detect_logo(image_bytes: bytes):
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if img is None:
        return None
    header = crop_logo_zone(img)
    gray = cv2.cvtColor(header, cv2.COLOR_BGR2GRAY)
    scores = {}
    for name, logo in LOGOS.items():
        score = orb_match(gray, logo["des"])
        scores[name] = score
    best_logo = max(scores, key=scores.get)
    best_score = scores[best_logo]
    print("ORB scores:", scores)

    if best_score >= MATCH_THRESHOLD:
        return best_logo
    return None

def payment_method(image_bytes: bytes):
    logo = detect_logo(image_bytes)
    if logo in ['SCB']:
        return scb_data(image_bytes)
    
    elif logo in ['TRUEMONEY','TRUE-MONEY']:
        return 'truemoney'
    
    elif logo in ['MAKE']:
        return 'make'
    
    else:
        return 'unknown'
    
