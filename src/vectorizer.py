from sklearn.feature_extraction.text import TfidfVectorizer

def get_tfidf_vectors(resume_text: str, jd_text: str):
    """
    Convert resume and job description into TF-IDF vectors.
    """

    vectorizer = TfidfVectorizer()

    vectors = vectorizer.fit_transform([resume_text, jd_text])

    resume_vector = vectors[0]
    jd_vector = vectors[1]

    return resume_vector, jd_vector