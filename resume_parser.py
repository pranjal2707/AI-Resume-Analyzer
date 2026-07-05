import re
import pdfplumber
import spacy

nlp = spacy.load("en_core_web_sm")

SKILLS = [
    "python", "java", "c++", "sql", "mysql",
    "tensorflow", "keras", "pytorch",
    "machine learning", "deep learning",
    "django", "flask", "react", "nodejs",
    "streamlit", "power bi", "excel"
]


class ResumeParser:

    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.text = self.extract_text()

    def extract_text(self):
        text = ""
        with pdfplumber.open(self.pdf_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text

    def extract_email(self):
        emails = re.findall(
            r'[\w\.-]+@[\w\.-]+\.\w+',
            self.text
        )
        return emails[0] if emails else None

    def extract_phone(self):
        phones = re.findall(
            r'(\+?\d[\d\s\-]{8,15})',
            self.text
        )
        return phones[0] if phones else None

    def extract_name(self):
        doc = nlp(self.text[:1000])

        for ent in doc.ents:
            if ent.label_ == "PERSON":
                return ent.text

        return None

    def extract_skills(self):
        text = self.text.lower()

        found = []

        for skill in SKILLS:
            if skill.lower() in text:
                found.append(skill)

        return list(set(found))

    def extract_degree(self):

        degrees = [
            "b.tech",
            "btech",
            "b.e",
            "be",
            "m.tech",
            "mtech",
            "mba",
            "bca",
            "mca",
            "b.sc",
            "m.sc"
        ]

        text = self.text.lower()

        found = []

        for d in degrees:
            if d in text:
                found.append(d)

        return found

    def get_extracted_data(self):

        return {
            "name": self.extract_name(),
            "email": self.extract_email(),
            "mobile_number": self.extract_phone(),
            "skills": self.extract_skills(),
            "degree": self.extract_degree(),
            "no_of_pages": 1
        }