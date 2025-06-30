from colorama import Fore, Style
from agents.chatmodel import ChatModelFactory

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
    def __init__(self, name, model, persona, role=None, chat_model=None):
        self.name = name
        self.persona = persona
        self.role = role  # e.g., 'analysis', 'refactor', 'test', etc.
        self.factory = ChatModelFactory(model=model, chat_model=chat_model)

    def generate_response(self, system_prompt, session_prompt, canvas, phase=None, extra_context=None):
        color = AGENT_COLORS.get(self.name, Fore.WHITE)
        print(f"\n\n{AGENT_ROUND_COLOR}--- {self.name} is thinking ---{Style.RESET_ALL}")
        # Phase- and role-specific instructions
        phase_instruction = f"\nCurrent Phase: {phase.capitalize()}" if phase else ""
        role_instruction = f"\nAgent Role: {self.role}" if self.role else ""
        # Optionally, add extra context (e.g., analysis findings, diffs, etc.)
        extra = f"\nExtra Context: {extra_context}" if extra_context else ""
        messages = [
            {"role": "system", "content": f"System Prompt:\n{system_prompt}{phase_instruction}{role_instruction}{extra}\n\n"},
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
        chat_model = self.factory.get()
        stream = chat_model.chat(
#            model=self.model,
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
