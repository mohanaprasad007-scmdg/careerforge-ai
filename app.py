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

Be honest. Do not invent experience or skills.
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

Your job is to guide students from ZERO knowledge to a realistic career.

STUDENT INFORMATION

Education:
{education}

Year:
{year or "Not specified"}

Interests:
{interests or "Not specified"}

Strengths:
{strengths or "Not specified"}

Things they dislike:
{dislikes or "Not specified"}

Preferred type of work:
{preference or "Not specified"}

Available learning time:
{time or "Not specified"}

Main goal:
{goal or "Not specified"}

Current skill level:
{level or "Complete beginner"}

Dream career:
{dream or "I don't know"}

IMPORTANT:
The student may have zero skills and may not know what career to choose.

Do NOT simply give a generic list of courses.

Analyze the student's situation and create a clear, realistic and future-focused direction.

Your response MUST contain:

1. 🎯 BEST CAREER DIRECTIONS
Recommend 2-4 suitable career paths.
Rank them from strongest to weakest.

For each path explain:
- Why it fits
- What the student will actually do in that career
- Important skills
- Difficulty for this student
- Possible entry-level roles

2. ⭐ RECOMMENDED PRIMARY PATH
Choose ONE primary path.
Explain why you selected it.
If the student has no clear preference, choose based on their information and clearly say that this is a recommendation, not a guarantee.

3. 📊 CURRENT STARTING POINT
Explain what the student knows and what they need to learn.
Assume beginner level when information is missing.

4. 🗺️ 12-MONTH ROADMAP
Create a month-by-month roadmap.

Include:
Month 1
Month 2
Month 3
...
Month 12

For every stage include:
- What to learn
- Why it matters
- What to practice
- What output/project should be completed

5. 📅 FIRST 30 DAYS
Create a practical beginner plan.

Week 1
Week 2
Week 3
Week 4

Keep it achievable with the student's available time.

6. 🚀 PROJECT ROADMAP
Recommend projects in this order:
- Very easy first project
- Beginner project
- Intermediate project
- Portfolio project
- Advanced/capstone project

Explain what each project proves.

7. 🧠 SKILLS TO LEARN
Separate into:
- Technical skills
- Communication skills
- Problem solving
- Career skills

Prioritize them.

8. 💼 CAREER ENTRY PLAN
Explain when the student should start:
- Building GitHub/portfolio
- Creating a resume
- Applying for internships
- Applying for jobs
- Preparing for interviews

9. 📈 CAREER PROGRESSION
Show a realistic progression such as:

Beginner
→ Student projects
→ Internship
→ Entry-level role
→ Professional
→ Advanced role

10. ⚠️ COMMON MISTAKES
Give 5 mistakes this student should avoid.

11. 🔥 NEXT ACTION
End with exactly 3 things the student should do TODAY.

Be encouraging but honest.
Do not promise a job or salary.
Do not recommend learning everything at once.
Focus on one primary career direction.
Explain WHY before WHAT.
Use simple language suitable for a college student.
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
