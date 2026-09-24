import os
from dotenv import load_dotenv

# Load variables from the local .env file
load_dotenv()

# Gemini API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Main Gemini model used by LearnMate AI
GEMINI_MODEL = "gemini-3.5-flash-lite"

# Validate required configuration
if not GEMINI_API_KEY:
    raise ValueError(
        "GEMINI_API_KEY was not found. "
        "Please add it to your local .env file."
    )