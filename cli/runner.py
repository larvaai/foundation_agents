from __future__ import annotations

import json
import sys

from core.errors import PromptRunnerError
from core.runtime_paths import DEFAULT_USER_PROMPT, display_path, resolve_prompt_path
from llm.config import DEFAULT_RUN_MODE, SUPPORTED_RUN_MODES
from orchestration.orchestrator import run_orchestrator
from tools.prompt_loader import read_text_file


def configure_stdout() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")


def print_usage() -> None:
    print("Usage: python main.py [--mode fake|local] [prompt_path]")
    print(f"Default prompt: {display_path(DEFAULT_USER_PROMPT)}")
    print(f"Default mode: {DEFAULT_RUN_MODE}")
    print("Local env: LLM_BASE_URL, LLM_MODEL, LLM_API_KEY, LLM_TIMEOUT")


def parse_cli_args(argv: list[str]) -> tuple[bool, str, str | None]:
    show_help = False
    mode = DEFAULT_RUN_MODE
    raw_prompt_path = None
    index = 0

    while index < len(argv):
        arg = argv[index]

        if arg in {"-h", "--help"}:
            show_help = True
            return show_help, mode, raw_prompt_path

        if arg == "--mode":
            if index + 1 >= len(argv):
                raise PromptRunnerError("Missing value after --mode.")
            mode = argv[index + 1]
            index += 2
            continue

        if arg.startswith("--mode="):
            mode = arg.split("=", 1)[1]
            index += 1
            continue

        if arg.startswith("--"):
            raise PromptRunnerError(f"Unknown option: {arg}")

        if raw_prompt_path is not None:
            raise PromptRunnerError("Expected zero or one prompt path argument.")

        raw_prompt_path = arg
        index += 1

    if mode not in SUPPORTED_RUN_MODES:
        raise PromptRunnerError(f"Unsupported mode '{mode}'. Use fake or local.")

    return show_help, mode, raw_prompt_path


def run_cli(argv: list[str]) -> int:
    show_help, mode, raw_prompt_path = parse_cli_args(argv)
    if show_help:
        print_usage()
        return 0

    prompt_path = resolve_prompt_path(raw_prompt_path)
    prompt = read_text_file(prompt_path)
    final_action = run_orchestrator(prompt, mode)
    print(json.dumps(final_action, ensure_ascii=False, indent=2))
    return 0


def main() -> int:
    configure_stdout()
    try:
        return run_cli(sys.argv[1:])
    except PromptRunnerError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
