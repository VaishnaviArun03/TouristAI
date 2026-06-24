from langchain_groq import ChatGroq
from dotenv import load_dotenv
from rag.hotel_rag import (
    search_data,
    save_data
)
import os

load_dotenv()

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY")
)


def hotel_agent(question):
    # Step 1: Search in FAISS
    cached_answer = search_data(question)

    if cached_answer:
        print("Answer from Hotel RAG")
        return cached_answer

    # Step 2: Call LLM
    print("Answer from LLM")

    prompt = f"""
    You are a hotel recommendation agent.

    Recommend hotels, price ranges,
    ratings and amenities.

    Question:
    {question}
    """

    response = llm.invoke(prompt)
    answer = response.content

    # Step 3: Save in FAISS
    save_data(
        question,
        answer
    )

    return answer