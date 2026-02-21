import json
import re


def extract_json(text: str):

    if not text:
        raise ValueError("LLM returned empty response")

    # remove markdown blocks
    text = text.strip()

    text = re.sub(r"```json", "", text)
    text = re.sub(r"```", "", text)

    # extract first JSON object
    match = re.search(r"\{.*\}", text, re.DOTALL)

    if not match:
        raise ValueError("No JSON found in LLM response")

    json_text = match.group(0)

    return json.loads(json_text)
