import ollama  # Keep the import for completeness, though we'll simulate its use
import re
from colorama import Fore, Style, init

init(autoreset=True)

AGENT_COLORS = {
    "Designer": Fore.CYAN,
    "Engineer": Fore.GREEN,
    "PromptDev": Fore.MAGENTA
}
BANNER_COLOR = Fore.LIGHTYELLOW_EX
LABEL_COLOR = Fore.YELLOW
ROUND_COLOR = Fore.RED
AGENT_ROUND_COLOR = Fore.LIGHTRED_EX
CANVAS_ROUND_COLOR = Fore.LIGHTMAGENTA_EX

class Agent:
    """Represents an agent with a name, model, and persona."""
    def __init__(self, name, model, persona):
        self.name = name
        self.model = model
        self.persona = persona

    def generate_response(self, system_prompt, session_prompt, canvas):
        color = AGENT_COLORS.get(self.name, Fore.WHITE)
        #print(f"\n{color}--- {self.name} is thinking ---{Style.RESET_ALL}")
        print(f"\n\n{AGENT_ROUND_COLOR}--- {self.name} is thinking ---{Style.RESET_ALL}")
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
        r"\*?\*?.*System Prompt.*\*?\*?\s*\n+([\s\S]*?)(?:\n\-{3,}\n|\n{3,}|\Z)", contribution
    )
    if match:
        # Return the extracted prompt, stripped of leading/trailing whitespace
        return match.group(1).strip()
    else:
        # Fallback: return the whole contribution (as before)
        return contribution.strip()


def extract_updated_canvas(update):
    """
    Extracts the updated canvas.
    """
    # Try to find the heading and capture all lines until a triple newline or end of string
    match = re.search(
        r"\*?\*?.*Canvas.*\*?\*?\s*\n+([\s\S]*?)(?:\n\-{3,}\n|\n{3,}|\Z)", update
    )
    if match:
        # Return the extracted prompt, stripped of leading/trailing whitespace
        return match.group(1).strip()
    else:
        # Fallback: return the whole contribution (as before)
        return update.strip()


def aggregate_contribution(session_prompt, canvas, contribution):
    """
    Uses ollama to summarize or merge the new contribution into the shared canvas.
    """
    print(f"\n\n{CANVAS_ROUND_COLOR}--- --- Updating Canvas --- ---{Style.RESET_ALL}")
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
    print(f"\n{Fore.BLUE}Current Canvas:{Style.RESET_ALL}\n{canvas}\n")
    print(f"\n{Fore.MAGENTA}New Contribution:{Style.RESET_ALL}\n{contribution}\n")
    response = ollama.chat(
        model=MODEL,
        messages=messages,
        stream=False,
    )
    updated_canvas = extract_updated_canvas(response['message']['content'].strip())
    print(f"{Fore.GREEN}Updated Canvas:{Style.RESET_ALL}\n{updated_canvas}\n\n\n\n")
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
system_prompt = "We are collaboratively designing a simple, responsive web page."
session_prompt = (
    "This is a collaborative multi-agent design session. Each agent will add to or modify the shared canvas below. "
    "PromptDev will update the system prompt as needed to keep the team aligned."
)
canvas = ""
num_rounds = 20  # Reasonable number for demonstration

print(f"\n{BANNER_COLOR}=== Multi-Agent Web Design Collaboration Prototype ==={Style.RESET_ALL}")
print(f"{LABEL_COLOR}Initial System Prompt:{Style.RESET_ALL}\n{system_prompt}\n")
print(f"{LABEL_COLOR}Initial Session Prompt:{Style.RESET_ALL}\n{session_prompt}\n")
print(f"{LABEL_COLOR}Initial Shared Canvas:{Style.RESET_ALL}\n{canvas}\n")
print(f"{BANNER_COLOR}{"=" * 60}{Style.RESET_ALL}")

for round_num in range(1, num_rounds + 1):
    print(f"\n\n\n\n\n\n{ROUND_COLOR}+++ --- Round {round_num} --- +++{Style.RESET_ALL}")
    for agent in agents:
        contribution = agent.generate_response(system_prompt, session_prompt, canvas)
        if agent.name == "PromptDev":
            #print("PromptDev is updating the system prompt...")
            system_prompt = extract_revised_system_prompt(contribution)
            #canvas = ""  # Optionally clear canvas after prompt update
        else:
            #canvas += f"{contribution}\n\n\n\n"
            canvas = aggregate_contribution(session_prompt, canvas, contribution)
    #print("\nCurrent Shared Canvas:\n" + canvas)
    #print("Current System Prompt:\n" + system_prompt)
    print("-" * 40)

print("\n=== Simulation Complete ===")
print("\nFinal Shared Canvas:\n" + canvas)
print("\nFinal System Prompt:\n" + system_prompt)
