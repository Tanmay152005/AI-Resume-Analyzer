# 📄 AI Resume Analyzer

An AI-powered web application that analyzes resumes against job descriptions and provides:
- Match score (ATS-style)
- Missing keywords
- AI-based improvement suggestions

---

## 🚀 Features

- 📊 **Match Score Calculation**
  - Uses TF-IDF and Cosine Similarity
  - Gives percentage match between resume and job description

- ❌ **Missing Keywords Detection**
  - Extracts important keywords using NLP (spaCy)
  - Highlights missing skills

- 🤖 **AI Suggestions (Gemini)**
  - Provides resume improvement suggestions
  - Includes fallback logic if API is unavailable

- 📂 **PDF Resume Upload**
  - Extracts and processes resume content

---

## 🛠️ Tech Stack

- **Frontend/UI:** Streamlit  
- **Backend:** Python  
- **NLP:** spaCy  
- **ML Logic:** TF-IDF, Cosine Similarity (scikit-learn)  
- **AI:** Google Gemini API  
- **PDF Parsing:** PyPDF2  

## Enhancements made
 - Added resume_validator.py which ensures only resumes are uploaded
 - Added skills_db.py with categorized tech skill directory
 - Added skill_extractor.py for skill matching and comparison
 - Updated app.py to use skill-based matching with category display
---

