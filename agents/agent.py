import ollama
from colorama import Fore, Style

AGENT_COLORS = {
    "Designer": Fore.CYAN,
    "Engineer": Fore.GREEN,
    "PromptDev": Fore.MAGENTA,
    "Analyzer": Fore.LIGHTBLUE_EX,
    "Refactorer": Fore.LIGHTGREEN_EX,
    "Documenter": Fore.LIGHTYELLOW_EX,
    "Reviewer": Fore.LIGHTMAGENTA_EX,
    "Deployer": Fore.LIGHTWHITE_EX
}
AGENT_ROUND_COLOR = Fore.LIGHTRED_EX
LABEL_COLOR = Fore.YELLOW

class Agent:
    """Represents an agent with a name, model, persona, and optional phase-specific behavior."""
    def __init__(self, name, model, persona):
        self.name = name
        self.model = model
        self.persona = persona

    def generate_response(self, system_prompt, session_prompt, canvas, phase=None):
        color = AGENT_COLORS.get(self.name, Fore.WHITE)
        print(f"\n\n{AGENT_ROUND_COLOR}--- {self.name} is thinking ---{Style.RESET_ALL}")
        # Optionally, phase-specific instructions can be added to the prompt
        phase_instruction = f"\nCurrent Phase: {phase.capitalize()}" if phase else ""
        messages = [
            {"role": "system", "content": f"System Prompt:\n{system_prompt}{phase_instruction}\n\n"},
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
        stream = ollama.chat(
            model=self.model,
            messages=messages,
            stream=True,
        )
        for chunk in stream:
            if chunk['message']['content'] is not None:
                content = chunk['message']['content']
                print(content, end='', flush=True)
                full_response += content
        print(f"\n{'-'*60}\n")
        print(f"--- {self.name} finished thinking ---\n")
        return full_response.strip()
