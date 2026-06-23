import os
import sys
from dotenv import load_dotenv


def main():
    # Load environment variables first to make them available globally
    load_dotenv()

    agent_path = os.path.join(
        os.path.dirname(__file__),
        "nearby-places-agent"
    )

    if agent_path not in sys.path:
        sys.path.insert(0, agent_path)

    from agent import nearby_agent

    while True:
        question = input("\nYou: ")

        if question.lower() == "exit":
            break

        if not question.strip():
            print("Please enter a question.")
            continue

        response = nearby_agent(question)

        print("\nAI:")
        print(response)


if __name__ == "__main__":
    main()