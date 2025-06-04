from fastapi import FastAPI, Request
from pydantic import BaseModel
import requests
import fitz  # PyMuPDF
import io

app = FastAPI()

class ScrapeRequest(BaseModel):
    url: str

@app.post("/scrape-site")
async def scrape_site(data: ScrapeRequest):
    try:
        response = requests.get(data.url)
        if response.status_code != 200:
            return {"error": "Failed to download PDF", "status_code": response.status_code}

        pdf_bytes = io.BytesIO(response.content)
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")

        all_text = []
        for page in doc:
            all_text.append(page.get_text())

        return {
            "document_text": "\n".join(all_text).strip(),
            "page_count": doc.page_count,
            "status": "success"
        }

    except Exception as e:
        return {"error": str(e)}
