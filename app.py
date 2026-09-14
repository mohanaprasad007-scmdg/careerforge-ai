from flask import Flask, request, jsonify, send_from_directory
from openai import OpenAI
import os

app = Flask(__name__)

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

@app.route("/")
def home():
    return send_from_directory(".", "index.html")

@app.route("/api/analyze-resume", methods=["POST"])
def analyze_resume():
    data = request.get_json() or {}
    resume = data.get("resume", "").strip()

    if not resume:
        return jsonify({"error": "Resume is empty"}), 400

    if len(resume) > 20000:
        resume = resume[:20000]

    prompt = f"""
You are an expert career and recruitment advisor.

Analyze this resume:

{resume}

Return a concise career analysis with:

1. Resume score out of 100
2. Strong points
3. Missing skills
4. ATS improvements
5. Project improvements
6. Recommended career roles
7. A practical 30-day improvement plan

Be honest, specific and useful for a college student.
"""

    try:
        response = client.responses.create(
            model="gpt-5.6-luna",
            input=prompt
        )

        answer = response.output_text

        return jsonify({
            "success": True,
            "answer": answer
        })

    except Exception as e:
        return jsonify({
            "error": "AI analysis failed",
            "details": str(e)
        }), 500


@app.route("/api/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
