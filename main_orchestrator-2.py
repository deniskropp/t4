
#
# aichat -rcl -f gemma-deep-research.md -f chats/TaskAgnosticCodeImprovement-main_orchestrator-1.prompt.md
#

import logging
import os
from typing import List, Dict, Any

from agents.agent import Agent
from agents.canvas import Canvas
from agents.extractors import extract_revised_system_prompt, extract_updated_canvas
from agents.logging_utils import setup_jsonl_logger as setup_logging

# Setup structured logging
setup_logging()
logger = logging.getLogger(__name__)

# --- Configuration ---
# Define the phases of the code improvement plan
PLAN_PHASES = [
    "Understanding and Assessment",
    "Improvement Implementation",
    "Review and Deployment",
]

# Define the agents and their roles for each phase
# You can customize agents per phase or use a default set
AGENT_ROLES_PER_PHASE: Dict[str, List[Dict[str, str]]] = {
    "Understanding and Assessment": [
        {"name": "ContextGatherer", "persona": "Expert in project documentation and requirements.", "role": "gather context"},
        {"name": "StaticAnalyzer", "persona": "Tool-based code analysis expert.", "role": "perform static analysis"},
        {"name": "CodeReviewer", "persona": "Human-like code quality expert.", "role": "review code readability and maintainability"},
        {"name": "PerformanceProfiler", "persona": "Code performance bottleneck identifier.", "role": "identify performance issues"},
    ],
    "Improvement Implementation": [
        {"name": "Prioritizer", "persona": "Task and problem prioritization expert.", "role": "prioritize identified problems"},
        {"name": "Planner", "persona": "Action plan developer.", "role": "develop implementation plan"},
        {"name": "CodeRestructurer", "persona": "Code organization and modularity expert.", "role": "restructure code"},
        {"name": "CodeRefactorer", "persona": "Code readability and maintainability expert.", "role": "refactor code"},
        {"name": "Documenter", "persona": "Code documentation and commenting expert.", "role": "add documentation and comments"},
        {"name": "LoggerImplementer", "persona": "Logging system expert.", "role": "implement logging"},
        {"name": "TestWriter", "persona": "Unit and integration test expert.", "role": "write tests"},
    ],
    "Review and Deployment": [
        {"name": "CodeReviewApprover", "persona": "Code quality gatekeeper.", "role": "review and approve code changes"},
        {"name": "Deployer", "persona": "Deployment process expert.", "role": "deploy code"},
        {"name": "Monitor", "persona": "Production monitoring expert.", "role": "monitor performance and issues"},
    ],
}

# Default agents if not specified per phase
DEFAULT_AGENTS: List[Dict[str, str]] = [
    {"name": "GeneralAgent", "persona": "A helpful AI assistant.", "role": "assist with the current task"},
]

# Initial prompts (can be refined)
INITIAL_SYSTEM_PROMPT = """You are part of a multi-agent system collaborating on a code improvement task.
Your goal is to contribute to the shared canvas based on your assigned role and the current phase of the project.
Be concise and focus on your specific task within the current phase.
The current phase is: {phase}
Your role in this phase is: {role}
"""

INITIAL_SESSION_PROMPT = """We are working on improving the following code:
{initial_code}

Based on the current phase ({phase}) and your role ({role}), provide your contribution to the canvas.
Remember to be concise and focused.
"""

# --- Main Orchestration Logic ---

def load_code_from_file(filepath: str) -> str:
    """Loads code content from a specified file."""
    try:
        with open(filepath, 'r') as f:
            return f.read()
    except FileNotFoundError:
        logger.error(f"Code file not found: {filepath}")
        return ""
    except Exception as e:
        logger.error(f"Error loading code file {filepath}: {e}")
        return ""

def main():
    logger.info("Starting multi-agent code improvement orchestration.")

    # --- Initialize ---
    # Load the initial code to be improved
    code_filepath = "sample_code.py" # <--- Specify your sample code file here
    initial_code = load_code_from_file(code_filepath)
    if not initial_code:
        logger.error("No initial code loaded. Exiting.")
        return

    # Initialize the shared canvas with the initial code
    canvas = Canvas(initial_content=initial_code)
    logger.info("Canvas initialized with initial code.")

    # --- Execute Phases ---
    for phase in PLAN_PHASES:
        logger.info(f"--- Starting Phase: {phase} ---")

        # Get agents for the current phase, or use default agents
        agent_configs = AGENT_ROLES_PER_PHASE.get(phase, DEFAULT_AGENTS)
        agents: List[Agent] = []
        for config in agent_configs:
            # Assuming Agent class takes name, persona, and role
            agents.append(Agent(name=config["name"], model=None, persona=config["persona"], role=config["role"]))
        logger.info(f"Initialized {len(agents)} agents for phase: {phase}")

        # Prepare prompts for the current phase
        system_prompt = INITIAL_SYSTEM_PROMPT.format(phase=phase, role="collaborate on the task") # System prompt is general
        # Session prompt includes the initial code and phase/role context for each agent
        session_prompt_template = INITIAL_SESSION_PROMPT

        # Agent Collaboration Loop for the phase
        phase_contributions: List[str] = []
        for agent in agents:
            logger.info(f"Agent {agent.name} ({agent.role}) is contributing to phase: {phase}")
            # Pass the current phase to the agent's generate_response method
            contribution = agent.generate_response(
                system_prompt=system_prompt,
                session_prompt=session_prompt_template.format(initial_code=canvas.get_content(), phase=phase, role=agent.role),
                canvas="\n\n\n".join(phase_contributions), # Pass current canvas content
                phase=phase # Pass the current phase
            )
            phase_contributions.append(contribution)
            logger.info(f"Agent {agent.name} contribution received.")

        # Aggregate contributions for the phase
        logger.info(f"Aggregating contributions for phase: {phase}")
        # The Canvas class handles the aggregation logic using an LLM
        canvas.aggregate_contribution(contribution="\n\n\n".join(phase_contributions))  # Replace None with actual model if needed
        logger.info(f"Canvas updated after phase: {phase}")

        # Optional: Save canvas state after each phase
        # with open(f"canvas_after_{phase.replace(' ', '_').lower()}.md", "w") as f:
        #     f.write(canvas.get_content())
        # logger.info(f"Canvas state saved to canvas_after_{phase.replace(' ', '_').lower()}.md")


    logger.info("--- Orchestration Complete ---")
    logger.info("Final Canvas Content:")
    print(canvas.get_content()) # Print the final result

    # Optional: Save final canvas state
    # with open("final_improved_code.md", "w") as f:
    #     f.write(canvas.get_content())
    # logger.info("Final canvas state saved to final_improved_code.md")


if __name__ == "__main__":
    main()
