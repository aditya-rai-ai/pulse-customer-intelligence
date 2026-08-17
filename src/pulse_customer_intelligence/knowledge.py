"""Pulse's knowledge base — a tiny Retrieval-Augmented Generation (RAG) setup.

It turns FAQ/policy text into 'meaning vectors' (embeddings), so we can find the
most relevant entry for any question by meaning, not by matching keywords.
"""
import numpy as np
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
_client = OpenAI()  # reads OPENAI_API_KEY from your .env

# The company's knowledge. Swap in real policies/FAQ later.
KNOWLEDGE_BASE = [
    "Return policy: If any produce does not meet quality standards, report it within 2 hours of delivery for a free replacement or refund.",
    "Delivery: We deliver within a 5 km radius. Delivery is free on orders above Rs 200; smaller orders have a flat Rs 30 fee.",
    "Freshness: All our produce is sourced fresh from local farms every day.",
    "Payments: We accept Cash on Delivery, UPI (Google Pay, PhonePe, Paytm), debit and credit cards, and net banking.",
    "Store hours: We are open every day from 7:00 AM to 9:00 PM.",
    "Organic range: We stock a dedicated selection of certified organic vegetables.",
]


def _embed(text: str) -> np.ndarray:
    """Turn a piece of text into a meaning vector (embedding)."""
    response = _client.embeddings.create(model="text-embedding-3-small", input=text)
    return np.array(response.data[0].embedding)


# Compute an embedding for every knowledge entry once, when this file loads.
_kb_vectors = [_embed(entry) for entry in KNOWLEDGE_BASE]


def _cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """How close two vectors are in meaning: 1.0 = identical, 0 = unrelated."""
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


def search_knowledge(query: str) -> str:
    """Return the single most relevant company knowledge entry for a question or topic."""
    query_vector = _embed(query)
    scores = [_cosine_similarity(query_vector, kb_vector) for kb_vector in _kb_vectors]
    best_index = int(np.argmax(scores))
    return KNOWLEDGE_BASE[best_index]


if __name__ == "__main__":
    # Quick test — does it find the right knowledge by MEANING, not keywords?
    print("Q: tomatoes were mushy and not fresh")
    print("A:", search_knowledge("The tomatoes I received were mushy and not fresh"))
    print()
    print("Q: how can I pay you?")
    print("A:", search_knowledge("how can I pay you?"))
    print()
    print("Q: what time do you close?")
    print("A:", search_knowledge("what time do you close?"))