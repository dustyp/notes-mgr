#!/bin/bash
# Resume Project Script for Notes Manager Knowledge Graph Project
# This script helps quickly resume work on the project after a compact operation.

echo "=== Notes Manager Knowledge Graph Project Resume ==="
echo "Checking project state..."

# Ensure we're in the project root directory
cd "$(dirname "$0")/.." || exit 1

# Check if session_state.json exists
if [ ! -f "data/session_state.json" ]; then
    echo "No session state found. Running update_state.py to create one..."
    python3 scripts/update_state.py
fi

# Display current project state
python3 scripts/quick_resume.py

# List files to be processed
echo -e "\nFiles to be processed:"
processed_files=$(grep -o '"[^"]*\.md"' data/registry.json | sed 's/"//g')
all_files=$(find notes -name "*.md" -type f | sort)

echo "Files remaining to process:"
for file in $all_files; do
    filename=$(basename "$file")
    if ! echo "$processed_files" | grep -q "$filename"; then
        echo "  - $filename"
    fi
done

# Ask if user wants to update the project state
echo -e "\nDo you want to update the project state? (y/n)"
read -r response
if [[ "$response" =~ ^[Yy]$ ]]; then
    echo "Enter current focus (leave empty to keep current):"
    read -r focus
    
    echo "Enter next tasks (comma-separated, leave empty to keep current):"
    read -r tasks
    
    focus_arg=""
    tasks_arg=""
    
    if [ -n "$focus" ]; then
        focus_arg="--focus \"$focus\""
    fi
    
    if [ -n "$tasks" ]; then
        tasks_arg="--tasks \"$tasks\""
    fi
    
    if [ -n "$focus_arg" ] || [ -n "$tasks_arg" ]; then
        eval "python3 scripts/update_state.py $focus_arg $tasks_arg"
        python3 scripts/quick_resume.py
    fi
fi

echo -e "\n=== Ready to continue work on the project ==="