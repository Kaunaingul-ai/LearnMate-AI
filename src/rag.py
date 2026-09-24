import json
from pathlib import Path

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


class LearnMateRAG:
    """
    Lightweight semantic retrieval system for LearnMate AI.
    Uses Hugging Face sentence embeddings to find relevant
    knowledge-base entries for a user's question.
    """

    def __init__(self, knowledge_base_path="data/knowledge_base.json"):
        self.knowledge_base_path = Path(knowledge_base_path)

        # Load the local knowledge base
        with open(self.knowledge_base_path, "r", encoding="utf-8") as file:
            self.knowledge_base = json.load(file)

        # Lightweight sentence-transformer model
        self.embedding_model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )

        # Prepare text used for semantic search
        self.documents = [
            f"{item['topic']}: {item['content']}"
            for item in self.knowledge_base
        ]

        # Create embeddings once when the retriever starts
        self.document_embeddings = self.embedding_model.encode(
            self.documents,
            normalize_embeddings=True
        )

    def retrieve(self, query, top_k=3):
        """
        Returns the most semantically relevant knowledge-base entries.
        """

        query_embedding = self.embedding_model.encode(
            [query],
            normalize_embeddings=True
        )

        similarities = cosine_similarity(
            query_embedding,
            self.document_embeddings
        )[0]

        top_indices = similarities.argsort()[::-1][:top_k]

        results = []

        for index in top_indices:
            item = self.knowledge_base[index]

            results.append({
                "id": item["id"],
                "topic": item["topic"],
                "content": item["content"],
                "similarity": round(float(similarities[index]), 4)
            })

        return results