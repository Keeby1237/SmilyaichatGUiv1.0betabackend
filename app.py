from flask import Flask, request, render_template_string, send_file, jsonify
from transformers import pipeline

app = Flask(__name__)

# Load Hugging Face model
model_id = "Smilyai-labs/Sam-reason-S3"
pipe = pipeline("text-generation", model=model_id)

def read_html(replace=None):
    with open("index.html", encoding="utf-8") as f:
        html = f.read()
    if replace:
        for k, v in replace.items():
            html = html.replace("{{" + k + "}}", v)
    return html

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        prompt = request.form.get("prompt", "")
        max_new_tokens = int(request.form.get("max_new_tokens", 50))
        result = pipe(prompt, max_new_tokens=max_new_tokens)
        formatted = result[0]["generated_text"]
        html = read_html({
            "prompt": prompt,
            "max_new_tokens": str(max_new_tokens),
            "result": formatted
        })
        return render_template_string(html)
    # GET
    html = read_html({
        "prompt": "",
        "max_new_tokens": "50",
        "result": ""
    })
    return render_template_string(html)

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json(force=True)
    prompt = data.get("prompt", "")
    max_new_tokens = int(data.get("max_new_tokens", 50))
    result = pipe(prompt, max_new_tokens=max_new_tokens)
    return jsonify({"result": result})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
