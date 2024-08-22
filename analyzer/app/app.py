import streamlit as st
import requests
from analyzer.model.model_preprocessing import clean_comments


st.title("Welcome to Multiplatform-Post-Analyzer")

url = st.text_input("Paste the link below.")

dropdown = st.selectbox(
    "Which platform content would you like to analyze?",
    ("Youtube", "Reddit"),
    placeholder="Select the platform..."
)

if st.button("Analyze"):
    elements = {
        'url': url,
        'platform': dropdown
    }

    if dropdown == "Youtube":
        response = requests.post('http://127.0.0.1:8000/scrape/youtube', json=elements).json()
        with open('youtube_comments.txt', 'w') as comments_file:
            for i in response:
                comments_file.write(f"{i}\n")
        comments = clean_comments("youtube")
        with open('clean_youtube_comments.txt', 'w') as file:
            for i in comments:
                file.write(f"{i}\n")
    if dropdown == "Reddit":
        response = requests.post('http://127.0.0.1:8000/scrape/reddit', json=elements).json()
        with open("reddit_comments.txt", 'w') as file:
            for i in response:
                file.write(f"{i}\n")
        comments = clean_comments("reddit")
        with open('clean_reddit_comments.txt', 'w') as file:
            for i in comments:
                file.write(f"{i}\n")
