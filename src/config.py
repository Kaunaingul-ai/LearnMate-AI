import os
from dotenv import load_dotenv

# Load local environment variables
load_dotenv()

# Read Gemini API key from local environment
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Fallback to Streamlit Cloud Secrets
if not GEMINI_API_KEY:
    try:
        import streamlit as st
        GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY")
    except Exception:
        pass

# Remove accidental whitespace
if GEMINI_API_KEY:
    GEMINI_API_KEY = GEMINI_API_KEY.strip()

# Main Gemini model
GEMINI_MODEL = "gemini-3.5-flash-lite"

# Validate configuration
if not GEMINI_API_KEY:
    raise ValueError(
        "GEMINI_API_KEY was not found. "
        "Configure it in your local .env or Streamlit Secrets."
    )