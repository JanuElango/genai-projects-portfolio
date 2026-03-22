import streamlit as st
import re
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# -------------------------------
# Extract Video ID
# -------------------------------
def extract_video_id(url):
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11})", url)
    return match.group(1) if match else None

# -------------------------------
# Get Transcript (ROBUST VERSION)
# -------------------------------
def get_transcript(video_id):
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

        try:
            # Try manually created transcript
            transcript = transcript_list.find_transcript(['en'])
        except:
            # Fallback to auto-generated
            transcript = transcript_list.find_generated_transcript(['en'])

        fetched = transcript.fetch()

        text = " ".join([t['text'] for t in fetched])
        return text

    except TranscriptsDisabled:
        return "ERROR: Transcripts are disabled for this video"
    except NoTranscriptFound:
        return "ERROR: No transcript found"
    except Exception as e:
        return f"ERROR: {str(e)}"

# -------------------------------
# LLM Setup
# -------------------------------
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.5
)

template = """
You are an expert summarizer.

Summarize the following YouTube transcript in under 300 words.

Transcript:
{text}

Make it:
- Clear
- Structured
- Easy to read

Summary:
"""

prompt = PromptTemplate(
    input_variables=["text"],
    template=template
)

chain = LLMChain(llm=llm, prompt=prompt)

# -------------------------------
# UI
# -------------------------------
st.set_page_config(page_title="YouTube Summarizer")
st.title("🎥 YouTube Video Summarizer")

url = st.text_input("Enter YouTube URL")

if st.button("Generate Summary"):

    if not url:
        st.warning("Please enter a URL")
        st.stop()

    video_id = extract_video_id(url)

    if not video_id:
        st.error("Invalid YouTube URL")
        st.stop()

    st.info(f"Video ID: {video_id}")

    # Step 1: Get transcript
    with st.spinner("Fetching transcript..."):
        transcript = get_transcript(video_id)

    if transcript.startswith("ERROR"):
        st.error(transcript)
        st.info("👉 Try this working video: https://www.youtube.com/watch?v=aircAruvnKk")
        st.stop()

    st.success("Transcript fetched successfully!")

    # Step 2: Limit size (important)
    transcript = transcript[:4000]

    # Step 3: Generate summary
    with st.spinner("Generating summary..."):
        result = chain.run({"text": transcript})

    st.subheader("📄 Summary")
    st.write(result)