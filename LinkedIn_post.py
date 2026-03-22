import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(
    page_title="LinkedIn Post Generator",
    page_icon="💼",
    layout="wide"
)

st.title("💼 LinkedIn Post Generator")
st.caption("Create engaging, professional LinkedIn posts using AI")

# -------------------------------
# LLM Setup
# -------------------------------
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.7
)

template = """
You are a professional LinkedIn content creator.

Create a high-quality LinkedIn post based on:

Topic: {topic}
Tone: {tone}

Instructions:
- Start with a strong hook
- Keep it engaging and human
- Use short paragraphs
- Add emojis where appropriate
- Include a call-to-action
- Keep it under 150-200 words

LinkedIn Post:
"""

prompt = PromptTemplate(
    input_variables=["topic", "tone"],
    template=template
)

chain = LLMChain(llm=llm, prompt=prompt)

# -------------------------------
# UI Layout
# -------------------------------
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("⚙️ Configuration")

    topic = st.text_area(
        "Enter Topic",
        placeholder="Example: My journey learning GenAI",
        height=150
    )

    tone = st.selectbox(
        "Select Tone",
        ["Professional", "Inspirational", "Casual", "Storytelling"]
    )

    generate = st.button("🚀 Generate Post")

with col2:
    st.subheader("📄 Generated Post")

    if generate:
        if not topic:
            st.warning("Please enter a topic")
        else:
            with st.spinner("Generating..."):
                result = chain.run({
                    "topic": topic,
                    "tone": tone
                })

            st.write(result)

            st.download_button(
                "⬇️ Download Post",
                result,
                file_name="linkedin_post.txt"
            )