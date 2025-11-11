import os
import tempfile
from typing import List

from PIL import Image
import pytesseract
from pdf2image import convert_from_path
import openpyxl

POPPLER_PATH = os.environ.get("POPPLER_PATH")  # optional for Windows

def ocr_image(path: str, lang: str = "eng") -> str:
    img = Image.open(path)
    text = pytesseract.image_to_string(img, lang=lang)
    return text

def ocr_pdf(path: str, lang: str = "eng") -> str:
    # Convert PDF pages to images and OCR each page
    images = convert_from_path(path, poppler_path=POPPLER_PATH) if POPPLER_PATH else convert_from_path(path)
    texts: List[str] = []
    for img in images:
        texts.append(pytesseract.image_to_string(img, lang=lang))
    return "\n\n---PAGE---\n\n".join(texts)

def extract_text_from_excel(path: str) -> str:
    wb = openpyxl.load_workbook(path, data_only=True)
    texts: List[str] = []
    for sheet in wb.worksheets:
        for row in sheet.iter_rows(values_only=True):
            for cell in row:
                if cell is None:
                    continue
                texts.append(str(cell))
    return "\n".join(texts)

def save_upload_to_temp(upload_file) -> str:
    suffix = os.path.splitext(upload_file.filename)[1] or ""
    fd, tmp_path = tempfile.mkstemp(suffix=suffix)
    with os.fdopen(fd, "wb") as f:
        f.write(upload_file.file.read())
    return tmp_path
