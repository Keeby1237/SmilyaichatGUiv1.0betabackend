from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from transformers import pipeline

# Load the Hugging Face model
model_id = "Smilyai-labs/Sam-reason-S3"
pipe = pipeline("text-generation", model=model_id)

app = FastAPI(title="Sam-reason-S3 Inference API")
templates = Jinja2Templates(directory="templates")

class InferRequest(BaseModel):
    prompt: str
    max_new_tokens: int = 50

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    # Show the template at the home route
    return templates.TemplateResponse("index.html", {"request": request, "result": None, "prompt": "", "max_new_tokens": 50})

@app.post("/", response_class=HTMLResponse)
def generate_form(request: Request, prompt: str = Form(...), max_new_tokens: int = Form(50)):
    result = pipe(prompt, max_new_tokens=max_new_tokens)
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "result": result[0]["generated_text"],
            "prompt": prompt,
            "max_new_tokens": max_new_tokens,
        },
    )

@app.post("/generate")
def generate(req: InferRequest):
    result = pipe(req.prompt, max_new_tokens=req.max_new_tokens)
    return {"result": result}
