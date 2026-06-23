import os

from dotenv import load_dotenv
from openai import AzureOpenAI, OpenAI


SYSTEM_PROMPT = "你是一個企業內部助理，請用繁體中文回答，回答要簡潔、準確、可操作。"


def ask_agent(question: str) -> str:
    """Ask the Foundry / Azure OpenAI compatible chat endpoint a question."""
    load_dotenv(override=True)

    if not question or not question.strip():
        return "請輸入問題後再試一次。"

    endpoint = os.environ["AZURE_OPENAI_ENDPOINT"].rstrip("/")

    if endpoint.endswith("/openai/v1"):
        client = OpenAI(
            base_url=endpoint,
            api_key=os.environ["AZURE_OPENAI_API_KEY"],
        )
    else:
        client = AzureOpenAI(
            azure_endpoint=endpoint,
            api_key=os.environ["AZURE_OPENAI_API_KEY"],
            api_version=os.environ["AZURE_OPENAI_API_VERSION"],
        )

    response = client.chat.completions.create(
        model=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": question.strip()},
        ],
    )

    return response.choices[0].message.content or ""
