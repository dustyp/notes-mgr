#!/usr/bin/env python3
"""
Update State Script for Notes Manager Knowledge Graph Project

This script updates the session_state.json file with the current state of the project.
It should be run after significant changes to the knowledge graph or project state.
"""

import json
# os import can be removed as it's not used
from datetime import datetime
import argparse


def update_project_state(current_focus=None, next_tasks=None):
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
    
    # Save updated state
    with open("data/session_state.json", "w") as f:
        json.dump(state, f, indent=2)
    
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
        }
    }


def add_challenge(challenge, description):
    """Add a challenge to the session state."""
    try:
        with open("data/session_state.json", "r") as f:
            state = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("Error: Could not load session state. Creating new file.")
        state = create_default_state()
    
    state["recent_challenges"][challenge] = description
    
    with open("data/session_state.json", "w") as f:
        json.dump(state, f, indent=2)
    
    print(f"Added challenge: {challenge}")


def update_rules(rule, description):
    """Update processing rules in the session state."""
    try:
        with open("data/session_state.json", "r") as f:
            state = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("Error: Could not load session state. Creating new file.")
        state = create_default_state()
    
    state["processing_rules"][rule] = description
    
    with open("data/session_state.json", "w") as f:
        json.dump(state, f, indent=2)
    
    print(f"Updated rule: {rule}")


def main():
    """Command-line interface for updating session state."""
    parser = argparse.ArgumentParser(description="Update Notes Manager KG session state")
    parser.add_argument("--focus", help="Current project focus", default=None)
    parser.add_argument("--tasks", help="Comma-separated list of next tasks", default=None)
    parser.add_argument("--add-challenge", nargs=2, metavar=("NAME", "DESCRIPTION"),
                        help="Add a challenge to the session state")
    parser.add_argument("--add-rule", nargs=2, metavar=("NAME", "DESCRIPTION"),
                        help="Add a processing rule to the session state")
    
    args = parser.parse_args()
    
    if args.add_challenge:
        add_challenge(args.add_challenge[0], args.add_challenge[1])
        return
    
    if args.add_rule:
        update_rules(args.add_rule[0], args.add_rule[1])
        return
    
    next_tasks = args.tasks.split(",") if args.tasks else None
    update_project_state(args.focus, next_tasks)


if __name__ == "__main__":
    main()