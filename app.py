import streamlit as st
import os
import uuid

from skill_extractor import extract_skills, categorize_skills, compare_skills
from resume_validator import is_resume

from src.parser import extract_text_from_pdf
from src.preprocess import preprocess_text
from src.vectorizer import get_tfidf_vectors
from src.similarity import calculate_similarity
from src.gemini_service import get_resume_feedback


st.set_page_config(page_title="AI Resume Analyzer", layout="wide")

st.title("📄 AI Resume Analyzer")

# Layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("Job Description")
    jd_text = st.text_area("Paste Job Description here", height=300)

with col2:
    st.subheader("Upload Resume")
    uploaded_file = st.file_uploader("Upload PDF Resume", type=["pdf"])


if st.button("Analyze Resume"):

    if not jd_text or not uploaded_file:
        st.warning("Please provide both Resume and Job Description")

    else:
        try:
            # Save file temporarily
            file_id = str(uuid.uuid4())
            file_path = f"temp_{file_id}.pdf"

            with open(file_path, "wb") as f:
                f.write(uploaded_file.read())

            # Step 1: Extract Resume Text
            resume_text = extract_text_from_pdf(file_path)

            # Step 1.5: Validate Resume
            if not is_resume(resume_text):
                os.remove(file_path)
                st.error("Uploaded document does not appear to be a valid resume. Please upload a proper resume PDF.")
                st.stop()

            # Step 2: Preprocess Text
            clean_resume = preprocess_text(resume_text)
            clean_jd = preprocess_text(jd_text)

            # Step 3: TF-IDF Vectorization
            resume_vec, jd_vec = get_tfidf_vectors(clean_resume, clean_jd)

            # Step 4: Similarity Score
            score = calculate_similarity(resume_vec, jd_vec)
            match_percentage = round(score * 100, 2)

            # Step 5: Skill Extraction
            jd_skills = extract_skills(clean_jd)
            resume_skills = extract_skills(clean_resume)

            matched_skills, missing_skills = compare_skills(jd_skills, resume_skills)

            categorized_matched = categorize_skills(matched_skills)
            categorized_missing = categorize_skills(missing_skills)

            # Step 6: Gemini Feedback
            if missing_skills:
                feedback = get_resume_feedback(resume_text, jd_text, missing_skills)
            else:
                feedback = "✅ Your resume is already well aligned with the job description."

            # Cleanup temp file
            os.remove(file_path)

            # -------- OUTPUT --------

            st.subheader("📊 Match Score")
            st.progress(int(match_percentage))
            st.write(f"**Match Percentage: {match_percentage}%**")

            st.subheader("✅ Matched Skills")
            if categorized_matched:
                for category, skills in categorized_matched.items():
                    formatted_skills = [skill.title() for skill in skills]
                    st.write(f"**{category}:** {', '.join(formatted_skills)}")
            else:
                st.warning("No matched skills detected.")

            st.subheader("❌ Missing Skills")
            if categorized_missing:
                for category, skills in categorized_missing.items():
                    formatted_skills = [skill.title() for skill in skills]
                    st.write(f"**{category}:** {', '.join(formatted_skills)}")
            else:
                st.success("No major skills missing 🎉")

            st.subheader("🤖 Suggestions")
            st.write(feedback)

        except Exception as e:
            st.error(f"Error: {e}")