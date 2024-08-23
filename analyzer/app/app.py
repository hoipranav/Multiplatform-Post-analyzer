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


def get_comments(platform:str):
    """Calls the post method according to the respective platform given as input"""
    response = requests.post("http://127.0.0.1:8000/scrape/{0}".format(platform), json=elements).json()
    with open(f"{platform}_comments.txt", 'w') as comments_file:
        for i in response:
            comments_file.write(f"{i}\n")
    comments = clean_comments(platform)
    with open(f"clean_{platform}_comments.txt", 'w') as file:
        for i in comments:
            file.write(f"{i}\n")


if st.button("Analyze"):
    elements = {
        'url': url,
        'platform': dropdown
    }
    get_comments(elements['platform'].lower())
