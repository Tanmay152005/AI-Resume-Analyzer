from sklearn.metrics.pairwise import cosine_similarity

def calculate_similarity(resume_vector, jd_vector) -> float:
    """
    Calculate cosine similarity between resume and job description
    """

    similarity = cosine_similarity(resume_vector, jd_vector)

    return float(similarity[0][0])