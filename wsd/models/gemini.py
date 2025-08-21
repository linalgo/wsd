"""Using Gemini to rank definitions"""
import json
import os

from google import genai
from google.genai import types

from wsd.parsers import Entry, Token

SYSTEM = """You are a Japanese dictionary ranking system.
When given several candidate definitions for a Japanese word in the context of
a sentence, you must select the best one. You must answer with the number of
the candidate and also the best sub-meaning within the candidate."""


def show(candidate: Entry):
    """Return the candidate information as a string"""
    s = ', '.join(k.keb for k in candidate.k_ele) + '\n'
    s += ', '.join(r.reb for r in candidate.r_ele) + '\n'
    for i, sense in enumerate(candidate.sense):
        s += f'{i}. ' + ', '.join(g.text for g in sense.gloss) + '\n'
    return s


def get_prompt(sentence: str, token: Token, candidates: list[Entry]):
    """Create a prompt from the sentence and candidates"""
    prompt = (
        f"Which candidate is the correct definition of {token.text} in the "
        "follwing sentence?\n"
        "\n"
        "Sentence\n"
        "---------\n"
        f"{sentence}\n"
    )
    for i, candidate in enumerate(candidates):
        prompt += (
            f"Candidate #{i}\n"
            "------------\n"
            f"{show(candidate)}\n"
        )
    return prompt


def generate(prompt, model_name):
    """Call the LLM and return a json formatted response.

    Parameters
    ---------
    prompt : str
        The user prompt
    model_name: str
        The version of Gemini to use.

    Return
    ------
    res : {'answer': int, 'meaning': int}
    """
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )

    model = model_name
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=prompt),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=genai.types.Schema(
            type=genai.types.Type.OBJECT,
            properties={
                "answer": genai.types.Schema(
                    type=genai.types.Type.INTEGER,
                ),
                "meaning": genai.types.Schema(
                    type=genai.types.Type.INTEGER,
                ),
            },
        ),
        system_instruction=[
            types.Part.from_text(text=SYSTEM),
        ],
    )

    response = client.models.generate_content(
        model=model,
        contents=contents,
        config=generate_content_config,
    )
    return json.loads(response.text)



__all__ = ['GeminiRanker']
