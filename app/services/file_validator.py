from fastapi import HTTPException
from PIL import Image

MAX_FILE_SIZE_MB = 5
ALLOWED_FORMATS = {"JPEG", "PNG", "WEBP"}

def validate_image(file):
    if file.content_type not in ["image/jpeg", "image/png", "image/webp"]:
        raise HTTPException(status_code=400, detail="Invalid image type")

    file.file.seek(0, 2)
    size_mb = file.file.tell() / (1024 * 1024)
    file.file.seek(0)

    if size_mb > MAX_FILE_SIZE_MB:
        raise HTTPException(status_code=400, detail="File too large")

    try:
        img = Image.open(file.file)
        img.verify()
        if img.format not in ALLOWED_FORMATS:
            raise HTTPException(status_code=400, detail="Unsupported image format")
    except Exception:
        raise HTTPException(status_code=400, detail="Corrupted image file")

    file.file.seek(0)


