from langchain_groq import ChatGroq
from dotenv import load_dotenv
from rag.restaurant_rag import (
    search_data,
    save_data
)
import os

load_dotenv()

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY")
)


def restaurant_agent(question):
    # Search in FAISS first
    cached_answer = search_data(question)

    if cached_answer:
        print("Answer from Restaurant RAG")
        return cached_answer

    print("Answer from LLM")

    prompt = f"""
    You are a restaurant recommendation agent.

    Recommend restaurants, foods, ratings and specialties.

    Question:
    {question}
    """

    response = llm.invoke(prompt)

    answer = response.content

    # Save to FAISS
    save_data(
        question,
        answer
    )

    return answer