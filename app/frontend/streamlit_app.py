import streamlit as st
import requests

st.title("Welcome to Multiplatform-Post-Analyzer")

url = st.text_input("Paste the link below.")

dropdown = st.selectbox(
    "Which paltform content would you like to analyze?",
    ("Youtube", "X", "LinkedIn"),
    placeholder="Select the platform..."
)

st.button("Analyze")

elements = {
    'url': url,
    'platform': dropdown
}

response = requests.post('http://127.0.0.1:8000/scrape', json=elements)
print(response.con)