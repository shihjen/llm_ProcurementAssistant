import json
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from loaders.document_loaders import load_document_text
from utils.json_parser import extract_json


llm = ChatOllama(
    model="gpt-oss",
    temperature=0
)

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are a procurement data extraction engine.

You MUST return ONLY valid JSON.

DO NOT explain.
DO NOT add text.
DO NOT use markdown.
DO NOT include ```json.
Return JSON only.
"""
    ),
    (
        "human",
        """
Requirement Schema:
{requirement_schema}

Quotation:
{quotation_text}
"""
    )
])


chain = prompt | llm

def extract_quotation(filepath, requirement_schema):
    text = load_document_text(filepath)
    response = chain.invoke({
        "requirement_schema": requirement_schema,
        "quotation_text": text
    })
    return extract_json(response.content)
