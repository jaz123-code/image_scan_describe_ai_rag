from app.services.model_engines.base import VisionLLM
from app.services.image_scan import scan_image
import json

class LocalVision(VisionLLM):
     """
    Simple OCR-based fallback engine
    """
     def analyze(self, image_path: str)->dict:
          ocr=scan_image(image_path)
          return {
               "raw_response":json.dumps({
                    "document_type": "unknown",
                    "extracted_data": {
                         "raw_text": ocr["raw_text"]
                    },
                    "summary": ocr["summary"]
               }),
               "model_metadata": {
                    "provider" : "local",
                    "model": "tesseract"
               }
          }
