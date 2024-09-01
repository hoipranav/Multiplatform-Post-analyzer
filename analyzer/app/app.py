import streamlit as st
import requests


st.title("Welcome to Platform-Analyzer")

url = st.text_input("Paste the link below.")

dropdown = st.selectbox(
    "Which platform content would you like to analyze?",
    ("Youtube", "Reddit"),
    placeholder="Select the platform..."
)


def get_comments(platform:str):
    """Calls the post method according to the respective platform given as input"""
    response = requests.post("http://0.0.0.0:8081/scrape/{0}".format(platform), json=elements).json()
    # response = requests.post("{config.server.host}:81/127.0.0.1:8000/scrape/{0}".format(platform), json=elements).json()
    with open(f"{platform}_comments.txt", 'w') as comments_file:
        for i in response:
            comments_file.write(f"{i}\n")


if st.button("Analyze"):
    elements = {
        'url': url,
        'platform': dropdown
    }
    get_comments(elements['platform'].lower())
