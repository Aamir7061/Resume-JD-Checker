import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
import pdfplumber
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content(input)
    return response.text


def input_pdf_text(uploaded_file):
    # Creating a PDF reader object
    with pdfplumber.open(uploaded_file) as pdf:
        text = ""
        # Iterating over each page in the PDF
        for page in pdf.pages:
            # Extracting text from each page and appending to the 'text' variable
            text += page.extract_text()
    return text

input_promt="""
Hey Act like a skilled or very experiance ATS(Application Tracking System)
with a deep understanding of the Technology field like software engineering, data science, data analyst and data cientist. Your task is to evaluate the resume based on the given job description.
You must consider the job market is very competitive and you should provide best assistance for improving the resumes. Assign the percentage Matching based 
On Jd and
The Missing keywords with high accuracy
Resume:{text}
Description:{jd}
I want the response in one single string having the structure
{{"JD MAtch":"%","MissingKeywords:[]","Profile Summary":""}}
"""

st.title('Resume-JD-Checker')
st.text("Improve Your Resume ATS")
jd=st.text_area('Paste the Job Description')
uploaded_file=st.file_uploader("Upload Your Resume",type='pdf',help='Please upload the pdf')

submit=st.button("Submit")

if submit:
    if uploaded_file is not None:
        text=input_pdf_text(uploaded_file)
        response=get_gemini_response(input_promt)
        st.subheader(response)
