import streamlit as st
import requests

st.title("Welcome to Multiplatform-Post-Analyzer")

url = st.text_input("Paste the link below.")

dropdown = st.selectbox(
    "Which paltform content would you like to analyze?",
    ("Youtube", "X", "LinkedIn"),
    placeholder="Select the platform..."
)

if st.button("Analyze"):
    elements = {
        'url': url,
        'platform': dropdown
    }

    if dropdown == "Youtube":
        response = requests.post('http://127.0.0.1:8000/scrape/youtube', json=elements).json()
        print(len(response))
    if dropdown == "X":
        response = requests.post('http://127.0.0.1:8000/scrape/x', json=elements).json()
        print(response)
    if dropdown == "LinkedIn":
        response = requests.post('http://127.0.0.1:8000/scrape/linkedIn', json=elements).json()
        for i in response:
            print(i)
