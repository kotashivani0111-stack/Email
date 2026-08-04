import os
import base64
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from groq import Groq
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

# ----------------------------
# Load Environment Variables
# ----------------------------
load_dotenv()

# ----------------------------
# Streamlit Page Config
# ----------------------------
st.set_page_config(
    page_title="Email Bot",
    page_icon="📧",
    layout="wide"
)

# ----------------------------
# Background Image
# ----------------------------
BASE_DIR = Path(__file__).parent
image_path = BASE_DIR / "image.png"

def get_base64(image_file):
    with open(image_file, "rb") as f:
        return base64.b64encode(f.read()).decode()

if image_path.exists():
    img = get_base64(image_path)

    page_bg = f"""
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
        padding-top: 2rem;
        padding-bottom: 2rem;
        background: rgba(255,255,255,0.88);
        border-radius: 18px;
    }}

    </style>
    """

    st.markdown(page_bg, unsafe_allow_html=True)

# ----------------------------
# Title
# ----------------------------
st.title("📧 Email Bot")
st.write("Generate professional email templates using AI.")

# ----------------------------
# User Input
# ----------------------------
question = st.text_area(
    "Enter your email request",
    placeholder="Example: Draft an email informing employees about a phishing attack."
)

# ----------------------------
# Generate Button
# ----------------------------
if st.button("🚀 Generate Email"):

    if not question.strip():
        st.warning("Please enter your request.")
        st.stop()

    try:

        # Load API Key
        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            st.error("GROQ_API_KEY not found in .env file.")
            st.stop()

        llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0.3,
            api_key=api_key
        )

        prompt = ChatPromptTemplate.from_template(
            """
You are an Email Expert.

You ONLY answer email-related requests.

Supported topics:
- Employment Letter
- Offer Letter
- Appointment Letter
- Resignation Email
- Leave Application
- Professional Email
- Business Email
- Complaint Email
- Appreciation Email
- Invitation Email
- Reminder Email
- Meeting Email
- Follow-up Email
- Phishing Alert Email
- Password Reset Email
- Data Breach Notification
- Incident Report Email
- Security Awareness Email
- Malware Detection Notification
- Zero Trust Announcement
- Monthly Cybersecurity Newsletter

If the user's request is NOT related to writing an email, reply EXACTLY:

Sorry, I can answer only email-related questions.

Question:
{question}

If it is an email request, generate:

## 📧 Email Subject

## ✉️ Email Body

## 📢 Recommended Call to Action

## 🔐 Security Recommendations

## ✅ Professional Closing
"""
        )

        chain = prompt | llm

        response = chain.invoke({"question": question})

        answer = response.content.strip()

        # Display success only if an email is generated
        if "## 📧 Email Subject" in answer:
            st.success("✅ Email Generated Successfully!")
            st.markdown(answer)
        else:
            st.warning("Sorry, I can answer only email-related questions.")

    except Exception as e:
        st.error(f"❌ Error: {e}")
