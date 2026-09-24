import streamlit as st

from src.chatbot import LearnMateChatbot


# -------------------------------------------------
# Page Configuration
# -------------------------------------------------
st.set_page_config(
    page_title="LearnMate AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# -------------------------------------------------
# Custom Styling
# -------------------------------------------------
st.markdown(
    """
    <style>
        .main-title {
            font-size: 2.6rem;
            font-weight: 700;
            margin-bottom: 0.2rem;
        }

        .subtitle {
            font-size: 1.05rem;
            color: #6b7280;
            margin-bottom: 1.5rem;
        }

        .welcome-card {
            padding: 1.2rem 1.4rem;
            border: 1px solid #e5e7eb;
            border-radius: 16px;
            background-color: rgba(250, 250, 250, 0.7);
            margin-bottom: 1.2rem;
        }

        .feature-box {
            padding: 0.8rem 1rem;
            border-radius: 12px;
            border: 1px solid #e5e7eb;
            margin-bottom: 0.7rem;
        }

        .footer {
            text-align: center;
            color: #6b7280;
            font-size: 0.85rem;
            padding-top: 2rem;
        }
    </style>
    """,
    unsafe_allow_html=True
)


# -------------------------------------------------
# Session State
# -------------------------------------------------
if "chatbot" not in st.session_state:
    st.session_state.chatbot = LearnMateChatbot()

if "messages" not in st.session_state:
    st.session_state.messages = []


# -------------------------------------------------
# Sidebar
# -------------------------------------------------
with st.sidebar:
    st.title("🤖 LearnMate AI")

    st.markdown(
        """
        **LearnMate AI** is a Generative AI learning and career assistant
        designed for students exploring Artificial Intelligence,
        Machine Learning, Python, Data Science, NLP, and related fields.
        """
    )

    st.divider()

    if st.button("🆕 New Chat", use_container_width=True):
        st.session_state.chatbot.reset_conversation()
        st.session_state.messages = []
        st.rerun()

    st.divider()

    st.subheader("✨ Features")
    st.markdown(
        """
        - Generative AI responses
        - Multi-turn conversation memory
        - Hugging Face semantic retrieval
        - Local knowledge-base RAG
        - AI and ML concept explanations
        - Coding guidance
        - Project suggestions
        - Career learning support
        """
    )

    st.subheader("🧰 Tech Stack")
    st.markdown(
        """
        - **Python**
        - **Gemini API**
        - **Hugging Face Sentence Transformers**
        - **Scikit-learn**
        - **Streamlit**
        - **JSON Knowledge Base**
        """
    )

    st.subheader("📚 Knowledge Areas")
    st.markdown(
        """
        - Artificial Intelligence
        - Machine Learning
        - Deep Learning
        - Natural Language Processing
        - Computer Vision
        - Python
        - Data Science
        - AI Career Guidance
        """
    )


# -------------------------------------------------
# Main Header
# -------------------------------------------------
st.markdown(
    '<div class="main-title">🤖 LearnMate AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Your AI Learning & Career Assistant</div>',
    unsafe_allow_html=True
)


# -------------------------------------------------
# Welcome Section
# -------------------------------------------------
if not st.session_state.messages:
    st.markdown(
        """
        <div class="welcome-card">
            <h3>Welcome to LearnMate AI 👋</h3>
            <p>
                Ask questions about Artificial Intelligence, Machine Learning,
                Python, NLP, Computer Vision, projects, or AI career paths.
            </p>
            <p>
                LearnMate combines Generative AI with semantic retrieval from
                a local knowledge base to provide more context-aware responses.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            <div class="feature-box">
                <b>📘 Learn Concepts</b><br>
                Get beginner-friendly explanations of AI and ML topics.
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            """
            <div class="feature-box">
                <b>💻 Get Coding Help</b><br>
                Understand Python and common AI development workflows.
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            """
            <div class="feature-box">
                <b>🚀 Build Your Career</b><br>
                Explore project ideas, roadmaps, and AI career guidance.
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("### Try asking:")
    st.markdown(
        """
        - What is overfitting in machine learning?
        - Explain NLP in simple words.
        - Suggest a beginner AI project.
        - What skills should I learn for an AI internship?
        """
    )


# -------------------------------------------------
# Display Conversation History
# -------------------------------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        if (
            message["role"] == "assistant"
            and message.get("retrieved_topics")
        ):
            with st.expander("🔎 Retrieved Knowledge"):
                for topic in message["retrieved_topics"]:
                    st.markdown(f"- {topic}")


# -------------------------------------------------
# Chat Input
# -------------------------------------------------
user_prompt = st.chat_input(
    "Ask LearnMate about AI, Machine Learning, Python, projects, or careers..."
)

if user_prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(user_prompt)

    with st.chat_message("assistant"):
        with st.spinner("LearnMate is thinking..."):
            response = st.session_state.chatbot.ask(user_prompt)

        st.markdown(response)

        retrieved_topics = (
            st.session_state.chatbot.last_retrieved_topics
        )

        if retrieved_topics:
            with st.expander("🔎 Retrieved Knowledge"):
                for topic in retrieved_topics:
                    st.markdown(f"- {topic}")

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response,
            "retrieved_topics": retrieved_topics
        }
    )


# -------------------------------------------------
# Footer
# -------------------------------------------------
st.markdown(
    """
    <div class="footer">
        LearnMate AI • Generative AI + Semantic Retrieval + RAG
    </div>
    """,
    unsafe_allow_html=True
)