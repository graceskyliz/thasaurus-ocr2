import os
import shutil
from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

from .db import get_db, engine
from .models import Base, Document
from .ocr import ocr_image, ocr_pdf, extract_text_from_excel, save_upload_to_temp

app = FastAPI(title="OCR Microservice")


@app.on_event("startup")
def startup_event():
    # create tables
    Base.metadata.create_all(bind=engine)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/upload")
def upload_file(file: UploadFile = File(...), db=Depends(get_db)):
    # Save upload to temp
    tmp_path = save_upload_to_temp(file)
    try:
        ext = os.path.splitext(file.filename)[1].lower()
        if ext in [".png", ".jpg", ".jpeg", ".tiff", ".bmp"]:
            extracted = ocr_image(tmp_path)
            ctype = "image"
        elif ext in [".pdf"]:
            extracted = ocr_pdf(tmp_path)
            ctype = "pdf"
        elif ext in [".xls", ".xlsx"]:
            extracted = extract_text_from_excel(tmp_path)
            ctype = "excel"
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type")

        doc = Document(filename=file.filename, content_type=ctype, extracted_text=extracted)
        db.add(doc)
        db.commit()
        db.refresh(doc)

        return JSONResponse(status_code=200, content={"id": doc.id, "filename": doc.filename, "extracted_text": doc.extracted_text})
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        try:
            os.remove(tmp_path)
        except Exception:
            pass
