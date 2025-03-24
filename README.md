# Smart ATS - Resume Matcher

Smart ATS is a Streamlit-based web application that leverages Google's Gemini generative AI (Gemini-1.5-pro) to evaluate resumes against job descriptions. The application extracts text from PDF resumes, evaluates them using a strict JSON output prompt, and presents detailed feedback for resume improvements.

## Overview

The Smart ATS application:
- **Extracts text** from uploaded PDF resumes.
- **Evaluates resumes** against a given job description using the Gemini AI model.
- **Outputs structured JSON** containing:
  - **JD Match:** The percentage match between the resume and job description.
  - **MissingKeywords:** A list of keywords missing from the resume.
  - **Profile Summary:** A summary of the candidate's profile.
  - **Resume Improvements:** Detailed suggestions to improve the resume.

## Features

- **PDF Parsing:** Automatically reads and extracts text from PDF files.
- **AI-Powered Evaluation:** Uses Google's Gemini-1.5-pro model for a professional ATS evaluation.
- **Strict JSON Output:** The prompt enforces a JSON format ensuring consistency.
- **Interactive UI:** Utilizes Streamlit components such as progress bars and dynamic columns to display results.

## Requirements

- Python 3.7+
- Required Python libraries:
  - [Streamlit](https://streamlit.io/)
  - [google-generativeai](https://pypi.org/project/google-generativeai/)
  - [PyPDF2](https://pypi.org/project/PyPDF2/)
  - [python-dotenv](https://pypi.org/project/python-dotenv/)
  - Built-in modules: `json`, `re`, `os`

You can install the necessary libraries using pip:

```bash
pip install streamlit google-generativeai PyPDF2 python-dotenv
