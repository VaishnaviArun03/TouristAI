import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

DB_PATH = "db/hotel_db"


def load_db():
    return FAISS.load_local(
        DB_PATH,
        embedding,
        allow_dangerous_deserialization=True
    )


def save_data(question, answer):
    documents = [
    Document(
        page_content=question,
        metadata={
            "answer": answer
        }
        )
    ]

    if os.path.exists(DB_PATH):
        db = load_db()
        db.add_documents(documents)
        db.save_local(DB_PATH)
    else:
        db = FAISS.from_documents(
            documents,
            embedding
        )
        db.save_local(DB_PATH)

def search_data(question):
    try:
        db = load_db()

        docs = db.similarity_search_with_score(
            question,
            k=1
        )

        if not docs:
            return None

        doc, score = docs[0]

        print("Question :", question)
        print("Matched  :", doc.page_content)
        print("Score    :", score)

        if doc.page_content.lower().strip() == question.lower().strip():
            print("Exact Match Found")
            return doc.metadata["answer"]

        if score < 0.3:
            print("Semantic Match Found")
            return doc.metadata["answer"]

        return None

    except Exception as e:
        print(e)
        return None