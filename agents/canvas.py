from colorama import Fore, Style
from agents.chatmodel import ChatModelFactory, HFStreamingChatModel, OllamaStreamingChatModel
from agents.extractors import extract_updated_canvas

CANVAS_ROUND_COLOR = Fore.LIGHTMAGENTA_EX

factory = ChatModelFactory()

class Canvas:
    """
    Represents the shared canvas where contributions are aggregated.
    This class can be extended to include methods for managing the canvas state.
    """
    def __init__(self, initial_content=""):
        self.content = initial_content

    def update(self, new_content):
        self.content += f"\n{new_content}"

    def __str__(self):
        return self.content

    def get_content(self):
        """
        Returns the current content of the canvas.
        This can be used to retrieve the canvas state for contributions.
        """
        return self.content

    def aggregate_contribution(self, contribution, model=None):
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
            {"role": "user", "content": f"Current Canvas:\n{self.content}\n"},
            {"role": "user", "content": f"New Contribution:\n{contribution}\n"}
        ]
        print(f"\n{Fore.BLUE}Current Canvas:{Style.RESET_ALL}\n{self.content}\n")
        print(f"\n{Fore.MAGENTA}New Contribution:{Style.RESET_ALL}\n{contribution}\n")
        full_response = ""
        print(f"\n{Fore.LIGHTGREEN_EX}Aggregator (streaming):{Style.RESET_ALL}")
        chat_model = factory.get(model=model)
        stream = chat_model.chat(
            #model=model,
            messages=messages,
            stream=True,
        )
        for chunk in stream:
            if chunk['message']['content'] is not None:
                content = chunk['message']['content']
                print(content, end='', flush=True)
                full_response += content
        updated_canvas = extract_updated_canvas(full_response.strip())
        print(f"\n{Fore.GREEN}Updated Canvas:{Style.RESET_ALL}\n{updated_canvas}\n\n\n\n")
        self.content = updated_canvas
