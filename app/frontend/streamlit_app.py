import streamlit as st

st.title("Welcome to Multiplatform-Post-Analyzer")

url = st.text_input("Paste the link below.")

dropdown = st.selectbox(
    "Which paltform content would you like to analyze?",
    ("Youtube", "X", "LinkedIn"),
    placeholder="Select the platform..."
)

st.button("Analyze")
