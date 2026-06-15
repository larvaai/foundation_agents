from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_USER_PROMPT = PROJECT_ROOT / "prompts" / "user_prompt.md"
DEFAULT_SYSTEM_PROMPT = PROJECT_ROOT / "prompts" / "system_prompt.md"


def resolve_prompt_path(raw_path: str | None) -> Path:
    if raw_path is None:
        return DEFAULT_USER_PROMPT

    path = Path(raw_path)
    if path.is_absolute():
        return path
    return PROJECT_ROOT / path


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(PROJECT_ROOT))
    except ValueError:
        return str(path)
