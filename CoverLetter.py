import streamlit as st
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import PyPDF2
import docx

# -------------------------------
# Functions to read files
# -------------------------------

def read_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def read_docx(file):
    doc = docx.Document(file)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

# -------------------------------
# Initialize LLM
# -------------------------------
llm = OpenAI(temperature=0.7)

template = """
You are a professional career assistant.

Write a compelling and concise cover letter based on the following details:

Resume:
{resume}

Company Name:
{company}

Job Title:
{job_title}

Instructions:
- Keep it professional and engaging
- Highlight relevant skills from resume
- Tailor it to the company and role
- Limit to 200-250 words

Cover Letter:
"""

prompt = PromptTemplate(
    input_variables=["resume", "company", "job_title"],
    template=template
)

chain = LLMChain(llm=llm, prompt=prompt)

# -------------------------------
# Streamlit UI
# -------------------------------
st.set_page_config(page_title="AI Cover Letter Generator")
st.title("📄 AI Cover Letter Generator (Upload Resume)")

uploaded_file = st.file_uploader(
    "Upload your Resume (PDF or DOCX)",
    type=["pdf", "docx"]
)

company = st.text_input("Company Name")
job_title = st.text_input("Job Title")

resume_text = ""

# Process uploaded file
if uploaded_file:
    if uploaded_file.type == "application/pdf":
        resume_text = read_pdf(uploaded_file)
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        resume_text = read_docx(uploaded_file)

    st.success("Resume uploaded and processed!")

# Generate button
if st.button("Generate Cover Letter"):
    if resume_text and company and job_title:
        with st.spinner("Generating..."):
            result = chain.run({
                "resume": resume_text,
                "company": company,
                "job_title": job_title
            })

        st.subheader("Generated Cover Letter")
        st.write(result)
    else:
        st.warning("Please upload resume and fill all fields")