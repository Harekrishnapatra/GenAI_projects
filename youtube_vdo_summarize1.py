# 📺 AI YouTube Video Summarizer (Gemini)

'''This Python script creates a **Streamlit web app** that extracts transcripts from YouTube videos and generates an AI-powered summary using **Google Gemini AI**'''

## Step-1:  Import Required Libraries
import streamlit as st
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
import os
### 🔹 Why All these required?
# streamlit → For building the interactive web app.
# google.generativeai → To use Google Gemini AI for summarization.
# youtube_transcript_api → To fetch video transcripts (subtitles).
# **os** → To securely store API keys using environment variables.

## Step-2: Set Up API Key
GOOGLE_API_KEY = os.getenv("use ur api_key_")
if not GOOGLE_API_KEY:
    st.error("API Key is missing. Set it in environment variables.")
### Why Api_key needed?
# Fetches the API key from environment variables (instead of hardcoding it).
# Shows an **error message** if the API key is missing.

## Step-3: Configure Gemini API

genai.configure(api_key=GOOGLE_API_KEY)

###  Why?
#- Configures Google Gemini AI with the API key for text generation.

## Step-4: Streamlit UI Setup

st.title("📺 AI YouTube Video Summarizer (Gemini)")
st.subheader("Enter a YouTube video link to get an AI-generated summary.")

###  Why?

#- **`st.title()`** → Adds the app title.
#- **`st.subheader()`** → Adds a subtitle to guide users.

## Step-4: User Input (YouTube Video URL)

video_url = st.text_input("YouTube Video URL")
### 🔹 Why?
#- Creates a text input field for users to enter the **YouTube video link**.


## Step-6:  Extract Video ID from URL

def get_video_id(url):
    import re
    patterns = [
        r"youtube\.com/watch\?v=([^&]+)",
        r"youtu\.be/([^?]+)",
        r"youtube\.com/embed/([^?]+)"
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None
### 🔹 Why?
#- Uses **Regular Expressions (regex)** to extract the **video ID** from different YouTube URL formats:
#  - `youtube.com/watch?v=...`
#  - `youtu.be/...`
# - `youtube.com/embed/...`
# - Returns `None` if the **URL is invalid**.

## Step-7: Fetch Transcript from YouTube

def get_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        text = " ".join([entry["text"] for entry in transcript])
        return text[:3000]  # Limit transcript to 3000 characters
    except Exception:
        return None
### 🔹 Why?
#- Fetches the **video transcript** using `YouTubeTranscriptApi`.
#- **Joins** all the transcript text into a single string.
#- **Limits to 3000 characters** to avoid exceeding Gemini’s token limit.
#- If an error occurs (e.g., no subtitles available), it **returns `None`**.

## Step-7: Generate AI Summary

def summarize_text(text):
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(f"Summarize this YouTube video transcript:\n\n{text}")
    return response.text if hasattr(response, "text") else "No summary generated."

### 🔹 Why?
#- Uses **Google Gemini AI** to generate a summary of the transcript.
#- Checks if `response.text` exists; otherwise, it returns a fallback message.


## Step-8: Process Video and Generate Summary

if st.button("Generate Summary"):
    video_id = get_video_id(video_url)
    if video_id:
        with st.spinner("Fetching transcript..."):
            transcript = get_transcript(video_id)
        if transcript:
            with st.spinner("Generating summary..."):
                summary = summarize_text(transcript)
            st.subheader("📄 AI-Generated Summary")
            st.write(summary)
        else:
            st.error("⚠️ Could not fetch the transcript. The video might not have captions enabled.")
    else:
        st.warning("⚠️ Please enter a valid YouTube URL!")

###  Why?
#1. if st.button("Generate Summary"): → Starts the process when the user clicks the button.
#2. Extracts video ID → Calls get_video_id(video_url).
#3. Fetches transcript with a **loading spinner (`st.spinner`).
#4. Generates AI summary using Gemini AI.
#5. Displays the summary or shows an error if transcript retrieval fails.


## step-9: Final Output
#This app takes a **YouTube video URL**, extracts its **transcript**, and generates an **AI-powered summary** using **Google Gemini AI**.

###  Features Used:
# **Supports various YouTube URL formats**
# **Handles errors gracefully**
# **Uses Google Gemini AI for accurate summarization**
# **Built with Streamlit for an easy-to-use interface**

