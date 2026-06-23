import os
from langchain_huggingface import (
    HuggingFaceEmbeddings
)
from langchain_community.vectorstores import (
    FAISS
)
from langchain_core.documents import (
    Document
)

embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

DB_PATH = "places_db"


def save_places(places):
    # This function now saves question-answer pairs from the LLM.
    # We will create Document objects with the 'answer' as the content.
    # The embedding will be generated from this content.
    documents = [
        Document(page_content=p["answer"], metadata={"question": p["question"]})
        for p in places
    ]

    # To ensure we search by question but store the answer, we'll generate embeddings
    # from the questions and associate them with the answer documents.
    texts_for_embedding = [doc.metadata["question"] for doc in documents]
    embeddings = embedding.embed_documents(texts_for_embedding)
    
    # Create a list of (text, embedding) pairs
    text_embedding_pairs = list(zip(texts_for_embedding, embeddings))

    # Create a new FAISS index and add the documents and their pre-computed embeddings
    new_db = FAISS.from_embeddings(text_embedding_pairs, embedding, metadatas=[d.metadata for d in documents])
    # Now, replace the docstore content with the actual answers
    new_db.docstore._dict = {doc_id: doc for doc_id, doc in zip(new_db.index_to_docstore_id.values(), documents)}

    if os.path.exists(DB_PATH):
        db = load_db()
        db.merge_from(new_db)
        db.save_local(DB_PATH)
    else:
        new_db.save_local(DB_PATH)


def load_db():
    return FAISS.load_local(
        DB_PATH,
        embedding,
        allow_dangerous_deserialization=True
    )