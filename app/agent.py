import os

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from dotenv import load_dotenv
from openai import AzureOpenAI, OpenAI


SYSTEM_PROMPT = (
    "你是一個企業內部助理，請用繁體中文回答，"
    "回答要簡潔、準確、可操作。"
)


def _get_env(name: str) -> str | None:
    value = os.getenv(name)
    if not value:
        return None

    return value.strip().strip('"').strip("'")


def _create_client():
    # 不覆蓋 Foundry Runtime 已注入的環境變數。
    load_dotenv(override=False)

    deployment_name = _get_env("AZURE_OPENAI_DEPLOYMENT_NAME")
    endpoint = _get_env("AZURE_OPENAI_ENDPOINT")
    api_key = _get_env("AZURE_OPENAI_API_KEY")

    if not deployment_name:
        raise RuntimeError(
            "Missing AZURE_OPENAI_DEPLOYMENT_NAME. "
            "Set it in .env locally or agent.yaml for Hosted Agent."
        )

    # 本機模式：使用 .env 內的 API key。
    if api_key:
        if not endpoint:
            raise RuntimeError("Missing AZURE_OPENAI_ENDPOINT.")

        endpoint = endpoint.rstrip("/")

        if endpoint.endswith("/openai/v1"):
            client = OpenAI(
                base_url=endpoint,
                api_key=api_key,
            )
        else:
            client = AzureOpenAI(
                azure_endpoint=endpoint,
                api_key=api_key,
                api_version=os.environ["AZURE_OPENAI_API_VERSION"],
            )

        print(
            f"[startup] Authentication: API key, "
            f"deployment: {deployment_name}",
            flush=True,
        )

        return client, deployment_name

    # Hosted Agent 模式：使用 Managed Identity。
    credential = DefaultAzureCredential()

    # 如果平台沒有直接注入模型 endpoint，
    # 則嘗試由 Foundry Project endpoint 取得。
    if not endpoint:
        project_endpoint = _get_env("FOUNDRY_PROJECT_ENDPOINT")

        if not project_endpoint:
            raise RuntimeError(
                "Missing AZURE_OPENAI_ENDPOINT and "
                "FOUNDRY_PROJECT_ENDPOINT."
            )

        project = AIProjectClient(
            endpoint=project_endpoint,
            credential=credential,
        )

        endpoint = str(
            project.get_openai_client().base_url
        ).rstrip("/")

    endpoint = endpoint.rstrip("/")

    scope = (
        "https://ai.azure.com/.default"
        if "services.ai.azure.com" in endpoint
        else "https://cognitiveservices.azure.com/.default"
    )

    token_provider = get_bearer_token_provider(
        credential,
        scope,
    )

    if endpoint.endswith("/openai/v1"):
        client = OpenAI(
            base_url=endpoint,
            api_key=token_provider,
        )
    else:
        client = AzureOpenAI(
            azure_endpoint=endpoint,
            azure_ad_token_provider=token_provider,
            api_version=os.environ["AZURE_OPENAI_API_VERSION"],
        )

    print(
        f"[startup] Authentication: Managed Identity, "
        f"deployment: {deployment_name}, endpoint: {endpoint}",
        flush=True,
    )

    return client, deployment_name


def ask_agent(question: str) -> str:
    """Ask the Foundry / Azure OpenAI endpoint a question."""

    if not question or not question.strip():
        return "請輸入問題後再試一次。"

    client, deployment_name = _create_client()

    response = client.chat.completions.create(
        model=deployment_name,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": question.strip(),
            },
        ],
    )

    return response.choices[0].message.content or ""
