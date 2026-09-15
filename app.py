from flask import Flask, request, jsonify, send_from_directory
from openai import OpenAI
import os

app = Flask(__name__)

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)


@app.route("/")
def home():
    return send_from_directory(".", "index.html")


@app.route("/api/analyze-resume", methods=["POST"])
def analyze_resume():
    data = request.get_json() or {}
    resume = data.get("resume", "").strip()

    if not resume:
        return jsonify({"error": "Resume is empty"}), 400

    resume = resume[:20000]

    prompt = f"""
You are an expert career and recruitment advisor.

Analyze this resume:

{resume}

Give a concise but useful analysis containing:

1. Resume score out of 100
2. Strong points
3. Missing skills
4. ATS improvements
5. Project improvements
6. Recommended career roles
7. Practical 30-day improvement plan

Be specific and helpful for a college student.
"""

    try:
        response = client.responses.create(
            model="gpt-5.6-luna",
            input=prompt
        )

        return jsonify({
            "success": True,
            "answer": response.output_text
        })

    except Exception as e:
        return jsonify({
            "error": "AI analysis failed",
            "details": str(e)
        }), 500


@app.route("/api/job-match", methods=["POST"])
def job_match():
    data = request.get_json() or {}

    resume = data.get("resume", "").strip()
    job = data.get("job", "").strip()

    if not resume:
        return jsonify({"error": "Resume is empty"}), 400

    if not job:
        return jsonify({"error": "Job description is empty"}), 400

    resume = resume[:18000]
    job = job[:12000]

    prompt = f"""
You are an expert technical recruiter and career advisor.

Compare the candidate's resume with the job description.

CANDIDATE RESUME:
{resume}

JOB DESCRIPTION:
{job}

Provide a clear job-match analysis.

Return:

1. MATCH SCORE: Give a percentage from 0 to 100.

2. MATCH SUMMARY:
Explain briefly how suitable the candidate is.

3. SKILLS MATCHED:
List skills from the job that the candidate already has.

4. MISSING SKILLS:
List important skills required by the job that are missing.

5. ATS KEYWORDS:
List important keywords from the job description that should appear naturally in the resume.

6. EXPERIENCE MATCH:
Explain whether the candidate's projects, education and experience match the role.

7. PROJECT GAPS:
Suggest projects that would make the candidate stronger.

8. SHOULD APPLY:
Answer YES, MAYBE, or NO and explain why.

9. IMPROVEMENT PLAN:
Give 5 practical steps the candidate should take to become a stronger applicant.

10. INTERVIEW PREPARATION:
Give 5 topics the candidate should prepare for this specific job.

Be honest. Do not invent experience or skills that are not present in the resume.
Keep the answer easy to understand for a college student.
"""

    try:
        response = client.responses.create(
            model="gpt-5.6-luna",
            input=prompt
        )

        return jsonify({
            "success": True,
            "answer": response.output_text
        })

    except Exception as e:
        return jsonify({
            "error": "Job matching failed",
            "details": str(e)
        }), 500


@app.route("/api/health")
def health():
    return jsonify({
        "status": "ok",
        "service": "CareerForge AI"
    })


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )
