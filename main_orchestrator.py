import logging
from agents.agent import Agent
from agents.extractors import extract_revised_system_prompt, extract_updated_canvas
from agents.canvas import aggregate_contribution
from agents.logging_utils import setup_jsonl_logger
from colorama import Fore, Style, init

init(autoreset=True)

# === Task-Agnostic Code Improvement Orchestrator ===

logger = setup_jsonl_logger(level=logging.INFO)

#MODEL = 'meta-llama/Llama-4-Scout-17B-16E-Instruct'#'deepcoder:14b'
MODEL = 'ollama:jan-nano'

# Define agent roles for each phase
def get_agents_for_phase(phase):
    if phase == 'assessment':
        return [Agent(name="Analyzer", model=MODEL, persona="Static Analyzer: Identify bugs, code smells, and vulnerabilities.")]
    elif phase == 'implementation':
        return [Agent(name="Refactorer", model=MODEL, persona="Refactoring Specialist: Improve code structure, readability, and maintainability."),
                Agent(name="Documenter", model=MODEL, persona="Documentation Specialist: Add and improve code documentation.")]
    elif phase == 'review':
        return [Agent(name="Reviewer", model=MODEL, persona="Code Reviewer: Review changes and provide feedback.")]
    elif phase == 'deployment':
        return [Agent(name="Deployer", model=MODEL, persona="Deployment Specialist: Deploy code and monitor for issues.")]
    else:
        return []

# Load sample code as the initial canvas
with open('sample_code.py', 'r') as f:
    canvas = f.read()

system_prompt = "You are a team of AI agents improving a codebase. Follow the standard code improvement protocol."
session_prompt = "This is a multi-phase code improvement session. Each agent will contribute to the shared canvas for their phase."

phases = ['assessment', 'implementation', 'review', 'deployment']

logger.info("=== Multi-Agent Code Improvement Orchestrator ===")
logger.info(f"Initial System Prompt: {system_prompt}")
logger.info(f"Initial Session Prompt: {session_prompt}")
logger.info(f"Initial Shared Canvas: {canvas}")
logger.info("=" * 60)

for phase in phases:
    logger.info(f"--- Phase: {phase.capitalize()} ---")
    agents = get_agents_for_phase(phase)
    for agent in agents:
        logger.info(f"Agent {agent.name} is generating a response.")
        contribution = agent.generate_response(system_prompt, session_prompt, canvas, phase=phase)
        logger.debug(f"Contribution from {agent.name}: {contribution}")
        # For demonstration, always update the canvas
        canvas = aggregate_contribution(session_prompt, canvas, contribution, MODEL)
        logger.info(f"Canvas updated by {agent.name}.")
    logger.info("-" * 40)

logger.info("=== Code Improvement Complete ===")
logger.info(f"Final Shared Canvas: {canvas}")
logger.info(f"Final System Prompt: {system_prompt}")
