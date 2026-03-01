from app.services.model_engines.base import VisionLLM
from openai import OpenAI
from dotenv import load_dotenv
import base64
import os
import time
load_dotenv()

_api_key = os.getenv("OPENAI_API_KEY")
client = None
if _api_key:
    try:
        client = OpenAI(api_key=_api_key)
    except Exception:
        client = None

PROMPT = """
Analyze the image and return STRICT JSON with keys:
- document_type
- extracted_data
- summary
"""

class OpenAIVision(VisionLLM):

    def analyze(self, image_path: str) -> dict:
        start = time.time()

        with open(image_path, "rb") as img:
            image_base64 = base64.b64encode(img.read()).decode("utf-8")

        if client is None:
            raise RuntimeError("OpenAI client not configured: set OPENAI_API_KEY")

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": PROMPT},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{image_base64}"
                            }
                        }
                    ]
                }
            ],
            timeout=20
        )

        latency = round((time.time() - start) * 1000)

        # Model returns text → you already parse later
        return {
            "raw_response": response.choices[0].message.content,
            "model_metadata": {
                "provider": "openai",
                "model": "gpt-4o-mini",
                "latency_ms": latency
            }
        }