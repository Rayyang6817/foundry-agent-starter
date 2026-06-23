# foundry-agent-starter

這是一個最小可執行的 Python Agent starter project，用來示範「我已經有一個可以呼叫 Foundry / Azure OpenAI endpoint 的 Agent」。

這個專案刻意保持很小：

- 這不是 Hosted Agent 專案
- 這不是 API server
- 這不是 Docker / deployment 範例
- 它只示範一個最小 Agent 如何呼叫 Foundry / Azure OpenAI endpoint
- 後續課程會再把 `ask_agent(question: str)` 包成 Foundry Hosted Agent

## 專案結構

```text
foundry-agent-starter/
  app/
    __init__.py
    agent.py
    cli.py
  .env.example
  .gitignore
  requirements.txt
  README.md
```

## 建立虛擬環境

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS / Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

## 安裝套件

```bash
pip install -r requirements.txt
```

## 設定環境變數

複製 `.env.example` 成 `.env`：

```bash
cp .env.example .env
```

Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

接著在 `.env` 填入你的 Foundry / Azure OpenAI endpoint 設定：

```env
AZURE_OPENAI_ENDPOINT=https://<your-resource-or-foundry-endpoint>/openai/v1
AZURE_OPENAI_API_KEY=<your-api-key>
AZURE_OPENAI_API_VERSION=<api-version>
AZURE_OPENAI_DEPLOYMENT_NAME=<your-chat-deployment-name>
```

## 執行 CLI

```bash
python -m app.cli
```

啟動後會看到：

```text
Foundry Agent Starter
Type 'exit' or 'quit' to leave.
```

輸入問題後，程式會呼叫 `ask_agent(question)`，並印出 Agent 的回答。

## 測試問題範例

```text
請用三點說明員工報銷流程。
```

```text
幫我寫一封簡短的會議提醒信。
```

```text
請整理一份新人入職待辦清單。
```

## 注意事項

請不要 commit `.env` 或任何 API key。`.env` 已經包含在 `.gitignore` 中，請只提交 `.env.example` 作為設定範例。
