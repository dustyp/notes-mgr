#!/usr/bin/env python3
"""
Resume State Script for Notes Manager Knowledge Graph Project

This script generates a compact project state summary for Claude to quickly restore context
after a compact operation or new session. It produces a Markdown summary that can be
included in the first prompt to Claude after a context reset.
"""

import json
import os
from datetime import datetime


def load_session_state():
    """Load the current session state from the session_state.json file."""
    try:
        with open("data/session_state.json", "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("Error: Could not load session state. Run update_state.py first.")
        return None


def generate_claude_state_summary():
    """Generate a compact state summary for Claude."""
    state = load_session_state()
    if not state:
        return None
    
    summary = [
        "# Notes Manager KG Project State Summary",
        "",
        f"*Last updated: {state['project_state']['last_updated']}*",
        "",
        "## Current Status",
        f"- **Files processed:** {state['project_state']['files_processed']}",
        f"- **Entity count:** {state['project_state']['entity_count']}",
        f"- **Relationship count:** {state['project_state']['relationship_count']}",
        f"- **Current focus:** {state['project_state']['current_focus']}",
        "",
        "## Next Tasks",
    ]
    
    for task in state['project_state']['next_tasks']:
        summary.append(f"- {task}")
    
    summary.extend([
        "",
        "## Taxonomy",
        f"- **Entity types:** {', '.join(state['taxonomy_summary']['entity_types'])}",
        f"- **Relationship types:** Key types include {', '.join(state['taxonomy_summary']['relationship_types'][:5])} "
        f"and {len(state['taxonomy_summary']['relationship_types']) - 5} more",
        "",
        "## Implementation Approach",
        "- **Core approach:** Prompt-only Claude extraction with minimal Python",
        "- **Dynamic taxonomy:** Expanding entity/relationship types as discovered",
        "- **Focus:** Precision over recall for entity extraction",
        "- **Processing:** Currently addressing challenges with large file chunking and entity candidate tracking",
        "",
        "## Key Components",
        "- `kg.json`: Main knowledge graph storage with entities, relationships, notes, metadata",
        "- `registry.json`: Tracks processed files with timestamps and hashes",
        "- `extraction.md`: Prompt template for entity/relationship extraction",
        "- `processed-notes/`: Directory with reformatted notes containing frontmatter and entity links",
        "- `kg_readable.md`: Human-readable view of the knowledge graph",
        "",
        "## Rule Reminders"
    ])
    
    for rule, description in state['processing_rules'].items():
        summary.append(f"- **{rule}:** {description}")
    
    return "\n".join(summary)


def main():
    """Generate the Claude state summary and save to a file."""
    summary = generate_claude_state_summary()
    if not summary:
        return
    
    # Save to a file
    os.makedirs("data/state", exist_ok=True)
    filename = f"data/state/claude_resume_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    with open(filename, "w") as f:
        f.write(summary)
    
    # Also save as the current version
    with open("data/state/current_resume.md", "w") as f:
        f.write(summary)
    
    print(f"Generated Claude resume state in {filename}")
    print("Also saved as data/state/current_resume.md")
    print("\nCopy and paste the content below into your first prompt after a Claude compact:\n")
    print(summary)


if __name__ == "__main__":
    main()