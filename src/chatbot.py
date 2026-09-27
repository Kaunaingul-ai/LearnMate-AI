import time
from google import genai

from src.config import GEMINI_API_KEY, GEMINI_MODEL
from src.prompts import SYSTEM_PROMPT
from src.rag import LearnMateRAG


class LearnMateChatbot:
    """
    Core LearnMate AI chatbot.

    Features:
    - Gemini Generative AI
    - Multi-turn conversation memory
    - Hugging Face semantic retrieval
    - Retrieval-Augmented Generation (RAG)
    - Retrieved-topic tracking
    - Graceful API error handling
    """

    def __init__(self):
        self.client = genai.Client(api_key=GEMINI_API_KEY)

        # Conversation memory
        self.previous_interaction_id = None

        # Semantic retrieval system
        self.rag = LearnMateRAG()

        # Stores retrieved topics for the latest question
        self.last_retrieved_topics = []

    def reset_conversation(self):
        """
        Start a fresh conversation.
        """
        self.previous_interaction_id = None
        self.last_retrieved_topics = []

    def ask(self, user_question, max_retries=3):
        """
        Send a question to LearnMate AI and return
        a context-aware response.
        """

        # Validate input
        if not user_question or not user_question.strip():
            self.last_retrieved_topics = []
            return "Please enter a valid question."

        # -------------------------------------------------
        # Semantic Retrieval
        # -------------------------------------------------
        retrieved_results = self.rag.retrieve(
            user_question,
            top_k=3
        )

        self.last_retrieved_topics = [
            item["topic"] for item in retrieved_results
        ]

        retrieved_context = "\n\n".join(
            [
                f"Topic: {item['topic']}\n"
                f"Content: {item['content']}"
                for item in retrieved_results
            ]
        )

        # -------------------------------------------------
        # Gemini Generation
        # -------------------------------------------------
        for attempt in range(1, max_retries + 1):

            try:
                # First message
                if self.previous_interaction_id is None:

                    interaction = self.client.interactions.create(
                        model=GEMINI_MODEL,
                        input=f"""
{SYSTEM_PROMPT}

Use the following retrieved knowledge when it is relevant
to the user's question.

The retrieved knowledge is supporting context.
If it is incomplete or irrelevant, use your general
reasoning while remaining accurate and within
LearnMate AI's educational scope.

Retrieved Knowledge:
{retrieved_context}

User Question:
{user_question}
"""
                    )

                # Follow-up message
                else:

                    interaction = self.client.interactions.create(
                        model=GEMINI_MODEL,
                        input=f"""
Use the following newly retrieved knowledge when relevant.

Retrieved Knowledge:
{retrieved_context}

User Question:
{user_question}
""",
                        previous_interaction_id=self.previous_interaction_id
                    )

                # Update conversation memory
                self.previous_interaction_id = interaction.id

                return interaction.output_text

            except Exception as e:
                error_message = str(e).lower()
                print(f"LEARNMATE ERROR: {type(e).__name__}: {e}")s

                # Temporary service problem
                if (
                    "503" in error_message
                    or "service_unavailable" in error_message
                    or "high demand" in error_message
                ):
                    if attempt < max_retries:
                        time.sleep(5)
                        continue

                    return (
                        "LearnMate AI is temporarily unavailable because "
                        "the AI service is experiencing high demand. "
                        "Please try again shortly."
                    )

                # API rate limit
                if (
                    "429" in error_message
                    or "rate limit" in error_message
                    or "resource_exhausted" in error_message
                    or "too_many_requests" in error_message
                ):
                    return (
                        "LearnMate AI has reached the current API usage limit. "
                        "Please try again later."
                    )

                # Unexpected error
                return (
                    "LearnMate AI encountered an unexpected error. "
                    "Please try again."
                )