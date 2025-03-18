# Notes Manager Knowledge Graph

A system for extracting structured information from markdown notes and building a knowledge graph.

## Features

- Process markdown notes to extract entities and relationships
- Build and maintain a knowledge graph structure
- Support querying and exploration of the knowledge graph
- Optimize performance with selective file processing
- Dynamic taxonomy expansion for entity and relationship types

## Installation

```bash
# Clone the repository
git clone https://github.com/heinzdoofenshmirtz-inator/notes-mgr.git
cd notes-mgr

# Install dependencies
pip install -r requirements.txt
```

## Usage

```bash
# Process notes
python scripts/notes-to-kg.py --input-dir notes/ --output data/kg.json

# Query the knowledge graph
python scripts/query_kg.py --entity "Person"

# Update project state
python scripts/update_state.py
```

## Development Workflow

1. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes and add tests

3. Run tests locally:
   ```bash
   pytest --cov=scripts
   ```

4. Commit changes with descriptive messages:
   ```bash
   git commit -m "Add your descriptive message here"
   ```

5. Push to your branch:
   ```bash
   git push origin feature/your-feature-name
   ```

6. Create a Pull Request for review

## Project Structure

- `/notes/` - Sample markdown notes for processing
- `/scripts/` - Python scripts for processing notes
- `/data/` - Output directory for generated knowledge graph
- `/tests/` - Test suite
- `/features/` - Feature documentation and specifications
- `/processed-notes/` - Reformatted notes with frontmatter and links

## Brain State Management

- `scripts/fix_brain.py` - Restore context after reset
- `scripts/save_brain.py` - Save state with progress notes
- `scripts/resume_state.py` - Generate context summaries

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for team workflow guidelines.