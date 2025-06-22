import logging
from agents.agent import Agent
from agents.extractors import extract_revised_system_prompt
from agents.canvas import aggregate_contribution
from agents.logging_utils import setup_jsonl_logger
from colorama import Fore, Style, init

init(autoreset=True)

BANNER_COLOR = Fore.LIGHTYELLOW_EX
LABEL_COLOR = Fore.YELLOW
ROUND_COLOR = Fore.RED

# Set up JSONL logger
logger = setup_jsonl_logger(level=logging.INFO)

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

system_prompt = "We are collaboratively designing a simple, responsive web page."
session_prompt = (
    "This is a collaborative multi-agent design session. Each agent will add to or modify the shared canvas below. "
    "PromptDev will update the system prompt as needed to keep the team aligned."
)
canvas = ""
num_rounds = 20

logger.info("=== Multi-Agent Web Design Collaboration Prototype ===")
logger.info(f"Initial System Prompt: {system_prompt}")
logger.info(f"Initial Session Prompt: {session_prompt}")
logger.info(f"Initial Shared Canvas: {canvas}")
logger.info("=" * 60)

for round_num in range(1, num_rounds + 1):
    logger.info(f"+++ --- Round {round_num} --- +++")
    for agent in agents:
        logger.info(f"Agent {agent.name} is generating a response.")
        contribution = agent.generate_response(system_prompt, session_prompt, canvas)
        logger.debug(f"Contribution from {agent.name}: {contribution}")
        if agent.name == "PromptDev":
            system_prompt = extract_revised_system_prompt(contribution)
            logger.info(f"System prompt updated by PromptDev.")
        else:
            canvas = aggregate_contribution(session_prompt, canvas, contribution, MODEL)
            logger.info(f"Canvas updated by {agent.name}.")
    logger.info("-" * 40)

logger.info("=== Simulation Complete ===")
logger.info(f"Final Shared Canvas: {canvas}")
logger.info(f"Final System Prompt: {system_prompt}")
