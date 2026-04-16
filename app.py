import streamlit as st
import os
import uuid

from src.parser import extract_text_from_pdf
from src.preprocess import preprocess_text
from src.vectorizer import get_tfidf_vectors
from src.similarity import calculate_similarity
from src.keyword_matcher import get_missing_keywords
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

            # Step 1: Extract text
            resume_text = extract_text_from_pdf(file_path)

            # Step 2: Preprocess
            clean_resume = preprocess_text(resume_text)
            clean_jd = preprocess_text(jd_text)

            # Step 3: TF-IDF
            resume_vec, jd_vec = get_tfidf_vectors(clean_resume, clean_jd)

            # Step 4: Score
            score = calculate_similarity(resume_vec, jd_vec)
            match_percentage = round(score * 100, 2)

            # Step 5: Keywords
            missing_keywords = get_missing_keywords(clean_resume, clean_jd)

            # Step 6: Gemini (only if needed)
            if missing_keywords:
                feedback = get_resume_feedback(resume_text, jd_text, missing_keywords)
            else:
                feedback = "✅ Your resume is already well aligned with the job description."

            # Cleanup file
            os.remove(file_path)

            # -------- OUTPUT --------
            st.subheader("📊 Match Score")
            st.progress(int(match_percentage))
            st.write(f"**Match Percentage: {match_percentage}%**")

            st.subheader("❌ Missing Keywords")
            if missing_keywords:
                st.write(", ".join(missing_keywords))
            else:
                st.success("No major keywords missing 🎉")

            st.subheader("🤖 Suggestions")
            st.write(feedback)

        except Exception as e:
            st.error(f"Error: {e}")