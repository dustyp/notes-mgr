#!/usr/bin/env python3
"""
Fix Brain Script for Notes Manager Knowledge Graph Project

This script is designed to be called as a shell alias when the user types
"Wake up gang" to Claude. It automatically generates the project
state context summary for Claude to consume.
"""

import json
import os
import sys
# No datetime import needed in this file


def load_session_state():
    """Load the current session state from the session_state.json file."""
    try:
        with open("data/session_state.json", "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("Error: Could not load session state. Run update_state.py first.")
        return None


def update_from_kg_if_needed():
    """Update session_state.json if it's outdated compared to kg.json."""
    try:
        session_state_file = "data/session_state.json"
        kg_file = "data/kg.json"
        
        # Check if we need to update the session state
        if not os.path.exists(session_state_file):
            print("Session state not found. Creating from current knowledge graph.")
            os.system("python3 scripts/update_state.py")
            return
        
        # Check modification times
        kg_mtime = os.path.getmtime(kg_file)
        state_mtime = os.path.getmtime(session_state_file)
        
        if kg_mtime > state_mtime:
            print("Knowledge graph is newer than session state. Updating...")
            os.system("python3 scripts/update_state.py")
    except Exception as e:
        print(f"Warning: Could not check for updates: {e}")


def generate_claude_state_summary():
    """Generate a compact state summary for Claude."""
    update_from_kg_if_needed()
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
        return 1
    
    # Save to a file
    os.makedirs("data/state", exist_ok=True)
    filename = "data/state/current_resume.md"
    with open(filename, "w") as f:
        f.write(summary)
    
    print("Brain fixed! Project context has been updated.")
    print(f"Summary saved to {filename}")
    print("Ready to continue with the project.")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())