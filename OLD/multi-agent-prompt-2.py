import ollama # Keep the import for completeness, though we'll simulate its use

class Agent:
    """Represents an agent with a name, model, and persona."""
    def __init__(self, name, model, persona):
        self.name = name
        self.model = model
        self.persona = persona

    def generate_response(self, system_prompt, prompt):
        """
        Generates a response based on the agent's persona and prompt.
        This function simulates the call to ollama.generate.
        """
        print(f"\n{'='*60}\n{self.name} is preparing a contribution...\n{'='*60}")
        print(f"--- SYSTEM PROMPT ---\n{system_prompt}\n--- END SYSTEM PROMPT ---\n")
        print(f"--- AGENT PROMPT ---\n{prompt}\n--- END AGENT PROMPT ---\n")
        # --- Start Simulation Logic ---
        response = ollama.generate(
            model=self.model,
            system=system_prompt,
            prompt=prompt
        )
        ret = response['response'].strip()
        print(f"\n{self.name} contributed:\n{ret}\n{'-'*60}\n")
        return ret

# Model and Agents
MODEL = 'gemma3:4b' # Placeholder model name

designer = Agent(
    name="Designer",
    model=MODEL,
    persona="Creative Web Designer: Focus on visual aesthetics, user experience, and layout. Suggest color schemes, typography, and design elements."
)
engineer = Agent(
    name="Engineer",
    model=MODEL,
    persona="Front-End Engineer: Implement designs using HTML, CSS, and JavaScript. Ensure responsiveness, accessibility, and performance."
)
prompt_dev = Agent(
    name="PromptDev",
    model=MODEL,
    persona="Prompt Engineer: Observe the collaboration and refine the system prompt to keep the team aligned and effective."
)

agents = [designer, engineer, prompt_dev]

# Initial Setup
canvas = "Shared Canvas:\n"
rounds = 30
system_prompt = (
    "This is a collaborative multi-agent design session. Each agent will add to or modify the shared canvas below."
)

print("\n=== Multi-Agent Web Design Collaboration ===")
print(f"Initial System Prompt: {system_prompt}")
print("=" * 50)

for round_number in range(1, rounds + 1):
    print(f"\n\n\n\n\n\n\n\n\n=== Round {round_number} ===")
    for agent in agents:
        prompt = (
            f"{canvas}\n\n\n"
            f"As {agent.name}: {agent.persona}\nWhat is your contribution?"
        )
        try:
            reply = agent.generate_response(system_prompt, prompt)
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
