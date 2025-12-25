from fastapi import FastAPI, HTTPException
from azure.identity import DefaultAzureCredential
from openai import AzureOpenAI
import os

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/chat")
def chat(payload: dict):
    try:
        # 1. Get Azure AD token via Managed Identity
        credential = DefaultAzureCredential()

        # 2. Create Foundry OpenAI client (NO API KEY)
        client = AzureOpenAI(
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            azure_ad_token_provider=credential.get_token,
            api_version="2024-02-15-preview"
        )

        # 3. Call your GPT-5 deployment
        completion = client.chat.completions.create(
            model=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
            messages=[
                {"role": "user", "content": payload["message"]}
            ]
        )

        return {
            "response": completion.choices[0].message.content
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
