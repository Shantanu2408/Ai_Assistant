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
        credential = DefaultAzureCredential()

        def token_provider():
            return credential.get_token(
                "https://ai.azure.com/.default"
            ).token

        client = AzureOpenAI(
            azure_endpoint=os.getenv("AZURE_AI_PROJECT_ENDPOINT"),
            azure_ad_token_provider=token_provider
            # ✅ NO api_version here
        )

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
