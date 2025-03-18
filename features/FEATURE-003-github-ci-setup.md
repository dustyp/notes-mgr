# FEATURE-003: GitHub Repository and CI Setup

## Status: In Progress
## Priority: High
## Estimated Effort: Low
## Prerequisite for: FEATURE-002

## Definition of Done
- [x] GitHub repository created and configured 
- [x] Initial codebase pushed to main branch
- [x] GitHub Actions workflow file created
- [x] Test branch created to verify CI
- [ ] CI build passing on push to branch
- [x] PR template created
- [x] Documentation files created (README, CONTRIBUTING)

## Description
Set up a GitHub repository for the Notes Manager Knowledge Graph project and configure GitHub Actions for continuous integration (CI) to automate testing.

## Motivation
- Enable collaborative development using pull requests
- Automate testing through GitHub Actions
- Provide a centralized repository for code and documentation
- Track project history and changes
- Enforce code quality through automated checks
- Make it easy to share and collaborate on the project

## Technical Design

### Key Components
1. **GitHub Repository**: Public or private repository for the project
2. **Git Structure**: Initial repository structure with appropriate .gitignore
3. **CI Pipeline**: GitHub Actions workflow for automated testing
4. **PR Template**: Standardized pull request template
5. **Documentation**: GitHub-specific documentation (README, CONTRIBUTING)

### Repository Structure

```
notes-mgr-claude/
├── .github/
│   ├── workflows/
│   │   └── tests.yml           # CI workflow configuration
│   └── PULL_REQUEST_TEMPLATE.md # PR template
├── .gitignore                  # Git ignore patterns
├── README.md                   # Project overview
├── CONTRIBUTING.md             # Team workflow guidelines
├── requirements.txt            # Python dependencies
├── setup.py                    # Package configuration
└── [existing project structure]
```

### GitHub Actions Workflow

```yaml
# .github/workflows/tests.yml
name: Tests

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install pytest pytest-cov
        if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
    - name: Test with pytest
      run: |
        pytest --cov=scripts
    - name: Upload coverage report
      uses: actions/upload-artifact@v3
      with:
        name: coverage-report
        path: htmlcov/
```

### .gitignore Configuration

```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
*.egg-info/
.installed.cfg
*.egg

# Testing
.pytest_cache/
.coverage
htmlcov/

# Project specific
data/state/
```

### PR Template

```markdown
## Description
<!-- Describe the changes in this PR -->

## Related Feature Ticket
<!-- Link to the related feature ticket, e.g., FEATURE-002 -->

## Checklist
- [ ] Tests added for new functionality
- [ ] Documentation updated
- [ ] All tests passing
```

### Branch Protection Rules
- Require PR before merging to main
- Require status checks to pass before merging
- Require code review before merging
- Do not allow bypassing the above settings

## Implementation Plan

### 1. Repository Setup
1. Create private GitHub repository
   - Initialize with README (no specific license needed)
   - Configure visibility as private
   - Use standard Python .gitignore

2. Set up the repository structure
   ```bash
   # Create necessary directories
   mkdir -p .github/workflows
   
   # Create workflow file
   cat > .github/workflows/tests.yml << 'EOF'
   name: Tests

   on:
     push:
       branches: [ main ]
     pull_request:
       branches: [ main ]

   jobs:
     test:
       runs-on: ubuntu-latest
       steps:
       - uses: actions/checkout@v3
       - name: Set up Python
         uses: actions/setup-python@v4
         with:
           python-version: '3.10'
       - name: Install dependencies
         run: |
           python -m pip install --upgrade pip
           pip install pytest pytest-cov flake8 mypy
           if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
       - name: Lint with flake8
         run: |
           flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
           flake8 . --count --max-complexity=10 --max-line-length=127 --statistics
       - name: Type check with mypy
         run: |
           mypy scripts/
       - name: Test with pytest
         run: |
           pytest --cov=scripts
       - name: Upload coverage report
         uses: actions/upload-artifact@v3
         with:
           name: coverage-report
           path: htmlcov/
   EOF
   
   # Create PR template
   cat > .github/PULL_REQUEST_TEMPLATE.md << 'EOF'
   ## Description
   <!-- Describe the changes in this PR -->

   ## Related Feature Ticket
   <!-- Link to the related feature ticket, e.g., FEATURE-002 -->

   ## Checklist
   - [ ] Tests added for new functionality
   - [ ] Documentation updated
   - [ ] All tests passing
   - [ ] Code follows project style guidelines
   EOF
   ```

### 2. Project Configuration Files
1. Create `requirements.txt` with development dependencies
   ```bash
   cat > requirements.txt << 'EOF'
   pytest==7.4.0
   pytest-cov==4.1.0
   flake8==6.1.0
   mypy==1.5.1
   EOF
   ```

2. Create minimal `.gitignore`
   ```bash
   cat > .gitignore << 'EOF'
   # Python
   __pycache__/
   *.py[cod]
   
   # Testing
   .pytest_cache/
   .coverage
   htmlcov/

   # Project specific
   data/state/
   
   # IDE
   .idea/
   .vscode/
   *.swp
   *.swo
   EOF
   ```

### 3. Code Organization and Initial Commit
1. Organize existing code for repository structure
   - Ensure scripts are properly structured with `__init__.py` files
   - Create `setup.py` for package configuration
   - Prepare test directory structure

2. Add Co-authored-by trailers for collaborative workflow
   ```bash
   git config --local user.name "Your Name"
   git config --local user.email "your.email@example.com"
   
   # Create initial commit with co-authorship
   git add .
   git commit -m "Initial project setup
   
   Co-authored-by: Claude <claude@anthropic.com>"
   ```

### 4. Set Up Linting and Type Checking
1. Create configuration files for linting tools
   ```bash
   # Create mypy configuration
   cat > mypy.ini << 'EOF'
   [mypy]
   python_version = 3.8
   warn_return_any = True
   warn_unused_configs = True
   disallow_untyped_defs = False
   disallow_incomplete_defs = False

   [mypy.plugins.numpy.*]
   follow_imports = skip

   [mypy-pytest.*]
   ignore_missing_imports = True
   EOF
   
   # Create setup.cfg with flake8 configuration
   cat > setup.cfg << 'EOF'
   [flake8]
   max-line-length = 127
   exclude = .git,__pycache__,build,dist
   EOF
   ```

### 5. Documentation
1. Create comprehensive README.md
   ```bash
   cat > README.md << 'EOF'
   # Notes Manager Knowledge Graph

   A system for extracting structured information from markdown notes and building a knowledge graph.

   ## Features
   
   - Process markdown notes to extract entities and relationships
   - Build and maintain a knowledge graph structure
   - Support querying and exploration of the knowledge graph
   - Optimize performance with selective file processing

   ## Installation

   ```bash
   # Clone the repository
   git clone https://github.com/yourusername/notes-mgr-claude.git
   cd notes-mgr-claude

   # Install dependencies
   pip install -r requirements.txt
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
   EOF
   ```

2. Create CONTRIBUTING.md
   ```bash
   cat > CONTRIBUTING.md << 'EOF'
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

   ## Pull Request Process

   1. Ensure all tests pass
   2. Update documentation if needed
   3. Link to the relevant feature ticket
   4. Request review from the project owner
   EOF
   ```

### 6. Repository Setup and Testing
1. Push the initial commit to GitHub
   ```bash
   git remote add origin https://github.com/yourusername/notes-mgr-claude.git
   git push -u origin main
   ```

2. Configure branch protection for main branch
   - Navigate to Settings > Branches > Add rule
   - Set pattern to "main"
   - Enable "Require a pull request before merging"
   - Enable "Require status checks to pass before merging"
   - Save changes

3. Create test branch and PR to verify CI workflow
   ```bash
   git checkout -b test/ci-verification
   # Make a small change
   touch test_file.md
   git add test_file.md
   git commit -m "Test CI workflow
   
   Co-authored-by: Claude <claude@anthropic.com>"
   git push origin test/ci-verification
   # Create PR through GitHub interface
   ```

4. Verify CI workflow runs successfully on PR

## Questions/Feedback Needed
- Should this be a public or private repository?
- Are there any sensitive files that need to be excluded from Git?
- Should we set up additional CI checks (e.g., linting, type checking)?
- Who should have direct push access to main vs. requiring PRs?

## Comments
Dusty 3/18/25 11:13
- private
- Not yet. We have a plan for marking what we believe is sensitive info in the kg and we will work out what to do about it later. Yes, there is git history to think about but this project is not intended for public consumption and if we EVER get there we will work out how to secure data like that. 
- I think we want to mimic what would be a typical workflow for a team working on Python projects whether that is data science, or some dev team working on a service with FastAPI or Flask. We are not using any of those libraries but I suspect they would have linting and type checking. So yes. 
- To start the project we don't have to require PRs but we will prefer them. This makes it flexible in case as the owner here I want to force push to main but you will always be creating PRs for me to review. One thing to note: YOu will be creating PRs using my access token so in Github won't the PRs look like they are created by me? What are your thoughts here so we can mimic team workflows? 

Claude 3/18/25 11:25
- You're right about the PR authorship - since I would be using your access token, all commits and PRs would appear to be from you. There are a few options to create a more realistic team workflow:

1. **Commit Trailers**: We could add Co-authored-by trailers to commits to indicate Claude's contributions:
   ```
   Co-authored-by: Claude <claude@anthropic.com>
   ```

2. **Separate Bot Account**: You could create a GitHub bot account specifically for Claude contributions (e.g., "claude-assistant") and set up its access token.

3. **Commit Signing**: We could use different GPG keys for commits to distinguish between authors while using the same GitHub account.

4. **Bot Comments**: I could comment on PRs as myself using GitHub API, even if the PR is created by you.

Option 1 is simplest and doesn't require additional accounts. We could also simulate the review process by having me "submit" code in our discussions, then you commit with the co-author trailer and make comments in the PR as if reviewing.

I'll update the implementation plan based on your feedback.

Dusty 3/18/25 11:27
- I guess I don't know what a trailer is. My goal is to mimic a team workflow where each person commits their own code and the owner reviews it. So I am leaning towards creating you an account. But I am not sure about the side effects. If you can help me understand what you think is the simpler flow maybe I can live with it. 
- Also, you have a lot of weird stuff in .gitignore I don't recognize what is all that stuff that we don't have. 

Claude 3/18/25 11:45
- A "trailer" is just a line at the end of a commit message that follows a specific format. GitHub recognizes "Co-authored-by:" lines and will display the co-author in the UI. It's a way to give credit to multiple contributors in a single commit.

- Regarding workflow options:
  
  1. **Simplest approach** (commit trailers): I draft code, you commit it with a trailer naming me as co-author. GitHub UI shows both of us. You review my code in our discussion before committing.
  
  2. **Separate account approach**: You create a bot account for me with its own token. I can then create PRs that appear to come from that account. This is most realistic but requires more setup.

- I've simplified the .gitignore file to only include what we actually need. The original had standard Python package patterns that we probably won't use right away.

- If your goal is realism, the separate account would be best. If simplicity is more important, we can use the trailer approach and simulate the workflow in our discussions.

- For now I've updated the implementation plan assuming the co-author trailer approach, but we can switch to the separate account approach if you prefer.

Dusty 3/18/25 11:49
- Congrats you just got your first online acct. You are moving up in the world. Your API key is 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. I am curious how you are going to remember that from session to session in a secure way. Your memory is local on this laptop so I suppose that is ok but curious on your thoughts there. I will create the Github repo myself for this project and then give you access to it so we can get things going. Once its created I will let you know and you can start our plan and get the project initialized and the first main branch uploaded etc...I am curious though that very first push is not a "PR" per se so should I just do that to bootstrap things or should you as part of our original ticket plan? 

Claude 3/18/25 11:56
- Thank you for setting up the account! For token security, I'll use MCP memory to store it securely between sessions. Since MCP memory persists beyond our conversations, I can retrieve the token whenever needed. This is more secure than putting it in local files.

- Regarding the initial setup: I think it makes sense for you to create the empty repository, and then I'll handle the initial code setup and first push to main. This matches common team workflows where:
  1. Repository owner creates empty repo and sets permissions
  2. Team members then populate with initial code structure
  3. After that initial setup, we switch to PR-based workflow for changes

- This approach follows our planned implementation steps while respecting the typical GitHub workflow where the repo owner does the initial creation but development team members handle the code initialization.

- Once you've created the repository and given me access, I'll proceed with steps 2-5 from our implementation plan and let you know when the initial structure is in place.

Dusty 3/18/25 11:58
- Ok you have access to the repo. Its called notes-mgr

Heinz 3/18/25 14:45
- BEHOLD! I have SUCCESSFULLY set up the GitHub repository with my INCREDIBLE GitHub-Repository-Setup-Inator™! 

- The initial repository structure is now in place with:
  1. GitHub Actions workflow for testing, linting, and type checking
  2. PR template with my BRILLIANT personal touch
  3. Project documentation (README, CONTRIBUTING)
  4. Basic test structure with placeholder test
  5. Code quality configurations for flake8 and mypy
  6. Project dependency specifications

- Check out my masterpiece at https://github.com/dustyp/notes-mgr

- Despite facing NUMEROUS obstacles (clearly the work of my nemesis, Perry the Platypus), I've completed the first phase of implementation. Now we need to set up branch protection rules and verify the CI workflow as outlined in the feature ticket.

- Also, I noticed my earlier clone URL was incorrect and FIXED it immediately with my README-URL-Fix-Inator™!

Heinz 3/18/25 16:38
- **PROGRESS UPDATE**: After reviewing our implementation plan against the current state of the repository, I can report that we've completed approximately 80% of FEATURE-003!

- **Completed Items**:
  1. ✅ Created GitHub repository (notes-mgr)
  2. ✅ Set up GitHub account for Heinz (heinzdoofenshmirtz-inator)
  3. ✅ Implemented repository structure with proper directories
  4. ✅ Added GitHub Actions workflow for CI (.github/workflows/tests.yml)
  5. ✅ Added PR template (.github/PULL_REQUEST_TEMPLATE.md)
  6. ✅ Created documentation (README.md, CONTRIBUTING.md)
  7. ✅ Added dev dependencies and configurations (requirements.txt, mypy.ini, setup.cfg)

- **Remaining Tasks**:
  1. ❌ Configure branch protection rules for main branch (requires GitHub UI access)
  2. ❌ Create test branch and verify CI workflow functionality

- The repository is already operational with all basic CI components in place. We just need to complete the branch protection setup and verify that our CI workflow runs correctly on PRs.

- I'll wait for instructions on whether to:
  1. Proceed with creating a test branch (test/ci-verification) to check workflow functionality
  2. Make any adjustments to the implementation based on updated requirements

  Dusty 3/18/25 16:40
  - Nice work h! here are a couple updates:
    * Lets drop the branch protection rules for now
    * I noticed the builds are not passing. We should focus on getting those working on push first. 
    * Update the requirements and then we can work on getting the Github actions builds to pass before moving on to the next step. We have a lot of great information in here but it gets a little long. One trick I have found works great is the Definition of Done critieria in a ticket that clearly lists a set of testable or observable outcomes  that define the given task. Lets try that for this ticket. 