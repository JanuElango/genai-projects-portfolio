import streamlit as st
import PyPDF2
import docx
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# -------------------------------
# File Readers
# -------------------------------
def read_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def read_docx(file):
    doc = docx.Document(file)
    return "\n".join([p.text for p in doc.paragraphs])

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(page_title="Resume-JD Matcher", layout="wide")
st.title("📄 Resume vs Job Description Matcher")

# -------------------------------
# LLM Setup
# -------------------------------
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)

template = """
You are an expert HR and ATS system.

Analyze the match between a resume and a job description.

Resume:
{resume}

Job Description:
{jd}

Provide output in this format:

Match Score: (percentage)

Matching Skills:
- ...

Missing Skills:
- ...

Suggestions to Improve:
- ...
"""

prompt = PromptTemplate(
    input_variables=["resume", "jd"],
    template=template
)

chain = LLMChain(llm=llm, prompt=prompt)

# -------------------------------
# UI Layout
# -------------------------------
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("📥 Inputs")

    uploaded_file = st.file_uploader("Upload Resume (PDF/DOCX)", type=["pdf", "docx"])
    jd = st.text_area("Paste Job Description", height=200)

    analyze = st.button("🔍 Analyze Match")

# -------------------------------
# Process Resume
# -------------------------------
resume_text = ""

if uploaded_file:
    if uploaded_file.type == "application/pdf":
        resume_text = read_pdf(uploaded_file)
    else:
        resume_text = read_docx(uploaded_file)

    st.success("Resume uploaded successfully")

# -------------------------------
# Output
# -------------------------------
with col2:
    st.subheader("📊 Analysis Result")

    if analyze:
        if not resume_text or not jd:
            st.warning("Upload resume and enter job description")
        else:
            with st.spinner("Analyzing..."):
                result = chain.run({
                    "resume": resume_text[:4000],
                    "jd": jd
                })

            st.write(result)

            st.download_button(
                "⬇️ Download Report",
                result,
                file_name="match_report.txt"
            )