import easyocr
import os
import cv2
import re

reader = easyocr.Reader(['en','th'], gpu=True, verbose=False)

def preprocess_fast(image_path):
    img = cv2.imread(image_path)
    h, w = img.shape[:2]
    img = cv2.resize(img, (w//2, h//2))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return gray

def fast_ocr(image_path):
    img = preprocess_fast(image_path)
    return reader.readtext(img, detail=0, paragraph=False)

def list_seven(image_path):
    text = fast_ocr(image_path)
    raw_text = ' '.join(text)
    date_match = re.search(r'\d{1,2}\s*\S+\.\s*\d{4}', raw_text)
    time_match = re.search(r'\d{2}:\d{2}:\d{2}', raw_text)
    date = date_match.group() if date_match else None
    time = time_match.group() if time_match else None
    list_ocr = {
        'id' : text[15],
        'Date' : date,
        'Time' : time,
        'Payment' : text[0],
        'Store' : text[1],
        'Amount' : text[2],
        'address' : text[25]
    }
    return list_ocr

def list_lotus(image_path):
    text = fast_ocr(image_path)
    raw_text = ' '.join(text)
    date_match = re.search(r'\d{1,2}\s*\S+\.\s*\d{4}', raw_text)
    time_match = re.search(r'\d{2}:\d{2}:\d{2}', raw_text)
    date = date_match.group() if date_match else None
    time = time_match.group() if time_match else None
    match = re.findall(r'\d+(?:,\d{3})*(?:\.\d{2})', raw_text)
    amount = max(match, key=lambda x: float(x.replace(',', '')))
    list_ocr = {
        'id' : text[17],
        'Date' : date,
        'Time' : time,
        'Payment' : text[0],
        'Store' : text[1],
        'Amount' : amount,
        'address' : text[28]
    }
    return list_ocr

def delect_image(image_path):
    os.remove(image_path)

def patment_ocr(image_path):
    text = fast_ocr(image_path)
    if text[0] == "โลตัส":
        return list_lotus(image_path)
    elif text[1] == "เซเว่น อีเลฟเว่น" or text[0] == "TrueMoney":
        return list_seven(image_path)
    else:
        return list_seven(image_path)