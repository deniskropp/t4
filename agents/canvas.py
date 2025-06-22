import ollama
from colorama import Fore, Style
from .extractors import extract_updated_canvas

CANVAS_ROUND_COLOR = Fore.LIGHTMAGENTA_EX


def aggregate_contribution(session_prompt, canvas, contribution, model):
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
    full_response = ""
    print(f"\n{Fore.LIGHTGREEN_EX}Aggregator (streaming):{Style.RESET_ALL}")
    stream = ollama.chat(
        model=model,
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
    return updated_canvas
