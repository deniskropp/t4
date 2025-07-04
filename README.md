# Multi-Agent Collaboration Prototype

System uses agents. Agents collaborate. Shared canvas holds work. Adapting for code improvement.

## Features

*   Multi-agent system.
*   Shared canvas.
*   Phase workflow.
*   Structured logging (JSONL).
*   Extensible agents.

## Code Improvement Plan

Based on "Task-Agnostic Code Improvement Plan". Plan guides phases.

## Project Structure

*   `main.py`: Original web design demo.
*   `main_orchestrator.py`: Code improvement workflow. Runs phases.
*   `agents/agent.py`: Agent base class. Defines agent.
*   `agents/canvas.py`: Merges agent work. Updates canvas.
*   `agents/extractors.py`: Gets data from agent output.
*   `agents/logging_utils.py`: Sets up JSONL logs.
*   `files/f-Code Improvement Task Agnostic Plan.md`: The plan document.
*   `sample_code.py`: Example code for agents.

## Setup

Need Python. Need Ollama.
Install deps: `pip install colorama ollama`

## Usage

Run `python main_orchestrator.py`.
Agents process `sample_code.py`.
Output shows progress.
Logs are JSONL.

## Extending

Add agents in `get_agents_for_phase`.
Add phases to list.

## Notes

Prototype state.
Canvas is text.
No file writes yet.
