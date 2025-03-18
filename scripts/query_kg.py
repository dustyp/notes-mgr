#!/usr/bin/env python3
"""
Knowledge Graph Query Tool

A simple Python script for exploring the knowledge graph.

Usage:
  python query_kg.py [command] [args...]

Commands:
  find entity <name>          - Find and display an entity
  find related <name>         - Show entities related to the specified one
  list types                  - Show all entity types
  list entities <type>        - List all entities of a specific type
  search <term>               - Search across entities and relationships
  info                        - Show knowledge graph statistics
  help                        - Show this help message

Examples:
  python query_kg.py find entity Amplitude
  python query_kg.py find related Spenser
  python query_kg.py list types
  python query_kg.py list entities person
  python query_kg.py search pricing
  python query_kg.py info
"""

import argparse
import json
import sys
from typing import Dict, Any

DEFAULT_KG_PATH = 'data/merged_kg.json'


def load_knowledge_graph(file_path: str = DEFAULT_KG_PATH) -> Dict[str, Any]:
    """Load the knowledge graph from the specified JSON file."""
    try:
        with open(file_path, 'r') as f:
            data: Dict[str, Any] = json.load(f)
            return data
    except FileNotFoundError:
        print(f"Error: Knowledge graph file '{file_path}' not found")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in knowledge graph file '{file_path}'")
        sys.exit(1)


def find_entity(kg: Dict, name: str) -> None:
    """Find and display an entity by name."""
    name = name.lower()
    matches = []
    
    for entity in kg.get('entities', []):
        if name in entity.get('name', '').lower():
            matches.append(entity)
    
    if not matches:
        print(f"No entities found matching '{name}'")
        return
    
    for entity in matches:
        print(f"\n{entity['name']} ({entity['type']})")
        print("="*40)
        print(f"ID: {entity['id']}")
        print(f"Source: {entity['source_file']}")
        print(f"Confidence: {entity['confidence']}")
        
        print("\nProperties:")
        for key, value in entity.get('properties', {}).items():
            if isinstance(value, list):
                print(f"  - {key}: {', '.join(value)}")
            else:
                print(f"  - {key}: {value}")
        
        # Find relationships for this entity
        print("\nRelationships:")
        rel_found = False
        for rel in kg.get('relationships', []):
            if rel['source'] == entity['id']:
                target = next((e for e in kg.get('entities', []) if e['id'] == rel['target']), None)
                if target:
                    print(f"  - {rel['type']} → {target['name']} ({target['type']})")
                    rel_found = True
            elif rel['target'] == entity['id']:
                source = next((e for e in kg.get('entities', []) if e['id'] == rel['source']), None)
                if source:
                    print(f"  - {source['name']} ({source['type']}) → {rel['type']}")
                    rel_found = True
        
        if not rel_found:
            print("  No relationships found")


def find_related(kg: Dict, name: str) -> None:
    """Show entities related to the specified one."""
    name = name.lower()
    
    # Find matching entities
    entities = []
    for entity in kg.get('entities', []):
        if name in entity.get('name', '').lower():
            entities.append(entity)
    
    if not entities:
        print(f"No entities found matching '{name}'")
        return
    
    # For each matching entity, find related entities
    for entity in entities:
        print(f"\nEntities related to {entity['name']} ({entity['type']}):")
        print("="*50)
        
        related = []
        
        # Check relationships where entity is source
        for rel in kg.get('relationships', []):
            if rel['source'] == entity['id']:
                target = next((e for e in kg.get('entities', []) if e['id'] == rel['target']), None)
                if target:
                    related.append({
                        'entity': target,
                        'relationship': rel['type'],
                        'direction': 'outgoing'
                    })
        
        # Check relationships where entity is target
        for rel in kg.get('relationships', []):
            if rel['target'] == entity['id']:
                source = next((e for e in kg.get('entities', []) if e['id'] == rel['source']), None)
                if source:
                    related.append({
                        'entity': source,
                        'relationship': rel['type'],
                        'direction': 'incoming'
                    })
        
        if not related:
            print("  No related entities found")
        else:
            # Sort by entity name
            related.sort(key=lambda x: x['entity']['name'])
            for item in related:
                if item['direction'] == 'outgoing':
                    print(f"  → {item['relationship']} → {item['entity']['name']} ({item['entity']['type']})")
                else:
                    print(f"  ← {item['relationship']} ← {item['entity']['name']} ({item['entity']['type']})")


def list_types(kg: Dict) -> None:
    """Show all entity types."""
    types = set()
    for entity in kg.get('entities', []):
        types.add(entity.get('type', 'unknown'))
    
    rel_types = set()
    for rel in kg.get('relationships', []):
        rel_types.add(rel.get('type', 'unknown'))
    
    print("\nEntity Types:")
    print("="*40)
    for t in sorted(types):
        count = sum(1 for e in kg.get('entities', []) if e.get('type') == t)
        print(f"  - {t} ({count} entities)")
    
    print("\nRelationship Types:")
    print("="*40)
    for t in sorted(rel_types):
        count = sum(1 for r in kg.get('relationships', []) if r.get('type') == t)
        print(f"  - {t} ({count} relationships)")


def list_entities_by_type(kg: Dict, entity_type: str) -> None:
    """List all entities of a specific type."""
    entity_type = entity_type.lower()
    
    entities = []
    for entity in kg.get('entities', []):
        if entity.get('type', '').lower() == entity_type:
            entities.append(entity)
    
    if not entities:
        print(f"No entities found of type '{entity_type}'")
        return
    
    print(f"\nEntities of type '{entity_type}':")
    print("="*40)
    
    # Sort by name
    entities.sort(key=lambda x: x.get('name', ''))
    
    for entity in entities:
        source_file = entity.get('source_file', 'unknown')
        print(f"  - {entity['name']} (from {source_file})")


def search(kg: Dict, term: str) -> None:
    """Search across entities and relationships."""
    term = term.lower()
    results = []
    
    # Search in entities
    for entity in kg.get('entities', []):
        if term in json.dumps(entity).lower():
            results.append({
                'type': 'entity',
                'data': entity
            })
    
    # Search in relationships
    for rel in kg.get('relationships', []):
        if term in json.dumps(rel).lower():
            # Get the source and target entities for display
            source = next((e for e in kg.get('entities', []) if e['id'] == rel['source']), None)
            target = next((e for e in kg.get('entities', []) if e['id'] == rel['target']), None)
            
            if source and target:
                results.append({
                    'type': 'relationship',
                    'data': rel,
                    'source': source,
                    'target': target
                })
    
    print(f"\nSearch results for '{term}':")
    print("="*40)
    
    if not results:
        print("  No results found")
        return
    
    for result in results:
        if result['type'] == 'entity':
            entity = result['data']
            print(f"\nEntity: {entity['name']} ({entity['type']})")
            print(f"  Source: {entity.get('source_file', 'unknown')}")
            
            # Display properties that match the search term
            matching_props = {k: v for k, v in entity.get('properties', {}).items()
                              if term in str(k).lower() or term in str(v).lower()}
            if matching_props:
                print("  Matching properties:")
                for key, value in matching_props.items():
                    print(f"    - {key}: {value}")
        
        elif result['type'] == 'relationship':
            rel = result['data']
            source = result['source']
            target = result['target']
            print(f"\nRelationship: {source['name']} → {rel['type']} → {target['name']}")
            print(f"  Source: {rel.get('source_file', 'unknown')}")
            print(f"  Confidence: {rel.get('confidence', 'unknown')}")


def show_info(kg: Dict) -> None:
    """Show knowledge graph statistics."""
    entity_count = len(kg.get('entities', []))
    rel_count = len(kg.get('relationships', []))
    note_count = len(kg.get('notes', {}))
    
    entity_types = set(e.get('type') for e in kg.get('entities', []))
    rel_types = set(r.get('type') for r in kg.get('relationships', []))
    
    metadata = kg.get('metadata', {})
    
    print("\nKnowledge Graph Statistics:")
    print("="*40)
    print(f"Entities: {entity_count}")
    print(f"Relationships: {rel_count}")
    print(f"Notes: {note_count}")
    print(f"Entity types: {len(entity_types)}")
    print(f"Relationship types: {len(rel_types)}")
    
    print("\nMetadata:")
    for key, value in metadata.items():
        print(f"  - {key}: {value}")


def main():
    parser = argparse.ArgumentParser(description='Knowledge Graph Query Tool')
    parser.add_argument('command', help='Command to execute')
    parser.add_argument('args', nargs='*', help='Additional arguments for the command')
    parser.add_argument('--kg', default=DEFAULT_KG_PATH, help='Path to knowledge graph JSON file')
    
    args = parser.parse_args()
    
    # Load knowledge graph
    kg = load_knowledge_graph(args.kg)
    
    # Process command
    if args.command == 'find':
        if len(args.args) < 2:
            print("Error: 'find' command requires at least 2 arguments")
            print("Usage: find entity <name> or find related <name>")
            return
        
        sub_command = args.args[0]
        name = ' '.join(args.args[1:])
        
        if sub_command == 'entity':
            find_entity(kg, name)
        elif sub_command == 'related':
            find_related(kg, name)
        else:
            print(f"Error: Unknown sub-command '{sub_command}' for 'find'")
            print("Usage: find entity <name> or find related <name>")
    
    elif args.command == 'list':
        if not args.args:
            print("Error: 'list' command requires a sub-command")
            print("Usage: list types or list entities <type>")
            return
        
        sub_command = args.args[0]
        
        if sub_command == 'types':
            list_types(kg)
        elif sub_command == 'entities':
            if len(args.args) < 2:
                print("Error: 'list entities' requires an entity type")
                print("Usage: list entities <type>")
                return
            entity_type = args.args[1]
            list_entities_by_type(kg, entity_type)
        else:
            print(f"Error: Unknown sub-command '{sub_command}' for 'list'")
            print("Usage: list types or list entities <type>")
    
    elif args.command == 'search':
        if not args.args:
            print("Error: 'search' command requires a search term")
            print("Usage: search <term>")
            return
        
        term = ' '.join(args.args)
        search(kg, term)
    
    elif args.command == 'info':
        show_info(kg)
    
    elif args.command == 'help':
        print(__doc__)
    
    else:
        print(f"Error: Unknown command '{args.command}'")
        print("Use 'help' to see available commands")


if __name__ == '__main__':
    main()