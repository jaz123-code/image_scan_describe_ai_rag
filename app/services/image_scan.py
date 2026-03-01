from PIL import Image
import pytesseract

def scan_image(image_path: str) -> dict:
    image = Image.open(image_path)
    extracted_text = pytesseract.image_to_string(image)

    return {
        "raw_text": extracted_text,
        "summary": extracted_text[:300]  # simple summary for now
    }
