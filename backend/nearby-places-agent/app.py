from agent import nearby_agent

while True:
    question = input("You: ")

    if question.lower() == "exit":
        break

    answer = nearby_agent(
        question=question,
        location="Trichy"
    )

    print("\nAI:")
    print(answer)