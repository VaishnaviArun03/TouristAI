from google_places import get_places
from rag import load_db, save_places
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY")
)

RAG_SIMILARITY_THRESHOLD = 0.5


VALID_CATEGORIES = [
    "nearby",
    "place",
    "places",
    "restaurant",
    "restaurants",
    "hotel",
    "hotels"
]


def _is_valid_question(question: str) -> bool:
    """
    Checks if the question contains any of the valid keywords.
    """
    print("--- Checking question for valid keywords ---")
    question_lower = question.lower()
    for category in VALID_CATEGORIES:
        if category in question_lower:
            print(f"--- Found valid keyword: '{category}' ---")
            return True
    print("--- No valid keywords found in question ---")
    return False


def nearby_agent(question):
    # Move the guardrail check to be the very first step, outside the try block.
    if not _is_valid_question(question):
        return ""

    try:
        # Attempt to load the local vector database
        db = load_db()

        docs = db.similarity_search_with_score(
            question,
            k=3
        )

        # If we find a good match (low score), return the cached result
        if docs and docs[0][1] < RAG_SIMILARITY_THRESHOLD:
            print("Answer from RAG")

            # Filter to only include highly relevant documents below the threshold
            return "\n\n".join(
                doc.page_content
                for doc, score in docs if score < RAG_SIMILARITY_THRESHOLD
            )
    
    except FileNotFoundError:
        # This is an expected error on the first run when the DB doesn't exist yet.
        print("Local RAG DB not found. Falling back to LLM.")
    except Exception as e:
        print(f"An unexpected error occurred during RAG search: {e}")

    # --- Fallback Logic ---
    # If RAG fails or doesn't have a good answer, call the LLM directly.
    print("No relevant info in RAG. Asking LLM directly...")

    # We can use a simple prompt, as we have no external context to provide.
    prompt = f"You are a helpful local guide. Answer the following question: {question}"

    response = llm.invoke(prompt)

    # --- Learn from the interaction ---
    # Save the LLM's generated answer back into the RAG database for future use.
    print("Saving new knowledge to RAG DB...")
    new_knowledge = [{"question": question, "answer": response.content}]
    save_places(new_knowledge)

    return response.content