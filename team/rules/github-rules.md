# GitHub Workflow Rules for Notes Manager Project

## Branch Naming and Creation

1. **Branch Types and Naming Conventions**:
   - `feature/<ticket-number>-short-description` - For new features
   - `fix/<ticket-number>-short-description` - For bug fixes
   - `refactor/<ticket-number>-short-description` - For code refactoring
   - `test/<ticket-number>-short-description` - For testing purposes

2. **One Branch per Ticket**:
   - Create only ONE branch per feature ticket
   - If additional fixes are needed based on PR feedback, use the same branch
   - Avoid creating multiple branches for the same ticket

3. **Branch Creation Process**:
   - Always start from an up-to-date `main` branch
   - Use `git checkout -b <branch-name>` to create new branches
   - Push branch to remote promptly with `git push -u origin <branch-name>`

## Pull Request Process

1. **PR Creation**:
   - Create PR only when the feature is complete and tested locally
   - Use PR template to ensure all required information is included
   - Assign PR to the project owner (dustyp) for review
   - Link PR to the corresponding feature ticket

2. **PR Title Format**:
   - `[FEATURE-XXX] Brief description of changes`
   - Example: `[FEATURE-003] Fix linter issues and update flake8 configuration`

3. **PR Description**:
   - Clearly describe what the PR accomplishes
   - List all significant changes made
   - Include any context necessary for the reviewer
   - Complete the checklist in the template

4. **PR Review**:
   - Address all feedback from reviewers
   - If changes are requested, update the same branch and push
   - Do not open a new PR for review-requested changes

## Commit Guidelines

1. **Commit Messages**:
   - Write clear, descriptive commit messages
   - Begin with a short summary (50 chars or less)
   - If needed, follow with more detailed explanation after a blank line
   - Include the feature ticket number in commits
   - Example: `Fix linter issues in query_kg.py (FEATURE-003)`

2. **Commit Frequency**:
   - Make small, focused commits
   - Avoid large commits that encompass multiple unrelated changes
   - Commit often to preserve your work and make PRs easier to review

3. **Co-Authorship**:
   - If collaborating, include co-author credits where appropriate:
     ```
     Co-authored-by: Claude <claude@anthropic.com>
     ```

## CI/Build Verification

1. **Pre-PR Checklist**:
   - Ensure code passes all linters locally before pushing
   - Run tests locally before submitting PR
   - Fix any style issues before requesting review

2. **CI Verification**:
   - Always verify CI build has passed in GitHub UI before marking tickets complete
   - If CI fails, fix issues on the same branch and push updates
   - Do not merge PRs with failing CI builds

## Branch Cleanup

1. **After Merge**:
   - Delete branch after PR is merged (can be done through GitHub interface)
   - If working locally on a branch that's been merged, delete it:
     ```
     git branch -d <branch-name>
     ```

2. **Abandoned Branches**:
   - If a branch is no longer needed, don't push it to remote
   - If already pushed, consider deleting it to keep the repository clean

## Special Cases

1. **Emergency Fixes**:
   - For critical fixes needed on production, use `hotfix/<ticket-number>-description`
   - Hotfixes should be merged to both `main` and any affected release branches

2. **Experimental Work**:
   - For experimental features, use `experimental/<description>`
   - No need to submit PR until experiment is proven viable

---

These rules will help maintain a clean and efficient workflow in our GitHub repository. Update this document as our needs evolve or when improvements to the process are identified.