#!/usr/bin/env python3
"""
Quick Resume Script for Notes Manager Knowledge Graph Project

This script provides a fast way to restore project context after a compact operation.
It reads session_state.json and generates a concise summary of the current project state.
"""

import json
# os module is used in the module, keep import
from datetime import datetime


def load_session_state():
    """Load the current session state from the session_state.json file."""
    try:
        with open("data/session_state.json", "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("Error: Could not load session state. File missing or invalid.")
        return None


def get_kg_stats():
    """Get basic statistics from the knowledge graph."""
    try:
        with open("data/kg.json", "r") as f:
            kg = json.load(f)
            entity_count = len(kg.get("entities", []))
            relationship_count = len(kg.get("relationships", []))
            return entity_count, relationship_count
    except (FileNotFoundError, json.JSONDecodeError):
        return "Unknown", "Unknown"


def get_processed_files():
    """Get the list of processed files from the registry."""
    try:
        with open("data/registry.json", "r") as f:
            registry = json.load(f)
            return len(registry.get("processed_files", {}))
    except (FileNotFoundError, json.JSONDecodeError):
        return "Unknown"


def main():
    """Generate a concise summary of the current project state."""
    state = load_session_state()
    if not state:
        return
    
    entity_count, relationship_count = get_kg_stats()
    files_processed = get_processed_files()
    
    # Update state if it doesn't match current files
    if entity_count != "Unknown" and state["project_state"]["entity_count"] != entity_count:
        state["project_state"]["entity_count"] = entity_count
        state["project_state"]["relationship_count"] = relationship_count
        state["project_state"]["files_processed"] = files_processed
        state["project_state"]["last_updated"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        with open("data/session_state.json", "w") as f:
            json.dump(state, f, indent=2)
    
    # Print summary
    print("\n=== Notes Manager Knowledge Graph - Quick Resume ===\n")
    print(f"Last Updated: {state['project_state']['last_updated']}")
    print(f"Files Processed: {state['project_state']['files_processed']}")
    print(f"Entity Count: {state['project_state']['entity_count']}")
    print(f"Relationship Count: {state['project_state']['relationship_count']}")
    print(f"\nCurrent Focus: {state['project_state']['current_focus']}")
    
    print("\nNext Tasks:")
    for i, task in enumerate(state['project_state']['next_tasks'], 1):
        print(f"  {i}. {task}")
    
    print("\nEntity Types:", ", ".join(state['taxonomy_summary']['entity_types']))
    
    print("\nRecent Challenges:")
    for challenge, description in state['recent_challenges'].items():
        print(f"  - {challenge}: {description}")
    
    print("\nProcessing Rules:")
    for rule, description in state['processing_rules'].items():
        print(f"  - {rule}: {description}")
    
    print("\n=== Ready to Continue ===\n")


if __name__ == "__main__":
    main()