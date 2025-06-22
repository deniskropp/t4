from ollama import generate

class Agent:
    def __init__(self, name, model, persona):
        self.name = name
        self.model = model
        self.persona = persona

# Define agents
agents = [
    Agent("Designer", "gemma3:4b", "You are a creative designer. Contribute ideas to the shared design canvas."),
    Agent("Engineer", "gemma3:4b", "You are a systems engineer. Refine and implement ideas on the shared canvas."),
    Agent("PromptDev", "gemma3:4b", "You are a prompt engineer. Improve the system prompt for the next round.")
]

canvas = "Shared Canvas:\n"
rounds = 30
system_prompt = (
    "This is a collaborative multi-agent design session. Each agent will add to or modify the shared canvas below."
)

for round_number in range(1, rounds + 1):
    print(f"\n\n\n\n\n\n\n\n\n=== Round {round_number} ===")
    for agent in agents:
        prompt = (
            f"{system_prompt}\n\n{canvas}\n\n\n"
            f"As {agent.name}: {agent.persona}\nWhat is your contribution?"
        )
        try:
            response = generate(agent.model, prompt)
            reply = response["response"]#as_simple_string()
            print(f"{agent.name}: {reply}")

            if agent.name == "PromptDev":
                system_prompt = reply
            else:
                canvas += f"{agent.name}: {reply}\n"

        except Exception as e:
            print(f"Error from {agent.name}: {e}")

    print("\nCurrent Canvas:\n" + canvas)
    print("Current System Prompt:\n" + system_prompt)

print("\n=== Final Shared Canvas ===\n" + canvas)
print("=== Final System Prompt ===\n" + system_prompt)
