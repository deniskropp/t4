import logging
from agents.agent import Agent
from agents.canvas import Canvas
from agents.logging_utils import setup_jsonl_logger
from colorama import Fore, Style, init
import argparse

init(autoreset=True)

# === Task-Agnostic Code Improvement Orchestrator ===

logger = setup_jsonl_logger(level=logging.INFO)

MODEL = 'ollama:gemma3:1b'

# Define agent roles for each phase
def get_agents_for_phase(phase):
    """
    Returns a list of Agent instances for the given phase, with explicit roles.
    """
    if phase == 'assessment':
        return [
            Agent(name="Analyzer", model=MODEL, persona="Static Analyzer: Identify bugs, code smells, and vulnerabilities.", role="analysis")
        ]
    elif phase == 'implementation':
        return [
            Agent(name="Refactorer", model=MODEL, persona="Refactoring Specialist: Improve code structure, readability, and maintainability.", role="refactor"),
            Agent(name="Documenter", model=MODEL, persona="Documentation Specialist: Add and improve code documentation.", role="document"),
            Agent(name="Logger", model=MODEL, persona="Logging Specialist: Insert appropriate logging statements following best practices.", role="logging"),
            Agent(name="Tester", model=MODEL, persona="Testing Specialist: Generate and improve unit/integration tests.", role="test")
        ]
    elif phase == 'review':
        return [
            Agent(name="Reviewer", model=MODEL, persona="Code Reviewer: Review changes and provide feedback.", role="review")
        ]
    elif phase == 'deployment':
        return [
            Agent(name="Deployer", model=MODEL, persona="Deployment Specialist: Deploy code and monitor for issues.", role="deploy")
        ]
    else:
        return []

parser = argparse.ArgumentParser(description="Multi-Agent Code Improvement Orchestrator")
parser.add_argument(
    "--files",
    nargs="+",
    required=True,
    help="List of code files to improve"
)
parser.add_argument(
    "--model",
    type=str,
    default="ollama:gemma3:1b",
    help="Model to use for all agents (default: ollama:gemma3:1b)"
)
args = parser.parse_args()
MODEL = args.model


# Aggregate contents of all input files into the canvas
canvas = ""
for file_path in args.files:
    with open(file_path, 'r') as f:
        canvas += f"\n⫻context/file:{file_path}\n"
        canvas += f.read()
canvas = canvas.strip()


system_prompt = "You are a team of AI agents improving a codebase. Follow the standard code improvement protocol."
session_prompt = f"This is a multi-phase code improvement session. Each agent will contribute to the shared canvas for their phase."
canvas = Canvas(canvas)
phases = ['assessment', 'implementation', 'review', 'deployment']

print("=== Multi-Agent Code Improvement Orchestrator ===")
print(f"Initial System Prompt: {system_prompt}")
print(f"Initial Session Prompt: {session_prompt}")
print(f"Initial Shared Canvas: {canvas}")
print("=" * 60)

for phase in phases:
    print(f"--- Phase: {phase.capitalize()} ---")
    agents = get_agents_for_phase(phase)
    for agent in agents:
        print(f"Agent {agent.name} (role: {agent.role}) is generating a response.")
        # Prepare extra context for future extensibility (e.g., analysis findings, diffs)
        extra_context = None
        contribution = agent.generate_response(system_prompt, session_prompt, canvas, phase=phase, extra_context=extra_context)
        #canvas.update(contribution)
        #logger.debug(f"Contribution from {agent.name}: {contribution}")
        # For demonstration, always update the canvas
        canvas.aggregate_contribution(contribution, MODEL)
        #print(f"Canvas updated by {agent.name}.")
    print("-" * 40)

print("=== Code Improvement Complete ===")
print(f"Final Shared Canvas: {canvas}")
print(f"Final System Prompt: {system_prompt}")
