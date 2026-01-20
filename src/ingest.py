import os
from typing import List, Dict
from pathlib import Path
from monitoring import timed

import pdfplumber
from docx import Document

chunk_size = 500
chunk_overlap = 100
supported_extensions = {".docx", ".pdf", ".txt"}


#pdf file processing
def load_text_from_pdf(file_path: Path) -> List[Dict]:
    documents=[]
    with pdfplumber.open(file_path) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            text = page.extract_text()
            if text and text.strip():
                documents.append(
                    {
                        "text": text.strip(),
                        "metadata": {
                            "source": file_path.name,
                            "page": page_number
                        }
                    }
                )
    return documents

#text file processing
def load_text_from_text(file_path: Path) -> List[Dict]:
    text = file_path.read_text(encoding="utf-8")
    return [
        {
            "text": text.strip(),
            "metadata": {
                "source": file_path.name,
                "page": None
            }
        }
    ]

#docx file processing
def load_text_from_docx(file_path: Path) -> List[Dict]:
    document = Document(file_path)
    paragraphs = [
        para.text.strip()
        for para in document.paragraphs
        if para.text and para.text.strip()
    ]

    full_text = "\n".join(paragraphs)

    return [
        {
            "text": full_text,
            "metadata": {
                "source": file_path.name,
                "page": None
            }
        }
    ]

#Chunk Text
def chunk_text(text:str) -> List[str]:
    chunks= []
    start= 0
    text_length= len(text)

    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start= end-chunk_overlap
    return chunks

#chunk Docs
def chunk_documents(documents: List[Dict]) -> List[Dict]:
    chunked_docs = []
    for doc in documents:
        text_chunks = chunk_text(doc["text"])
        for idx, chunk in enumerate(text_chunks):
            chunked_docs.append({
                "text": chunk,
                "metadata": {
                    **doc["metadata"],
                    "chunk_id": idx
                }
            }
            )
    return chunked_docs

#main ingestion function
@timed("Document Ingestion")
def ingest_documents(data_dir: str) -> List[Dict]:
    data_path = Path(data_dir)
    if not data_path.exists():
        raise FileNotFoundError(f"Data directory not found: {data_dir}")
    
    raw_documents=[]
    for file_path in data_path.iterdir():
        if file_path.suffix.lower() not in supported_extensions:
            continue
        suffix = file_path.suffix.lower()

        if suffix == ".pdf":
            docs = load_text_from_pdf(file_path)
        elif suffix == ".txt":
            docs = load_text_from_text(file_path)
        elif suffix == ".docx":
            docs = load_text_from_docx(file_path)
        else:
            continue
        raw_documents.extend(docs)

    chunked_documents = chunk_documents(raw_documents)
    return chunked_documents

