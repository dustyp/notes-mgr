# Team Workflow for Notes Manager

## Development Process

1. Check the feature tickets in the `/features` directory
2. Choose a feature to work on or create a new feature ticket
3. Create a feature branch (`feature/XXX-feature-name`)
4. Implement the feature with tests
5. Submit a PR for review

## Coding Standards

- Follow PEP 8 style guidelines
- Add type hints to function signatures
- Write docstrings for all functions and classes
- Include tests for new functionality
- Name features and scripts with "-inator" suffix (Heinz's rule)

## Pull Request Process

1. Ensure all tests pass
2. Update documentation if needed
3. Link to the relevant feature ticket
4. Request review from the project owner

## Feature Ticket Format

Feature tickets should follow this format:
```
# FEATURE-XXX: Feature Name

## Status: [Draft/In Progress/Ready for Review/Complete]
## Priority: [Low/Medium/High]
## Estimated Effort: [Low/Medium/High]
## Prerequisite for: [Other feature tickets, if applicable]

## Description
Brief description of the feature

## Motivation
- Why is this feature needed?
- What problems does it solve?

## Technical Design
Detailed technical approach

## Implementation Plan
Step-by-step implementation guide

## Questions/Feedback Needed
List any open questions or areas where feedback is needed

## Comments
Thread of comments on the feature ticket
```