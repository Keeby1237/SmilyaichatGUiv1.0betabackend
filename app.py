from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline

# Load the Hugging Face model
model_id = "Smilyai-labs/Sam-reason-S3"
pipe = pipeline("text-generation", model=model_id)

app = FastAPI(title="Sam-reason-S3 Inference API")

class InferRequest(BaseModel):
    prompt: str
    max_new_tokens: int = 50

@app.post("/generate")
def generate(req: InferRequest):
    result = pipe(req.prompt, max_new_tokens=req.max_new_tokens)
    return {"result": result}
