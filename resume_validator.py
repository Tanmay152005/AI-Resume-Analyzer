import re


RESUME_SECTIONS = [
    "skills",
    "education",
    "experience",
    "projects",
    "internship",
    "certifications",
    "summary",
    "objective"
]


def is_resume(text):
    text = text.lower()

    # Count resume-like section keywords
    section_matches = sum(
        1 for section in RESUME_SECTIONS if section in text
    )

    # Detect email
    email_found = re.search(
        r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
        text
    )

    # Detect phone number
    phone_found = re.search(
        r"(\+?\d{1,3}[-.\s]?)?(\d{10})",
        text
    )

    # Resume validation logic
    if section_matches >= 2 and (email_found or phone_found):
        return True

    return False