from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY")
)


def booking_agent(question):
    prompt = f"""
    You are a booking assistant.

    Question:
    {question}
    """

    response = llm.invoke(prompt)

    return response.content