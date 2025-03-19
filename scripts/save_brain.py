#!/usr/bin/env python3
"""
Save Brain Script for Notes Manager Knowledge Graph Project

This script is designed to be called when the user types
"Get Ready for Bed gang" to Claude. It saves the current project state
to session_state.json and generates an updated context summary.
"""

import json
import os
import sys
from datetime import datetime
import argparse


def update_project_state(current_focus=None, next_tasks=None, note=None):
    """Update the project state in session_state.json."""
    # Load current session state
    try:
        with open("data/session_state.json", "r") as f:
            state = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("Error: Could not load session state. Creating new file.")
        state = create_default_state()
    
    # Get current KG stats
    entity_count, relationship_count = get_kg_stats()
    files_processed = get_processed_files()
    
    # Update state
    state["project_state"]["entity_count"] = entity_count
    state["project_state"]["relationship_count"] = relationship_count
    state["project_state"]["files_processed"] = files_processed
    state["project_state"]["last_updated"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    
    if current_focus:
        state["project_state"]["current_focus"] = current_focus
    
    if next_tasks:
        state["project_state"]["next_tasks"] = next_tasks
    
    # Update taxonomy summary from kg.json
    update_taxonomy_summary(state)
    
    # Add a note if provided
    if note:
        if "notes" not in state:
            state["notes"] = []
        state["notes"].append({
            "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "content": note
        })
    
    # Save updated state
    with open("data/session_state.json", "w") as f:
        json.dump(state, f, indent=2)
    
    # Also generate the current_resume.md file
    generate_resume_file(state)
    
    print(f"Updated session state with {entity_count} entities and {relationship_count} relationships.")


def get_kg_stats():
    """Get basic statistics from the knowledge graph."""
    try:
        with open("data/kg.json", "r") as f:
            kg = json.load(f)
            entity_count = len(kg.get("entities", []))
            relationship_count = len(kg.get("relationships", []))
            return entity_count, relationship_count
    except (FileNotFoundError, json.JSONDecodeError):
        return 0, 0


def get_processed_files():
    """Get the list of processed files from the registry."""
    try:
        with open("data/registry.json", "r") as f:
            registry = json.load(f)
            return len(registry.get("processed_files", {}))
    except (FileNotFoundError, json.JSONDecodeError):
        return 0


def update_taxonomy_summary(state):
    """Update the taxonomy summary from kg.json."""
    try:
        with open("data/kg.json", "r") as f:
            kg = json.load(f)
            
            # Extract unique entity types
            entity_types = set()
            for entity in kg.get("entities", []):
                if "type" in entity:
                    entity_types.add(entity["type"].lower())
            
            # Extract unique relationship types
            relationship_types = set()
            for relationship in kg.get("relationships", []):
                if "type" in relationship:
                    relationship_types.add(relationship["type"].lower())
            
            # Update the state
            state["taxonomy_summary"]["entity_types"] = sorted(list(entity_types))
            state["taxonomy_summary"]["relationship_types"] = sorted(list(relationship_types))
    except (FileNotFoundError, json.JSONDecodeError):
        print("Warning: Could not update taxonomy from kg.json.")


def create_default_state():
    """Create a default session state if none exists."""
    return {
        "project_state": {
            "last_updated": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "files_processed": 0,
            "entity_count": 0,
            "relationship_count": 0,
            "current_focus": "initial setup",
            "next_tasks": [
                "Process initial note files",
                "Review extracted entities and relationships",
                "Update taxonomy as needed"
            ]
        },
        "taxonomy_summary": {
            "entity_types": ["person", "organization", "project", "concept"],
            "relationship_types": ["works_for", "reports_to", "leads", "mentions", "related_to"]
        },
        "implementation_summary": {
            "approach": "prompt-only",
            "current_components": {
                "extraction_prompt": "Identifies entities/relationships with dynamic taxonomy",
                "kg_json": "JSON structure with entities, relationships, notes, metadata",
                "registry": "Tracks processed files with timestamps and hashes",
                "reformatted_notes": "Notes with frontmatter, links and topic tags",
                "human_readable_kg": "kg_readable.md for easy review"
            },
            "performance_improvements": {
                "file_chunking": "Break large files at logical section boundaries",
                "change_detection": "Use MD5 hashing to skip unchanged files",
                "entity_resolution": "Implement candidate tracking before promotion",
                "prompt_optimization": "Create specialized prompts for different extraction tasks"
            }
        },
        "recent_challenges": {
            "large_files": "API connection closed for files >600 lines",
            "solution": "Implement chunking strategy for longer files"
        },
        "processing_rules": {
            "prompt_only": "Use Claude prompt-based extraction, minimize Python code",
            "dynamic_taxonomy": "Update extraction prompt with new entity/relationship types",
            "precision_focus": "Prioritize precision over recall for entity extraction",
            "file_protection": "Update existing files rather than creating duplicates"
        },
        "notes": []
    }


def generate_resume_file(state):
    """Generate a Claude-friendly resume file from the state."""
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
    
    # Add recent notes if they exist
    if "notes" in state and state["notes"]:
        summary.extend(["", "## Recent Notes"])
        # Only include the last 3 notes
        for note in state["notes"][-3:]:
            summary.append(f"- *{note['timestamp']}*: {note['content']}")
    
    # Save to file
    os.makedirs("data/state", exist_ok=True)
    with open("data/state/current_resume.md", "w") as f:
        f.write("\n".join(summary))


def main():
    """Command-line interface for saving brain state."""
    parser = argparse.ArgumentParser(description="Save Notes Manager KG brain state")
    parser.add_argument("--focus", help="Current project focus", default=None)
    parser.add_argument("--tasks", help="Comma-separated list of next tasks", default=None)
    parser.add_argument("--note", help="Add a note about current progress", default=None)
    
    args = parser.parse_args()
    
    next_tasks = args.tasks.split(",") if args.tasks else None
    update_project_state(args.focus, next_tasks, args.note)
    
    print("Brain state saved! Ready for future restoration.")
    print("Use 'Wake up gang' to restore this state later.")


if __name__ == "__main__":
    sys.exit(main())