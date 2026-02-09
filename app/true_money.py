import easyocr
import cv2
import numpy as np
import re
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

reader = easyocr.Reader(['en', 'th'], gpu=True, verbose=False)

def decode_image(image_bytes: bytes):
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("Invalid image bytes")
    return img

def split_image_dynamic(img):
    h, w, _ = img.shape
    return {
        "header": img[int(h*0.1):int(h*0.3), :],
        "body": img[int(h*0.35):int(h*0.65), :],
        "footer": img[int(h*0.5):int(h*0.9), :]
    }

def ocr_zone(img):
    results = reader.readtext(img, detail=1, paragraph=False)
    return " ".join(
        text.strip()
        for _, text, conf in results
        if conf >= 0.4
    )

def detect_date(text):
    match = re.search(r'(\d{1,2})\s([A-Za-zก-ฮ.]{2,5})\s(\d{4})', text)
    if not match:
        return None
    day, month_raw, year_raw = match.groups()
    month_map = {
        "ม.ค.":1,"ก.พ.":2,"มี.ค.":3,"เม.ย.":4,"พ.ค.":5,"มิ.ย.":6,
        "ก.ค.":7,"ส.ค.":8,"ก.ย.":9,"ต.ค.":10,"พ.ย.":11,"ธ.ค.":12,
        "jan":1,"feb":2,"mar":3,"apr":4,"may":5,"jun":6,
        "jul":7,"aug":8,"sep":9,"sept":9,"oct":10,"nov":11,"dec":12
    }
    month = month_map.get(month_raw.lower())
    if not month:
        return None
    year = int(year_raw)
    if year >= 2500:
        year -= 543
    return datetime(year, month, int(day)).strftime("%Y-%m-%d")

def detect_time(text):
    match = re.search(r'\d{2}:\d{2}:\d{2}', text)
    if not match:
        return None
    return datetime.strptime(match.group(), "%H:%M:%S").strftime("%H:%M:%S")

def detect_refid(text):
    tokens = text.split()
    for i, t in enumerate(tokens):
        if t in {"หมายเลขการสั่งซื้อ"} and i + 2 < len(tokens):
            return f"{tokens[i+1]}{tokens[i+2]}"
    return None

def detect_sender(text):
    tokens = text.split()
    for i, t in enumerate(tokens):
        if t in {"ช่องทางการชำระเงิน", "from"} and i + 3 < len(tokens):
            return f"{tokens[i+1]}{tokens[i+2]}"
    return None

def detect_receiver(text):
    tokens = text.split()
    for i, t in enumerate(tokens):
        if t in {"รายละเอียดสินค้า"} and i + 2 < len(tokens):
            return f"{tokens[i+1]} {tokens[i+2]}".upper()
    return None

def detect_amount(text):
    match = re.search(r'(\d{1,3}(?:,\d{3})*(?:\.\d{2}))', text)
    return match.group() if match else None

def true_money_data(image_bytes: bytes):
    img = decode_image(image_bytes)
    zones = split_image_dynamic(img)
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = {
            executor.submit(ocr_zone, zones[z]): z
            for z in zones
        }
        ocr = {futures[f]: f.result() for f in as_completed(futures)}
    return {
        "date": detect_date(ocr["body"]),
        "time": detect_time(ocr["body"]),
        "payment_method": "TrueMoney Wallet",
        "refid": detect_refid(ocr["footer"]),
        "sender": detect_sender(ocr["body"]),
        "receiver": detect_receiver(ocr["footer"]),
        "amount": detect_amount(ocr["header"])
    }
