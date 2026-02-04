import easyocr
import cv2
import re
import os

reader = easyocr.Reader(['en', 'th'], gpu=True, verbose=False)


def split_image_dynamic(image_path):
    img = cv2.imread(image_path)
    h, w, _ = img.shape
    return {
        "header": img[0:int(h*0.25), :],
        "body": img[int(h*0.25):int(h*0.7), :],
        "footer": img[int(h*0.7):h, :]
    }

def ocr_zone(img):
    results = reader.readtext(img, detail=1, paragraph=False)
    data = []
    for _, text, conf in results:
        t = text.strip()
        if len(t) > 1:
            data.append({
                "text": t,
                "conf": float(conf)
            })
    return data

def extract_payment(ocr_items):
    score = {
        "truemoney": 0.0,
        "scb": 0.0,
        "kbank": 0.0
    }
    for i in ocr_items:
        t = i["text"].lower()
        c = i["conf"]
        if any(k in t for k in ["true", "truemoney", "wallet"]):
            score["truemoney"] += c
        if any(k in t for k in ["scb", "siam commercial", "ไทยพาณิชย์"]):
            score["scb"] += c
        if any(k in t for k in ["make", "kbank", "kasikorn"]):
            score["kbank"] += c
    return max(score, key=score.get) if max(score.values()) > 0 else "unknown"

def extract_amount(ocr_items):
    candidates = []
    for i in ocr_items:
        txt = i["text"].replace(",", "")
        m = re.search(r'\b(\d+\.\d{2})\b', txt)
        if m:
            candidates.append((float(m.group(1)), i["conf"]))
    return max(candidates, key=lambda x: x[1])[0] if candidates else None

def extract_id(ocr_items):
    candidates = []
    for i in ocr_items:
        t = i["text"]
        m1 = re.search(r'\b\d{20,}\b', t)
        if m1:
            candidates.append((m1.group(), i["conf"]))
            continue
        m2 = re.search(r'\b\d{14,16}[A-Za-z]{3,6}\b', t)
        if m2:
            candidates.append((m2.group(), i["conf"]))
            continue
        m3 = re.search(r'\b[A-Z]{2,5}\d{8,}\b', t)
        if m3:
            candidates.append((m3.group(), i["conf"]))
    return max(candidates, key=lambda x: x[1])[0] if candidates else None

def extract_datetime(ocr_items):
    date, time = None, None
    date_conf, time_conf = 0, 0
    for i in ocr_items:
        t = i["text"]
        if re.search(r'\d{1,2}\s[ก-ฮ.]{2,5}\s256\d', t):
            if i["conf"] > date_conf:
                date = t
                date_conf = i["conf"]
        if re.search(r'\d{2}:\d{2}:\d{2}', t):
            if i["conf"] > time_conf:
                time = t
                time_conf = i["conf"]
    return date, time

def analyze_slip(image_path):
    zones = split_image_dynamic(image_path)
    all_ocr = []
    for img in zones.values():
        all_ocr.extend(ocr_zone(img))
    payment = extract_payment(all_ocr)
    amount = extract_amount(all_ocr)
    tx_id = extract_id(all_ocr)
    date, time = extract_datetime(all_ocr)
    return {
        "payment_method": payment,
        "ID": tx_id,
        "Amount": amount,
        "Date": date,
        "Time": time
    }
def delect_image(file_path):

    if os.path.exists(file_path):
        os.remove(file_path)