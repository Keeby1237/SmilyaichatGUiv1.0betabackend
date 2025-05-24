from fastapi import FastAPI, Request, Form
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel
from transformers import pipeline

model_id = "Smilyai-labs/Sam-reason-S3"
pipe = pipeline("text-generation", model=model_id)

app = FastAPI(title="Sam-reason-S3 Inference API")

class InferRequest(BaseModel):
    prompt: str
    max_new_tokens: int = 50

@app.get("/", response_class=HTMLResponse)
def get_home():
    # Serve index.html from the root directory
    return FileResponse("index.html", media_type="text/html")

@app.post("/", response_class=HTMLResponse)
async def generate_form(request: Request):
    form = await request.form()
    prompt = form.get("prompt", "")
    max_new_tokens = int(form.get("max_new_tokens", 50))
    result = pipe(prompt, max_new_tokens=max_new_tokens)
    generated = result[0]['generated_text']
    # Read the HTML, inject the result (very basic template replacement)
    with open("index.html", encoding="utf-8") as f:
        html = f.read()
    html = html.replace("{{result}}", generated).replace("{{prompt}}", prompt).replace("{{max_new_tokens}}", str(max_new_tokens))
    return HTMLResponse(content=html)

@app.post("/generate")
def generate(req: InferRequest):
    result = pipe(req.prompt, max_new_tokens=req.max_new_tokens)
    return {"result": result}
