from dotenv import load_dotenv

load_dotenv()

import streamlit as st
import os
import io
import base64
from PIL import Image
import pdf2image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(prompt,pdf_content,jd):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([prompt,pdf_content[0],jd])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        # Convert the PDF to image
        images = pdf2image.convert_from_bytes(uploaded_file.read())

        first_page = images[0]

        # Convert to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format="JPEG")
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()
            }
        ]

        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")


## Streamlit App

st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System")
jd=st.text_area("Job Description: ",key="input")
uploaded_file = st.file_uploader("Upload your resume (PDF)...", type=["PDF"])

submit1 = st.button("Tell Me About the Resume")

submit2 = st.button("Percentage Match")

input_prompt_1 = """
You are an experienced Technical Human Resource Manager. Your task is to review the provided resume against the job description for the position in question. In your professional evaluation, please assess whether the candidate's profile aligns with the role requirements.

1) Alignment Check: Analyze the candidate's skills, experience, and qualifications against the key requirements and responsibilities outlined in the job description.

2) Strengths Identification: Highlight the strengths of the applicant in relation to the specified job requirements. Focus on areas where the candidate excels, such as relevant experience, specific skills, or notable achievements that are particularly relevant to the job.

3) Weaknesses and Areas for Development: Identify any weaknesses or gaps in the candidate's profile. Discuss areas where the applicant's experience or skills might not align perfectly with the job requirements and suggest potential areas for development.

4) Overall Recommendation: Provide a summarized recommendation on the suitability of the candidate for the role based on your analysis. Include any reservations or conditions that might apply.

Your evaluation should be objective, detailed, and provide a balanced view of the candidate's potential fit for the role, considering both the requirements of the job and the strengths and weaknesses of the applicant.
"""

input_prompt_2 = """
Assume the role of a highly skilled ATS (Applicant Tracking System) scanner with a broad understanding of various industries and in-depth knowledge of ATS functionalities. Your task is to conduct a thorough evaluation of the resume against the provided job description, applicable to any job field. Present your findings in the following structured manner:

1) Match Percentage: First, calculate and present the match percentage between the resume and the job description. This percentage should reflect the extent to which the candidate’s skills, experiences, and qualifications align with the job requirements outlined in the description.

2) Keyword Gap Analysis: Next, perform a keyword gap analysis. Identify and list the crucial keywords, skills, and qualifications that are mentioned in the job description but are missing from the resume. This part of the evaluation should focus on industry-specific terminologies, technical skills, and other critical competencies that are essential for the role.

3) Final Assessment and Recommendations: Conclude with your final thoughts regarding the candidate’s suitability for the position. Provide insights on the overall alignment of the candidate's profile with the job's expectations. Include suggestions for the candidate on how to refine their resume to better meet the scanning criteria of ATS systems for the specific job field.

Ensure that your evaluation is detailed, objective, and provides a comprehensive assessment of the resume’s alignment with the job description, using the advanced scanning capabilities of an ATS.
"""

if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt_1,pdf_content,jd)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload the resume")

if submit2:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt_2,pdf_content,jd)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload the resume")



    


