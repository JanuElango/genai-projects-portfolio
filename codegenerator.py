import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# -------------------------------
# Helper Function (FIXED POSITION)
# -------------------------------
def get_extension(language):
    if language == "Python":
        return "py"
    elif language == "Java":
        return "java"
    else:
        return "cs"

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(
    page_title="AI Code Generator",
    page_icon="💻",
    layout="wide"
)

# -------------------------------
# Header
# -------------------------------
st.markdown("""
    <h1 style='text-align: center;'>💻 AI Code Generator</h1>
    <p style='text-align: center; color: gray;'>
    Generate production-ready code in Python, Java, or .NET
    </p>
""", unsafe_allow_html=True)

# -------------------------------
# LLM Setup
# -------------------------------
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.3
)

template = """
You are an expert software developer.

Generate clean, efficient, and production-ready {language} code.

Requirements:
{requirements}

Instructions:
- Add comments
- Follow best practices
- Keep code readable
- Include example usage if needed

Code:
"""

prompt = PromptTemplate(
    input_variables=["language", "requirements"],
    template=template
)

chain = LLMChain(llm=llm, prompt=prompt)

# -------------------------------
# Layout
# -------------------------------
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("⚙️ Configuration")

    language = st.selectbox(
        "Select Language",
        ["Python", "Java", ".NET"]
    )

    requirements = st.text_area(
        "Enter your requirement",
        placeholder="Example: Create a REST API for user login with validation",
        height=200
    )

    generate = st.button("🚀 Generate Code")

with col2:
    st.subheader("📄 Generated Code")

    if generate:
        if not requirements:
            st.warning("Please enter requirements")
        else:
            with st.spinner("Generating code..."):
                result = chain.run({
                    "language": language,
                    "requirements": requirements
                })

            st.code(result, language.lower())

            # Download button
            st.download_button(
                label="⬇️ Download Code",
                data=result,
                file_name=f"generated_code.{get_extension(language)}",
                mime="text/plain"
            )