# Copilot instructions for `precimed/container_template`

## Repository purpose
- This repository is a reusable template for containerized projects (Docker/Singularity/Apptainer) and workflow scaffolding.
- Keep changes minimal and scoped to the issue; avoid broad template rewrites unless explicitly requested.

## Key project structure
- `containers/`: container recipes and built image references.
- `tests/`: pytest-based validation for runtime/container behavior.
- `scripts/init.py`: initialization script that customizes this template for downstream projects.
- `.github/workflows/`: CI checks (including Python linting and container workflows).

## Validation commands
- Install test/lint dependencies:
  - `python -m pip install -r test-requirements.txt flake8`
- Run tests:
  - `python -m pytest -q`
- Run lint:
  - `flake8 .`

## Contribution expectations for agent changes
- Prefer surgical edits over refactors.
- Do not modify unrelated files to fix pre-existing lint issues unless the task asks for it.
- If modifying behavior, update or add focused tests under `tests/`.
- Keep workflow and container changes backward-compatible with template usage.
