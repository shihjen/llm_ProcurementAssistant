from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
import json


llm = ChatOllama(
    model = "gpt-oss", 
    temperature = 0
    )

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a procurement decision advisor."
    ),
    (
        "human",
        """
Given vendor evaluation results:

{evaluation}

Recommend the best vendor and explain why.
"""
    )
])


chain = prompt | llm

def recommend(evaluations):
    response = chain.invoke({
        "evaluation": json.dumps(evaluations, indent=2)
    })
    return response.content
