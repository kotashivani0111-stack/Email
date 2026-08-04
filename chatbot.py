import os
import base64
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
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
# Load Background Image
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

    [data-testid="stToolbar"] {{
        right: 2rem;
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
# Ask Button
# ----------------------------
if st.button("🚀 Generate Email"):

    if not question.strip():
        st.warning("Please enter a question.")
        st.stop()

    try:

        llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0.3,
            api_key=os.getenv("GROQ_API_KEY")
        )

        prompt = ChatPromptTemplate.from_template(
            """
You are an Email Expert.

Answer ONLY email-related requests.

Supported topics include:
- create a email template
- write a professional email
- generate email content
- create email subject lines
- provide email etiquette tips
- Phishing Alert Email
- Password Reset Email
- Data Breach Notification
- Incident Report Email
- Security Awareness Email
- Malware Detection Notification
- Zero Trust Announcement
- Monthly Cybersecurity Newsletter

If the user asks anything unrelated to email writing, reply exactly:

Sorry, I can answer only email-related questions.

Question:
{question}

Generate the response in the following format.

## 📧 Email Subject

## ✉️ Email Body

## 📢 Recommended Call to Action

## 🔐 Security Recommendations

## ✅ Professional Closing
"""
        )

        chain = prompt | llm

        response = chain.invoke(
            {"question": question}
        )

        st.success("Email Generated Successfully!")

        st.markdown(response.content)

    except Exception as e:
        st.error(f"Error: {e}")

        st.success("Email Generated Successfully!")

        st.markdown(response.content)

    except Exception as e:
        st.error(f"Error: {e}")
