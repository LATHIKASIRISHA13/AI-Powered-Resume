# AI-Powered Resume & Cover Letter Generator
# Tech: Python + Streamlit + Ollama (tinyllama – low RAM)

import streamlit as st
import requests

st.set_page_config(
    page_title="AI Resume and Cover Letter Generator",
    layout="centered"
)

st.title("AI-Powered Resume and Cover Letter Generator")

# ---------------- UI ----------------
name = st.text_input("Full Name")
role = st.text_input("Target Job Role")
skills = st.text_area("Skills (comma separated)")
experience = st.text_area("Experience Summary")
company = st.text_input("Company Name (for Cover Letter)")

option = st.selectbox("Generate", ["Resume", "Cover Letter"])

# ---------------- LLM FUNCTION ----------------
def generate_content(prompt):
    try:
        res = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "tinyllama:latest",
                "prompt": prompt,
                "stream": False
            }
        )
        data = res.json()
        return data["response"]
    except Exception as e:
        return f"Error: {e}"

# ---------------- BUTTON ACTION ----------------
if st.button("Generate"):

    if option == "Resume":
        prompt = f"""
You are an expert HR resume writer.

Create a PROFESSIONAL, ATS-FRIENDLY RESUME in clean format.

Use EXACTLY this structure:

NAME
{name}

TARGET ROLE
{role}

PROFESSIONAL SUMMARY
Write 2–3 lines suitable for a fresher.

SKILLS
- Convert these into bullet points: {skills}

EXPERIENCE
- Write points based on this: {experience}

EDUCATION
- B.Tech in Computer Science (Expected 2026)

PROJECTS
- Mention 1–2 relevant academic or technical projects.

Use proper headings and bullet points.
"""
    else:
        prompt = f"""
You are a professional HR writer.

Write a FORMAL COVER LETTER with proper format.

Name: {name}
Target Role: {role}
Company: {company}
Skills: {skills}
Experience: {experience}

Structure:
- Introduction
- Skills & Experience
- Why this company
- Closing

Keep it professional and concise.
"""

    with st.spinner("Generating..."):
        output = generate_content(prompt)

    st.subheader("Generated Output")
    st.markdown(output)
