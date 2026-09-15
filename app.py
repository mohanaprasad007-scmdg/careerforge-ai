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

Provide:

1. MATCH SCORE: percentage from 0 to 100.

2. MATCH SUMMARY

3. SKILLS MATCHED

4. MISSING SKILLS

5. ATS KEYWORDS

6. EXPERIENCE MATCH

7. PROJECT GAPS

8. SHOULD APPLY:
YES, MAYBE, or NO

9. IMPROVEMENT PLAN:
5 practical steps.

10. INTERVIEW PREPARATION:
5 topics to prepare.

Be honest.
Do not invent experience or skills.
Keep the answer useful for a college student.
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
        return jsonify({"error": "Education is required"}), 400

    prompt = f"""
You are CareerForge AI, an expert career mentor for college students.

Guide this student from their current level toward a realistic career.

Education:
{education}

Year:
{year or "Not specified"}

Interests:
{interests or "Not specified"}

Strengths:
{strengths or "Not specified"}

Dislikes:
{dislikes or "Not specified"}

Preferred work:
{preference or "Not specified"}

Learning time:
{time or "Not specified"}

Goal:
{goal or "Not specified"}

Current level:
{level or "Complete beginner"}

Dream career:
{dream or "I don't know"}

The student may have zero skills and may not know what career to choose.

Create a clear, realistic, future-focused plan.

Include:

1. BEST CAREER DIRECTIONS
Recommend 2-4 paths and rank them.

2. RECOMMENDED PRIMARY PATH
Choose ONE and explain why.

3. CURRENT STARTING POINT

4. 12-MONTH ROADMAP
Month 1 through Month 12.

5. FIRST 30 DAYS
Week 1 through Week 4.

6. PROJECT ROADMAP
Easy → Beginner → Intermediate → Portfolio → Capstone.

7. SKILLS TO LEARN
Technical, communication, problem solving and career skills.

8. CAREER ENTRY PLAN
When to build portfolio, resume, apply for internships and jobs.

9. CAREER PROGRESSION
Beginner → Projects → Internship → Entry role → Advanced role.

10. COMMON MISTAKES
Five mistakes to avoid.

11. NEXT ACTION
Exactly 3 things to do today.

Do not promise a job or salary.
Do not recommend learning everything at once.
Focus on one primary direction.
Explain WHY before WHAT.
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


@app.route("/api/career-dashboard", methods=["POST"])
def career_dashboard():

    data = request.get_json() or {}

    education = data.get("education", "").strip()
    career = data.get("career", "").strip()
    level = data.get("level", "").strip()
    skills = data.get("skills", "").strip()
    projects = data.get("projects", "").strip()
    resume_score = data.get("resume_score", "")
    job_score = data.get("job_score", "")
    completed = data.get("completed", "").strip()

    if not education:
        return jsonify({
            "error": "Education is required"
        }), 400

    prompt = f"""
You are CareerForge AI.

Create a simple student career dashboard.

STUDENT:
Education: {education}
Target career: {career or "Not decided"}
Current level: {level or "Beginner"}
Skills: {skills or "None yet"}
Projects: {projects or "None yet"}
Resume score: {resume_score or "Not tested"}
Latest job match: {job_score or "Not tested"}
Completed work: {completed or "Nothing completed yet"}

The student needs clear future-focused guidance.

Return exactly these sections:

CAREER STATUS
Give a short assessment.

CAREER READINESS
Give a score from 0 to 100.
Explain the score briefly.

CURRENT STAGE
Identify the student's current stage:
STARTING / LEARNING / BUILDING / INTERNSHIP READY / JOB READY

TOP 3 PRIORITIES
Give exactly 3 priorities.

TODAY'S 3 TASKS
Give exactly 3 realistic tasks that can be completed today.

THIS WEEK
Give a 7-day mini plan.

SKILLS TO FOCUS ON
List the 3 most important skills right now.

NEXT MILESTONE
Give one measurable milestone.

WHAT NOT TO DO
Give 3 things the student should avoid.

NEXT CAREER STEP
Tell the student the single most important next step.

Be encouraging but realistic.
Do not promise employment.
Do not overwhelm the student.
Prioritize actions over theory.
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
            "error": "Dashboard generation failed",
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
