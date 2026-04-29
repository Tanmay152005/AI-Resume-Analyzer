from skills_db import SKILL_CATEGORIES


def extract_skills(text):
    text = text.lower()
    found_skills = set()

    for category, skills in SKILL_CATEGORIES.items():
        for skill in skills:
            if skill.lower() in text:
                found_skills.add(skill)

    return list(found_skills)


def categorize_skills(skills):
    categorized = {}

    for category, category_skills in SKILL_CATEGORIES.items():
        matched = [skill for skill in skills if skill in category_skills]

        if matched:
            categorized[category] = matched

    return categorized


def compare_skills(jd_skills, resume_skills):
    matched = list(set(jd_skills) & set(resume_skills))
    missing = list(set(jd_skills) - set(resume_skills))

    return matched, missing