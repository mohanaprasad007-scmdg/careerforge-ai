from flask import Flask, request, jsonify, send_from_directory
from openai import OpenAI
import os

app = Flask(__name__)

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)


# =========================
# HOME
# =========================

@app.route("/")
def home():
    return send_from_directory(".", "index.html")


# =========================
# RESUME ANALYZER
# =========================

@app.route("/api/analyze-resume", methods=["POST"])
def analyze_resume():

    data = request.get_json() or {}
    resume = data.get("resume", "").strip()

    if not resume:
        return jsonify({
            "error": "Resume is empty"
        }), 400

    resume = resume[:20000]

    prompt = f"""
You are an expert career and recruitment advisor.

Analyze this resume:

{resume}

Return:

1. RESUME SCORE out of 100
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

        return jsonify({
            "success": True,
            "answer": response.output_text
        })

    except Exception as e:

        return jsonify({
            "error": "AI analysis failed",
            "details": str(e)
        }), 500


# =========================
# JOB MATCHER
# =========================

@app.route("/api/job-match", methods=["POST"])
def job_match():

    data = request.get_json() or {}

    resume = data.get("resume", "").strip()
    job = data.get("job", "").strip()

    if not resume:
        return jsonify({
            "error": "Resume is required"
        }), 400

    if not job:
        return jsonify({
            "error": "Job description is required"
        }), 400

    resume = resume[:18000]
    job = job[:12000]

    prompt = f"""
You are an expert AI recruitment advisor.

Compare this candidate resume with this job description.

RESUME:
{resume}

JOB DESCRIPTION:
{job}

Return:

1. MATCH SCORE: 0-100%
2. MATCH SUMMARY
3. MATCHED SKILLS
4. MISSING SKILLS
5. IMPORTANT ATS KEYWORDS
6. EXPERIENCE MATCH
7. PROJECT GAPS
8. SHOULD APPLY: YES / MAYBE / NO
9. 5-STEP IMPROVEMENT PLAN
10. 5 INTERVIEW TOPICS TO PREPARE

Be practical and honest.
Focus on helping a student improve their chances.
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


# =========================
# ZERO TO CAREER
# =========================

@app.route("/api/career-guide", methods=["POST"])
def career_guide():

    data = request.get_json() or {}

    education = data.get("education", "").strip()
    year = data.get("year", "").strip()
    interests = data.get("interests", "").strip()
    strengths = data.get("strengths", "").strip()
    dislikes = data.get("dislikes", "").strip()
    preference = data.get("preference", "").strip()
    time = data.get("time", "").strip()
    goal = data.get("goal", "").strip()
    level = data.get("level", "").strip()
    dream = data.get("dream", "").strip()

    if not education:
        return jsonify({
            "error": "Education is required"
        }), 400

    prompt = f"""
You are CareerForge AI, an expert career mentor.

Create a personalized career roadmap for this student.

Education:
{education}

Year:
{year}

Interests:
{interests}

Strengths:
{strengths}

Things they dislike:
{dislikes}

Preferred work:
{preference}

Learning time:
{time}

Main goal:
{goal}

Current skill level:
{level}

Dream career:
{dream}

Return:

1. BEST CAREER DIRECTIONS
2. RECOMMENDED PRIMARY PATH
3. CURRENT STARTING POINT
4. WHY THIS PATH FITS
5. SKILLS TO LEARN
6. FIRST 30 DAYS
7. MONTHS 2-3
8. MONTHS 4-6
9. MONTHS 7-12
10. PROJECT ROADMAP
11. HOW TO GET FIRST INTERNSHIP OR JOB
12. LONG-TERM CAREER PROGRESSION
13. COMMON MISTAKES TO AVOID
14. NEXT 3 ACTIONS TO DO TODAY

If the student is a complete beginner, explain everything simply.

If the goal is entrepreneurship or starting a business,
include business validation, skills, customer discovery,
MVP development and realistic first steps.

Do not give generic advice.
Make the roadmap practical and achievable.
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
            "error": "Career guidance failed",
            "details": str(e)
        }), 500


# =========================
# CAREER DASHBOARD
# =========================

@app.route("/api/career-dashboard", methods=["POST"])
def career_dashboard():

    data = request.get_json() or {}

    education = data.get("education", "").strip()
    career = data.get("career", "").strip()
    level = data.get("level", "").strip()
    skills = data.get("skills", "").strip()
    projects = data.get("projects", "").strip()
    resume_score = data.get("resume_score", "").strip()
    job_score = data.get("job_score", "").strip()
    completed = data.get("completed", "").strip()

    prompt = f"""
You are CareerForge AI Career Dashboard.

Analyze the student's current career progress.

Education:
{education}

Target career:
{career}

Current level:
{level}

Skills:
{skills}

Projects:
{projects}

Resume score:
{resume_score}

Job match score:
{job_score}

Completed work:
{completed}

Return:

CAREER STATUS

CAREER READINESS SCORE: 0-100

CURRENT STAGE:
STARTING / LEARNING / BUILDING / INTERNSHIP READY / JOB READY

TOP 3 PRIORITIES

TODAY'S 3 TASKS

THIS WEEK

SKILLS TO FOCUS ON

NEXT MILESTONE

WHAT NOT TO DO

NEXT CAREER STEP

Make the advice specific and actionable.
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
            "error": "Dashboard analysis failed",
            "details": str(e)
        }), 500


# =========================
# AI INTERVIEW COACH
# =========================

@app.route("/api/interview", methods=["POST"])
def interview():

    data = request.get_json() or {}

    role = data.get("role", "").strip()
    level = data.get("level", "").strip()
    question = data.get("question", "").strip()
    answer = data.get("answer", "").strip()
    history = data.get("history", "")

    if not role:
        return jsonify({
            "error": "Target role is required"
        }), 400

    # First question
    if not question:

        prompt = f"""
You are CareerForge AI Interview Coach.

Start a realistic job interview.

Target role:
{role}

Candidate level:
{level}

Ask ONE interview question only.

The question should be appropriate for the candidate's
career level and target role.

Do not provide the answer.
Do not ask multiple questions.

Return only the interview question.
"""

    else:

        prompt = f"""
You are CareerForge AI Interview Coach.

Conduct a realistic interview for:

Target role:
{role}

Candidate level:
{level}

Previous interview history:
{history[:12000]}

Previous question:
{question}

Candidate answer:
{answer[:8000]}

Evaluate the answer briefly.

Return:

SCORE: 0-100

WHAT WAS GOOD:
- ...

WHAT TO IMPROVE:
- ...

BETTER APPROACH:
- ...

Then ask ONE next interview question.

The next question should adapt to the candidate's
previous answer.

Do not ask multiple questions.
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
            "error": "Interview coach failed",
            "details": str(e)
        }), 500


# =========================
# INTERVIEW FINAL REPORT
# =========================

@app.route("/api/interview-report", methods=["POST"])
def interview_report():

    data = request.get_json() or {}

    role = data.get("role", "").strip()
    history = data.get("history", "")

    if not role:
        return jsonify({
            "error": "Target role is required"
        }), 400

    prompt = f"""
You are CareerForge AI Interview Coach.

Create a final interview performance report.

Target role:
{role}

Interview history:
{history[:20000]}

Return:

1. FINAL INTERVIEW SCORE /100
2. OVERALL PERFORMANCE
3. TECHNICAL KNOWLEDGE
4. COMMUNICATION
5. PROBLEM SOLVING
6. CONFIDENCE
7. STRONGEST AREAS
8. WEAK AREAS
9. QUESTIONS TO PRACTICE
10. 7-DAY INTERVIEW IMPROVEMENT PLAN
11. JOB READINESS:
BEGINNER / DEVELOPING / INTERVIEW READY / JOB READY

Be honest but encouraging.
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
            "error": "Interview report failed",
            "details": str(e)
        }), 500


# =========================
# HEALTH CHECK
# =========================

@app.route("/api/health")
def health():

    return jsonify({
        "status": "ok",
        "service": "CareerForge AI"
    })


# =========================
# RUN
# =========================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )
