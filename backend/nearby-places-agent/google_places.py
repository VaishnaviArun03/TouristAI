import os
from dotenv import load_dotenv

load_dotenv()


def get_places(question):
    """
    External API calls have been disabled. This function now returns an empty list.
    The agent will rely solely on its local RAG database.
    """
    print("External API (Geoapify) has been removed. No new places will be fetched.")
    return []