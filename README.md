# OCR microservice (FastAPI + Tesseract)

This microservice accepts PDF, image (PNG/JPG) and Excel files and returns extracted text using Tesseract OCR (for images/PDF) and cell text extraction (for Excel).

Important system dependencies
- Tesseract OCR must be installed on the host. On Windows install from: https://github.com/tesseract-ocr/tesseract
- Poppler (pdftoppm) is required for converting PDF pages to images. Windows builds are at: https://github.com/oschwartz10612/poppler-windows

Python deps are in `requirements.txt`.

Environment
- Set `DATABASE_URL` environment variable to your Postgres connection string. By default the app uses the value you provided (but it's recommended to set via env):

DATABASE_URL=postgres://JQTfOoXUrCuzJwAtONMazjNZlgqgUKnz@switchyard.proxy.rlwy.net:38303/railway

Run locally (after installing system dependencies and creating a virtualenv)

1) Install python deps:

```powershell
python -m pip install -r requirements.txt
```

2) Start the app:

```powershell
$env:DATABASE_URL = "postgres://JQTfOoXUrCuzJwAtONMazjNZlgqgUKnz@switchyard.proxy.rlwy.net:38303/railway"
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

API
- POST /upload - multipart/form-data, field name `file`. Returns JSON with extracted text, filename and id.
- GET /health - simple health check.

Docker
The included `Dockerfile` installs Tesseract and Poppler. Build and run the container if you prefer.

Notes
- Tesseract language packs: by default English is used. If you need other languages, install the corresponding tessdata and pass the `lang` parameter.
- PDF conversion uses `pdf2image` which calls `pdftoppm` from Poppler; on Windows set the `POPPLER_PATH` env var to Poppler's bin folder if necessary.
