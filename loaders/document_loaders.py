from langchain_community.document_loaders import (
    PyPDFLoader,
    UnstructuredWordDocumentLoader
)
import pandas as pd
import os
from pypdf import PdfReader
from docx import Document


def load_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def load_docx(file):
    doc = Document(file)
    return "\n".join([p.text for p in doc.paragraphs])

def load_excel(file):
    text = ""
    excel = pd.read_excel(file, sheet_name=None)
    for sheet, df in excel.items():
        text += f"\nSheet: {sheet}\n"
        text += df.astype(str).to_string(index=False)
    return text

def extract_text(uploaded_file):
    filename = uploaded_file.name.lower()

    if filename.endswith(".pdf"):
        return load_pdf(uploaded_file)
    elif filename.endswith(".docx"):
        return load_docx(uploaded_file)
    elif filename.endswith(".xlsx"):
        return load_excel(uploaded_file)
    else:
        raise ValueError("Unsupported file type")
    
def load_document_text(filepath):
    ext = os.path.splitext(filepath)[1].lower()
    if ext == ".pdf":
        loader = PyPDFLoader(filepath)
        pages = loader.load()
        return "\n".join(p.page_content for p in pages)
    elif ext in [".docx", ".doc"]:
        loader = UnstructuredWordDocumentLoader(filepath)
        docs = loader.load()
        return "\n".join(d.page_content for d in docs)
    elif ext in [".xlsx", ".xls"]:
        df = pd.read_excel(filepath)
        return df.to_string()
    else:
        raise ValueError("Unsupported file type")
