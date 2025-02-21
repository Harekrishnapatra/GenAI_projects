import streamlit as st
import pdfplumber
import google.generativeai as genai
import re

# Configure Gemini API
genai.configure(api_key="use ur own api key")

# Function to extract text from a PDF
def extract_text_from_pdf(pdf_file):
    with pdfplumber.open(pdf_file) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() + "\n"
        return text.strip()

# Function to generate AI-based resume suggestions
def generate_suggestions(resume_text, job_role):
    prompt = f"""
    Analyze the following resume and provide suggestions for improvement.
    Also, generate three optimized bullet points based on the job role '{job_role}'.
    Resume:
    {resume_text}
    """
    model = genai.GenerativeModel("gemini-2.0-flash")  # Using Gemini 2.0 pro
    response = model.generate_content(prompt)
    return response.text

# Function to calculate ATS score
def calculate_ats_score(resume_text, job_role):
    keywords = ["Python", "SQL", "Machine Learning", "Data Analysis", "Communication", "Problem-Solving", "Leadership"]  # Sample keywords
    matched_keywords = [kw for kw in keywords if re.search(rf'\b{kw}\b', resume_text, re.IGNORECASE)]
    score = (len(matched_keywords) / len(keywords)) * 100
    return round(score, 2)

# Streamlit UI Design
st.set_page_config(page_title="AI-Powered Resume Analyzer", layout="wide")
st.markdown(
    """
    <style>
        .main { background-color: #f5f5f5; }
        .stTextArea textarea { font-size: 16px; }
        .stButton button { background-color: #007bff; color: white; border-radius: 8px; }
        .stFileUploader label { font-size: 16px; font-weight: bold; }
        .stTextInput input { font-size: 16px; }
    </style>
    """, unsafe_allow_html=True
)

st.markdown("## 🌟 AI-Powered Resume Analyzer & Enhancer 📝")
st.write("Upload your resume and get AI-driven suggestions for improvement!")

# Upload and Input Section
uploaded_file = st.file_uploader("📂 Upload your Resume (PDF)", type=["pdf"])
job_role = st.text_input("🎯 Enter your Target Job Role")

if uploaded_file is not None and job_role:
    st.markdown("---")
    st.subheader("📄 Extracted Resume Content")
    resume_text = extract_text_from_pdf(uploaded_file)
    st.text_area("Your Resume:", resume_text, height=300)
    
    # Generate suggestions
    if st.button("🚀 Analyze Resume"):
        with st.spinner("🔍 Analyzing..."):
            suggestions = generate_suggestions(resume_text, job_role)
            ats_score = calculate_ats_score(resume_text, job_role)
            st.markdown("---")
            st.subheader("✨ AI Suggestions")
            st.write(suggestions)
            st.subheader("📊 ATS Compatibility Score")
            st.metric(label="Your ATS Score", value=f"{ats_score}%")
            st.success("✅ Analysis Completed!")
