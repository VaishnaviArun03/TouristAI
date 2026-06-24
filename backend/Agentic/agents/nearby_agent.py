from langchain_groq import ChatGroq
from dotenv import load_dotenv
from rag.nearby_rag import search_data, save_data
import os

load_dotenv()

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY")
)


def nearby_agent(question):
    # Step 1: Search in FAISS
    cached_answer = search_data(question)

    if cached_answer:
        print("Answer from RAG")
        return cached_answer

    # Step 2: Call LLM
    print("Answer from LLM")

    prompt = f"""
    You are a nearby places guide.

    User Question:
    {question}
    """

    response = llm.invoke(prompt)

    answer = response.content

    # Step 3: Save to FAISS
    save_data(
        question,
        answer
    )

    return answer