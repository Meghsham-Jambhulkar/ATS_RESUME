import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import json
import re

# Load environment variables
load_dotenv()

# Configure Streamlit page settings
st.set_page_config(
    page_title="Smart ATS",
    page_icon="👨‍💼",
    layout="centered",
)

generation_config = {
    "temperature": 0.4,
    "top_p": 1,
    "top_k": 32,
    "max_output_tokens": 4096,
}

# Function to configure Gemini AI model with the provided API key
def configure_gemini_api(api_key):
    genai.configure(api_key=api_key)

# Configure Gemini AI model with the provided API key
API_KEY = "____YOUR_API_KEY____"  # Replace with your actual API key
configure_gemini_api(API_KEY)

# Function to get response from Gemini AI
def get_gemini_response(input_text):
    model = genai.GenerativeModel(
        model_name="gemini-1.5-pro",
        generation_config=generation_config
    )
    response = model.generate_content(input_text)
    return response.text

# Function to extract text from uploaded PDF file
def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page_obj = reader.pages[page]
        text += str(page_obj.extract_text())
    return text

# Prompt Template with strict JSON instructions and escaped curly braces for literal output
input_prompt = """
You are an expert ATS evaluator. Evaluate the resume below against the job description and output ONLY a single JSON string with no extra text. The JSON must follow this format EXACTLY:

{{"JD Match": "<percentage string>", "MissingKeywords": ["<keyword1>", "<keyword2>", ...], "Profile Summary": "<string>", "Resume Improvements": "<string>"}}

Do not output any explanations, comments, or additional text.

Resume: {text}
Job Description: {jd}
"""

## Streamlit app
st.title("Resume Matcher _ATS_")
jd = st.text_area("Paste the Job Description")

if not jd:
    st.warning("Please enter a Job Description")

uploaded_file = st.file_uploader("Upload Your Resume", type="pdf", help="Please upload the PDF")

submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        text = input_pdf_text(uploaded_file)
        # Generate the response using the formatted prompt
        response = get_gemini_response(input_prompt.format(text=text, jd=jd))
        
        # st.subheader("Raw Response:")
        # st.write(response)
        
        # Use regex to extract JSON part from the response
        json_pattern = r"\{.*\}"
        match = re.search(json_pattern, response, re.DOTALL)
        if match:
            json_str = match.group(0)
        else:
            json_str = response  # Fallback if no match is found
        
        # st.subheader("Extracted JSON String:")
        # st.write(json_str)
        
        st.subheader("Parsed Response:")
        try:
            parsed_response = json.loads(json_str)
            percent_match = parsed_response['JD Match']
            st.write(f"**JD Match:** {percent_match}")
            st.progress(int(round(float(parsed_response['JD Match'].replace("%", "")))) / 100)
            
            missing_keywords = parsed_response['MissingKeywords']
            if missing_keywords:
                st.write("**Missing Keywords:**")
                row1 = st.columns(1)
                for keyword in missing_keywords:
                    for col in row1:
                        tile = col.container()
                        tile.write(f"{keyword}")
            
            st.subheader("**Profile Summary:**")
            st.write(parsed_response['Profile Summary'])
            st.write("\n")
            st.subheader("**Resume Improvements:**")
            st.write(parsed_response['Resume Improvements'])
            
        except json.decoder.JSONDecodeError:
            st.error("Failed to decode JSON after extraction. Please check the raw response and extracted JSON string above for debugging.")
