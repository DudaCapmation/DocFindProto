import os
from dotenv import load_dotenv
from mistralai import Mistral

load_dotenv()

api_key = os.getenv("MISTRAL_API_KEY")
client = Mistral(api_key=api_key)

def extract_text_from_document_url(document_url: str) -> str:
    try:
        response = client.ocr.process(
            model="mistral-ocr-latest",
            document={
                "type": "document_url",
                "document_url": document_url
            },
            include_image_base64=False
        )

        all_markdown = "\n\n".join(page.markdown for page in response.pages)

        print(f"Extracted {len(response.pages)} pages from Mistral OCR.")

        return  all_markdown

    except Exception as e:
        print(f"OCR failed: {e}")
        return ""
