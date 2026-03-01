import base64
from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()

client=OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)
PROMPT_TEXT="""
You are an AI image analyst.

Analyze the given image carefully and return:
1. Type of image/document
2. Important extracted information (structured)
3. A concise human-readable summary

Return output strictly in JSON format with keys:
- document_type
- extracted_data
- summary

"""
def analyze_image_with_vision(image_path: str) -> dict:
    with open(image_path, "rb") as img:
        image_base64 = base64.b64encode(img.read()).decode("utf-8")

    response = client.chat.completions.create(
        model="gpt-4o-mini",  # vision-capable
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": PROMPT_TEXT},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{image_base64}"
                        }
                    }
                ]
            }
        ]
    )

    return response.choices[0].message.content