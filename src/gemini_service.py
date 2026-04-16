import os
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not set in .env file")

# Initialize Gemini client
client = genai.Client(api_key=api_key)


def get_resume_feedback(resume_text: str, jd_text: str, missing_keywords: list) -> str:
    """
    Generate AI-based feedback using Gemini.
    Falls back to rule-based suggestions if API fails.
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=f"""
You are an ATS expert.

Analyze the resume against the job description.

Provide:
1. Missing skills
2. Resume improvement suggestions
3. Weak areas in resume

Resume:
{resume_text}

Job Description:
{jd_text}

Missing Keywords:
{', '.join(missing_keywords)}
"""
        )

        return response.text

    except Exception:
        # 🔥 Fallback logic (very important)
        if missing_keywords:
            return f"""
🔧 Suggestions to improve your resume:

• Add these important skills: {', '.join(missing_keywords[:5])}\n
• Include projects that use these technologies\n
• Highlight practical experience related to these skills\n
• Add measurable achievements (e.g., improved performance by X%)\n
• Use strong action verbs and clear bullet points\n

💡 Tip: Tailor your resume specifically for each job description.
"""
        else:
            return "✅ Your resume is already well aligned with the job description."