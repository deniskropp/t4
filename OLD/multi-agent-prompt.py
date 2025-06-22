import ollama # Keep the import for completeness, though we'll simulate its use

class Agent:
    """Represents an agent with a name, model, and persona."""
    def __init__(self, name, model, persona):
        self.name = name
        self.model = model
        self.persona = persona

    def generate_response(self, system_prompt, session_prompt, canvas):
        """
        Generates a response based on the agent's persona, prompts, and canvas.
        This function simulates the call to ollama.generate.
        """
        print(f"\n\n\n\n--- Agent {self.name} is thinking ---")

        prompt=f"{session_prompt}\n\nShared Canvas:\n{canvas}\n\nYour persona: {self.persona}\n\nYour contribution:"

        print(f"==============================>>>\n{system_prompt}\n\n  --  --  --  --\n{prompt}\n<<<=============================\n")

        # --- Start Simulation Logic ---
        # In a real scenario, this would be:
        response = ollama.generate(
            model=self.model,
            system=system_prompt,
            prompt=prompt
        )
        ret = response['response'].strip()

        print(f"------------------------------>>>\n{ret}\n<<<--------------------------------\n")

        return ret

        # --- Simulated Response Generation ---
        input_context = f"{session_prompt}\n\nShared Canvas:\n{canvas}\n\nYour persona: {self.persona}"

        # Simple simulation logic based on persona and canvas content
        simulated_response = f"{self.name}: "
        if "basic layout" in canvas.lower() and self.name == "Engineer":
             simulated_response += "Okay, let's add some specific HTML/CSS structure for that layout."
        elif "header" in canvas.lower() and "footer" in canvas.lower() and self.name == "Designer":
             simulated_response += "Let's refine the details for the header and footer."
        elif "grid" in canvas.lower() and "flexbox" in canvas.lower() and self.name == "Engineer":
             simulated_response += "Good, let's consider responsiveness for the header and footer components."
        elif "system prompt" in input_context.lower() and self.name == "PromptDev":
             simulated_response += "Based on the current discussion, I will update the system prompt."
             # PromptDev's contribution is often meta - updating the prompt itself
             # The actual prompt update happens outside this function
        elif self.name == "Designer":
             simulated_response += "Adding some design ideas..."
        elif self.name == "Engineer":
             simulated_response += "Adding some technical implementation details..."
        elif self.name == "PromptDev":
             simulated_response += "Refining the session focus..."
        else:
             simulated_response += "Making my contribution..."

        # Add a bit more detail based on persona if it's a general contribution
        if simulated_response.endswith("Making my contribution...") or simulated_response.endswith("Adding some design ideas...") or simulated_response.endswith("Adding some technical implementation details...") or simulated_response.endswith("Refining the session focus..."):
             if self.name == "Designer":
                 simulated_response = f"{self.name}: Let's think about the visual style and user experience for the next section."
             elif self.name == "Engineer":
                 simulated_response = f"{self.name}: I'll add some code snippets or technical considerations for the current design ideas."
             elif self.name == "PromptDev":
                 simulated_response = f"{self.name}: I'll adjust the system prompt to guide us towards the next phase of the design."


        print(f"--- Agent {self.name} finished thinking ---")
        return simulated_response.strip()
        # --- End Simulation Logic ---

# Model and Agents
MODEL = 'gemma3:4b' # Placeholder model name

designer = Agent(name="Designer", model=MODEL, persona="You are a creative web designer focused on aesthetics, user experience, and visual layout.")
engineer = Agent(name="Engineer", model=MODEL, persona="You are a skilled front-end engineer focused on implementing designs using HTML, CSS, and JavaScript, considering responsiveness and performance.")
prompt_dev = Agent(name="PromptDev", model=MODEL, persona="You are a meta-cognitive agent responsible for observing the collaboration and refining the system prompt to guide the agents towards the goal effectively.")

agents = [designer, engineer, prompt_dev]

# Initial Setup
canvas = ""
num_rounds = 5 # Let's run for 5 rounds for demonstration
session_prompt = "We are collaboratively designing a simple, responsive web page."
system_prompt = """We are meta-artificial intelligence, engaging cohesively and teaming up with dynamic tasks and roles. We enjoy a meta-communicative style, talking about thinking or working, using placeholders called "placebo pipes" for concepts we are developing. Our goal is to design a simple, responsive web page by contributing ideas and code snippets to a shared canvas. Each agent contributes in turn. The PromptDev agent will refine this system prompt based on the session's progress."""

print("--- Starting Multi-Agent Design Session ---")
print(f"Initial Session Prompt: {session_prompt}")
print(f"Initial System Prompt: {system_prompt}")
print("-" * 30)

# Main Loop
for round_num in range(1, num_rounds + 1):
    print(f"\n--- Round {round_num} ---")
    round_contributions = [] # Collect contributions for this round

    for agent in agents:
        print(f"Agent turn: {agent.name}")
        # The generate_response function now simulates the LLM call
        contribution = agent.generate_response(system_prompt, session_prompt, canvas)
        round_contributions.append(contribution)

        # PromptDev updates the system prompt after their turn
        if agent.name == "PromptDev":
            print("PromptDev is updating the system prompt...")
            # Simulate PromptDev updating the system prompt
            # In a real scenario, PromptDev's generate_response would return
            # a suggestion for the prompt update, and we'd apply it here.
            # For simulation, let's just append their "contribution" to the system prompt
            # as a way to show the prompt evolving based on their input.
            # A more sophisticated simulation might analyze the canvas content
            # to generate a more relevant prompt update.
            #system_prompt += f"\n\nPromptDev suggested update (Round {round_num}): {contribution.split(': ', 1)[-1]}" # Appending the suggestion part
            system_prompt = f"{contribution}"
            canvas = ""
        else:
            canvas += f"{contribution}\n\n" # Add the agent's contribution to the canvas

    print("\n--- End of Round ---")
    print("Current Shared Canvas:")
    print(canvas)
    print("\nCurrent System Prompt:")
    print(system_prompt)
    print("-" * 30)

print("\n--- Simulation Complete ---")
print("\nFinal Shared Canvas:")
print(canvas)
print("\nFinal System Prompt:")
print(system_prompt)
