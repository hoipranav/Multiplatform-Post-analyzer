import streamlit as st
import requests


def get_comments(platform: str, url: str) -> list:
    """
    Calls the post method according to the respective platform given as input

    Args:
        platform (str): The platform to scrape comments from
        url (str): The URL of the content to scrape comments from

    Returns:
        list: A list of comments scraped from the platform
    """
    response = requests.post(
        f"http://127.0.0.1:8000/scrape/{platform.lower()}",
        json={"url": url, "platform": platform}
    ).json()
    return response


if __name__ == "__main__":
    st.title("Welcome to Platform-Analyzer")

    url = st.text_input("Paste the link below.")

    dropdown = st.selectbox(
        "Which platform content would you like to analyze?",
        ("Youtube", "Reddit"),
        placeholder="Select the platform..."
    )

    if st.button("Analyze"):
        comments = get_comments(dropdown, url)
        
