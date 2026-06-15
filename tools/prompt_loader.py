from __future__ import annotations

from pathlib import Path

from core.errors import PromptRunnerError
from core.runtime_paths import display_path


def read_text_file(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise PromptRunnerError(f"Prompt file not found: {display_path(path)}") from exc
    except IsADirectoryError as exc:
        raise PromptRunnerError(f"Prompt path is a directory: {display_path(path)}") from exc
    except UnicodeDecodeError as exc:
        raise PromptRunnerError(
            f"Prompt file is not valid UTF-8: {display_path(path)}"
        ) from exc
