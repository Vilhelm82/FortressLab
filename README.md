# FortressLab

FortressLab is a headless research environment for spatially grounded,
evidence-backed evaluation of defensive fortifications.

The current milestone establishes the versioned scenario and reproducibility
contracts. Geometry and evaluator behaviour are added in subsequent milestones.

## Development

```bash
uv sync --all-groups
uv run pytest
uv run ruff check .
uv run mypy
```
