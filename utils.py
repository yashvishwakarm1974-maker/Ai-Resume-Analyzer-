from PyPDF2 import PdfReader
from docx import Document

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import re


# Extract PDF Text
def extract_text_from_pdf(file_path):

    text = ""

    pdf = PdfReader(file_path)

    for page in pdf.pages:
        extracted = page.extract_text()

        if extracted:
            text += extracted

    return text


# Extract DOCX Text
def extract_text_from_docx(file_path):

    text = ""

    doc = Document(file_path)

    for para in doc.paragraphs:
        text += para.text + " "

    return text


# ATS Score Logic
def calculate_ats_score(resume_text, job_description):

    resume_text = resume_text.lower()
    job_description = job_description.lower()

    # Remove symbols
    resume_text = re.sub(r'[^a-zA-Z0-9 ]', '', resume_text)
    job_description = re.sub(r'[^a-zA-Z0-9 ]', '', job_description)

    # Similarity
    cv = CountVectorizer(stop_words='english')

    matrix = cv.fit_transform([
        resume_text,
        job_description
    ])

    similarity = cosine_similarity(matrix)[0][1]

    score = round(similarity * 100)

    # Keywords
    jd_words = set(job_description.split())
    resume_words = set(resume_text.split())

    matched_keywords = list(
        jd_words.intersection(resume_words)
    )

    missing_keywords = list(
        jd_words.difference(resume_words)
    )

    return (
        score,
        matched_keywords[:20],
        missing_keywords[:20]
    )