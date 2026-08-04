import os
import base64
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

# -----------------------------
# Load Environment Variables
# -----------------------------
load_dotenv()

# -----------------------------
# Streamlit Page Config
# -----------------------------
st.set_page_config(
    page_title="Email Bot",
    page_icon="📧",
    layout="wide"
)

# -----------------------------
# Background Image
# -----------------------------
BASE_DIR = Path(__file__).parent
image_path = BASE_DIR / "image.png"

def get_base64(file):
    with open(file, "rb") as f:
        return base64.b64encode(f.read()).decode()

if image_path.exists():
    img = get_base64(image_path)

    st.markdown(
        f"""
        <style>

        .stApp {{
            background-image: url("data:image/png;base64,{img}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}

        [data-testid="stHeader"] {{
            background: rgba(0,0,0,0);
        }}

        .block-container {{
            background: rgba(255,255,255,0.88);
            padding: 2rem;
            border-radius: 20px;
        }}

        </style>
        """,
        unsafe_allow_html=True,
    )

# -----------------------------
# Title
# -----------------------------
st.title("📧 AI Email Generator")
st.write("Generate professional emails using Groq AI.")

# -----------------------------
# Read API Key
# -----------------------------
groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key:
    st.error("❌ GROQ_API_KEY not found.")
    st.info("Please add your API key in the .env file.")
    st.stop()

# -----------------------------
# User Input
# -----------------------------
question = st.text_area(
    "Enter your email request",
    height=180,
    placeholder="Example: Write a leave application email."
)

# -----------------------------
# Generate Button
# -----------------------------
if st.button("🚀 Generate Email"):

    if question.strip() == "":
        st.warning("Please enter your request.")
        st.stop()

    try:

        llm = ChatGroq(
            api_key=groq_api_key,
            model="llama-3.3-70b-versatile",
            temperature=0.3,
        )

        prompt = ChatPromptTemplate.from_template(
            """
You are an expert Email Writing Assistant.

You only answer email-related questions.

If the user asks something unrelated, reply exactly:

Sorry, I can answer only email-related questions.

User Request:
{question}

Generate the response in this format:

## 📧 Email Subject

## ✉️ Email Body

## 📢 Recommended Call to Action

## 🔐 Security Recommendations (if applicable)

## ✅ Professional Closing
"""
        )

        chain = prompt | llm

        response = chain.invoke(
            {
                "question": question
            }
        )

        st.success("✅ Email Generated Successfully!")

        st.markdown(response.content)

    except Exception as e:
        st.error(f"❌ {str(e)}")