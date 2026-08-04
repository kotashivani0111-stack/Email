import streamlit as st
import base64
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

st.set_page_config(
    page_title="Email Bot",
    page_icon="📧",
    layout="wide"
)

# Load Image
def get_base64(image_file):
    with open(image_file, "rb") as f:
        return base64.b64encode(f.read()).decode()

img = get_base64("image.png")

# Background CSS
page_bg = f"""
<style>
.stApp {{
    background-image: url("data:image/png;base64,{img}");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}}
</style>
"""

st.markdown(page_bg, unsafe_allow_html=True)

st.title("📧 Email Bot")
st.write("Ask anything about Email 📧")

# User Input
question = st.text_area("Enter your Question...")

if st.button("Ask AI"):

    # Initialize Groq LLM
    llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.3
)

    # Prompt Template
    prompt = ChatPromptTemplate.from_template(
        """
You are an Email Expert.

Your job is to answer ONLY email-related questions.

Topics include:
- Draft an email informing users about a phishing attack.
- Write a password reset email.
- Generate a data breach notification.
- Write an incident report email.
- Generate a security awareness training email.
- Write a malware detection notification.
- Generate a Zero Trust implementation announcement.
- Write a monthly cybersecurity newsletter.

If the user asks anything outside email-related topics, reply exactly:
"Sorry, I can answer only email-related questions."

Question:
{question}

Provide:
1.Email Subject
2.Email Body
3.Recommended Call to Action
4.Security Recommendations
5.Professional Closing
"""
    )

    # Create Chain
    chain = prompt | llm

    # Get Response
    response = chain.invoke({"question": question})

    # Display Output
    st.success(response.content)