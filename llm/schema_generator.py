# import libraries
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
import json

# define the llm
llm = ChatOllama(
    model = "gpt-oss",
    temperature = 0
    )

JSON_SCHEMA_EXAMPLE = """
{
  "model_name": "RequirementSpec",
  "fields": [
    {
      "name": "",
      "type": "int | float | str | bool",
      "description": ""
    }
  ]
}
"""

prompt = PromptTemplate(
    template="""
You are an expert procurement system designer.

Convert the following technical specification into
a structured JSON schema.

Specification:
{spec}

Return ONLY valid JSON in this format:

{schema_example}
""",
    input_variables=["spec", "schema_example"]
)

chain = prompt | llm

def generate_schema(spec_text):
    response = chain.invoke({
        "spec": spec_text,
        "schema_example": JSON_SCHEMA_EXAMPLE
    })
    return json.loads(response.content)