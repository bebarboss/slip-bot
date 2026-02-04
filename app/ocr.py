import pytesseract
import os
import cv2
import re
import numpy as np

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def preprocess_fast(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(
        gray, 0, 255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    return thresh


def fast_ocr(image_path):
    img = preprocess_fast(image_path)

    config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(
        img,
        lang='tha+eng',
        config=config
    )

    return [t.strip() for t in text.split('\n') if t.strip()]

def delect_image(image_path):
    os.remove(image_path)


def payment_ocr(image_path):
    raw_text = ' '.join(fast_ocr(image_path))
    text = raw_text.lower()

    payment_keywords = {
        'scb': ['SCB', 'ไทยพาณิชย์', 'siam commercial'],
        'truemoney': [' truemoney', 'true money', 'wallet','true'],
    }

    for payment, keywords in payment_keywords.items():
        for kw in keywords:
            if kw in text:
                return payment

    return 'unknown'

def clean_text(text):
    return (text
            .lower()
            .replace('฿', '฿ ')
            .replace('b ', '฿ ')
            .replace('8 ', '฿ ')
            .replace('o', '0')
            .replace(',', '')
            )

def amount(text):
    text = clean_text(text.lower())

    patterns = [
        r'ยอดชำระทั้งหมด\s*฿?\s*([\d,]+\.\d{2})',
        r'จำนวนเงิน\s*([\d,]+\.\d{2})',
        r'amount\s*([\d,]+\.\d{2})',
        r'฿\s*([\d,]+\.\d{2})',
    ]

    for p in patterns:
        m = re.search(p, text)
        if m:
            return float(m.group(1).replace(',', ''))
    return None


def show_list(image_path):
    text_list = fast_ocr(image_path)
    raw_text = ' '.join(text_list)

    date_match = re.search(r'\d{1,2}\s*\S+\.\s*\d{4}', raw_text)
    time_match = re.search(r'\d{2}:\d{2}:\d{2}', raw_text)
    id_match = re.search(r'(?i)(?:id|เลขที่(?:ธ)?รายการ)\s*[:\-]?\s*([A-Z0-9\s]{10,})',raw_text)

    return {
        'payment_method': payment_ocr(image_path),
        'ID': id_match.group(1) if id_match else None,
        'Amount': amount(raw_text),
        'Date': date_match.group() if date_match else None,
        'Time': time_match.group() if time_match else None,
    }