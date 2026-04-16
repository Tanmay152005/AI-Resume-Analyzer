import spacy

nlp = spacy.load("en_core_web_sm")

# Words to ignore (very important)
STOP_WORDS = {
    "work", "join", "requirement", "responsibility", "knowledge",
    "familiarity", "application", "developer", "code", "service"
}

def extract_keywords(text: str):
    doc = nlp(text)

    keywords = set()

    for token in doc:
        if (
            token.pos_ in ["NOUN", "PROPN"] and
            token.is_alpha and
            len(token.text) > 2 and
            token.lemma_.lower() not in STOP_WORDS
        ):
            keywords.add(token.lemma_.lower())

    return keywords


def get_missing_keywords(resume_text: str, jd_text: str):
    resume_keywords = extract_keywords(resume_text)
    jd_keywords = extract_keywords(jd_text)

    missing = jd_keywords - resume_keywords

    return sorted(list(missing))