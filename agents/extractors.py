import re

def extract_revised_system_prompt(contribution):
    """
    Extracts the revised system prompt from PromptDev's contribution.
    Looks for a heading or marker and returns the following section.
    """
    match = re.search(
        r"\*?\*?.*System Prompt.*\*?\*?\s*\n+([\s\S]*?)(?:\n\-{3,}\n|\n{3,}|\Z)", contribution
    )
    if match:
        return match.group(1).strip()
    else:
        return contribution.strip()

def extract_updated_canvas(update):
    """
    Extracts the updated canvas from a contribution.
    """
    match = re.search(
        r"\*?\*?.*Canvas.*\*?\*?\s*\n+([\s\S]*?)(?:\n\-{3,}\n|\n{3,}|\Z)", update
    )
    if match:
        return match.group(1).strip()
    else:
        return update.strip()
