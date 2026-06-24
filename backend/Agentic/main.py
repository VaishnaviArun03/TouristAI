from graph import app


while True:
    question = input("You : ")

    if question.lower() == "exit":
        break

    result = app.invoke(
        {
            "question": question,
            "category": "",
            "answer": ""
        }
    )

    print("\nAI:")
    print(result["answer"])