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
    response = requests.post("http://apicontainer:8081/scrape/{0}".format(platform), json=elements).json()
    # response = requests.post("http://127.0.0.1:8000/scrape/{0}".format(platform), json=elements).json()
    with open(f"{platform}_comments.txt", 'w') as comments_file:
        try:
            for i in response:
                comments_file.write(f"{i}\n")
        except:
            print("Blank")


if st.button("Analyze"):
    elements = {
        'url': url,
        'platform': dropdown
    }
    get_comments(elements['platform'].lower())
