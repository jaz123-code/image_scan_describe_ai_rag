from PIL import Image
import pytesseract

def scan_image(image_path: str) -> dict:
    try:
        image = Image.open(image_path)
        image=image.convert("L")
        extracted_text = pytesseract.image_to_string(image)

        return {
            "raw_text": extracted_text,
            "summary": extracted_text[:300],
            "Length": len(extracted_text)  # simple summary for now
            }
    except Exception as e:
        return {
            "raw_text": "",
            "summary": "",
            "error": str(e)
        }
