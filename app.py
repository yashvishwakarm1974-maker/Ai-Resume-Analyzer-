from flask import Flask, render_template, request
from utils import (
    extract_text_from_pdf,
    extract_text_from_docx,
    calculate_ats_score
)

import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@app.route("/", methods=["GET", "POST"])
def home():

    score = None
    matched_keywords = []
    missing_keywords = []

    if request.method == "POST":

        # Job Description
        job_description = request.form["job_description"]

        # Uploaded Resume
        resume = request.files["resume"]

        file_path = os.path.join(
            app.config["UPLOAD_FOLDER"],
            resume.filename
        )

        resume.save(file_path)

        # Extract Resume Text
        if resume.filename.endswith(".pdf"):
            resume_text = extract_text_from_pdf(file_path)

        elif resume.filename.endswith(".docx"):
            resume_text = extract_text_from_docx(file_path)

        else:
            resume_text = ""

        # ATS Calculation
        score, matched_keywords, missing_keywords = calculate_ats_score(
            resume_text,
            job_description
        )

    return render_template(
        "index.html",
        score=score,
        matched_keywords=matched_keywords,
        missing_keywords=missing_keywords
    )


if __name__ == "__main__":
    app.run(debug=True)