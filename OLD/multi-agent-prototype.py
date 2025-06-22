import ollama  # Keep the import for completeness, though we'll simulate its use
import re
from colorama import Fore, Style, init

init(autoreset=True)

AGENT_COLORS = {
    "Designer": Fore.CYAN,
    "Engineer": Fore.GREEN,
    "PromptDev": Fore.MAGENTA
}
LABEL_COLOR = Fore.YELLOW

class Agent:
    """Represents an agent with a name, model, and persona."""
    def __init__(self, name, model, persona):
        self.name = name
        self.model = model
        self.persona = persona

    def generate_response(self, system_prompt, session_prompt, canvas):
        color = AGENT_COLORS.get(self.name, Fore.WHITE)
        print(f"\n{color}--- {self.name} is thinking ---{Style.RESET_ALL}")
        # Construct the messages list for ollama.chat
        messages = [
            {"role": "system", "content": f"System Prompt:\n{system_prompt}\n\n"},
            {"role": "user", "content": f"Session Prompt:\n{session_prompt}\n\n"},
            {"role": "user", "content": f"Shared Canvas:\n{canvas}\n\n"},
            {"role": "user", "content": f"Your persona: {self.persona}\n"}
        ]

        for msg in messages:
            label, _, content = msg['content'].partition(':')
            print(f"{LABEL_COLOR}{label}:{Style.RESET_ALL}{content}")
            print("  ...." * 10)


        full_response = ""
        print(f"\n{color}{self.name} contributing (streaming):{Style.RESET_ALL}")
        print("-" * 60)

        # Use ollama.chat in stream mode
        stream = ollama.chat(
            model=self.model,
            messages=messages,
            stream=True,
        )

        # Process the streamed response
        for chunk in stream:
            if chunk['message']['content'] is not None:
                content = chunk['message']['content']
                print(content, end='', flush=True) # Print as it arrives
                full_response += content

        print(f"\n{'-'*60}\n")
        print(f"--- {self.name} finished thinking ---\n")

        return full_response.strip()

def extract_revised_system_prompt(contribution):
    """
    Extracts the revised system prompt from PromptDev's contribution.
    Looks for a heading or marker and returns the following section.
    """
    # Try to find the heading and capture all lines until a triple newline or end of string
    match = re.search(
        r"\*?\*?.*System Prompt.*\*?\*?\s*\n+([\s\S]*?)(?:\n{3,}|\Z)", contribution
    )
    if match:
        # Return the extracted prompt, stripped of leading/trailing whitespace
        return match.group(1).strip()
    else:
        # Fallback: return the whole contribution (as before)
        return contribution.strip()


def aggregate_contribution(canvas, contribution):
    """
    Uses ollama to summarize or merge the new contribution into the shared canvas.
    """
    prompt = (
        "You are a collaborative assistant. Given the current shared canvas and a new contribution, "
        "integrate the new contribution into the canvas, preserving important details and ensuring coherence. "
        "Do not remove existing valuable content. Return the updated canvas."
    )
    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": f"Current Canvas:\n{canvas}\n"},
        {"role": "user", "content": f"New Contribution:\n{contribution}\n"}
    ]
    response = ollama.chat(
        model=MODEL,
        messages=messages,
        stream=False,
    )
    updated_canvas = response['message']['content'].strip()
    return updated_canvas


# Model and Agents
MODEL = 'gemma3:4b'  # Placeholder model name
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
canvas = ""
system_prompt = "We are collaboratively designing a simple, responsive web page."
session_prompt = (
    "This is a collaborative multi-agent design session. Each agent will add to or modify the shared canvas below. "
    "PromptDev will update the system prompt as needed to keep the team aligned."
)
num_rounds = 20  # Reasonable number for demonstration

print("\n=== Multi-Agent Web Design Collaboration Prototype ===")
print(f"Initial Session Prompt: {session_prompt}")
print(f"Initial System Prompt: {system_prompt}")
print("=" * 60)

for round_num in range(1, num_rounds + 1):
    print(f"\n\n\n\n\n\n+++ --- Round {round_num} --- +++")
    for agent in agents:
        contribution = agent.generate_response(system_prompt, session_prompt, canvas)
        if agent.name == "PromptDev":
            print("PromptDev is updating the system prompt...")
            system_prompt = extract_revised_system_prompt(contribution)
            #canvas = ""  # Optionally clear canvas after prompt update
        else:
            #canvas += f"{contribution}\n\n\n\n"
            canvas = aggregate_contribution(canvas, contribution)
    print("\nCurrent Shared Canvas:\n" + canvas)
    print("Current System Prompt:\n" + system_prompt)
    print("-" * 40)

print("\n=== Simulation Complete ===")
print("\nFinal Shared Canvas:\n" + canvas)
print("\nFinal System Prompt:\n" + system_prompt)
