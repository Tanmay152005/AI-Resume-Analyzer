import spacy

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

def preprocess_text(text: str) -> str:
    doc = nlp(text.lower())

    tokens = []

    for token in doc:
        if not token.is_stop and not token.is_punct and token.is_alpha:
            tokens.append(token.lemma_)

    return " ".join(tokens)