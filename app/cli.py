from app.agent import ask_agent


def main() -> None:
    print("Foundry Agent Starter")
    print("Type 'exit' or 'quit' to leave.")
    print()

    try:
        while True:
            question = input("You: ").strip()

            if question.lower() in {"exit", "quit"}:
                break

            answer = ask_agent(question)
            print(f"Agent: {answer}")
            print()
    except KeyboardInterrupt:
        print("\nBye.")


if __name__ == "__main__":
    main()
