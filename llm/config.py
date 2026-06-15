from __future__ import annotations

import os

from core.errors import PromptRunnerError


DEFAULT_RUN_MODE = "fake"
LOCAL_RUN_MODE = "local"
SUPPORTED_RUN_MODES = {DEFAULT_RUN_MODE, LOCAL_RUN_MODE}

DEFAULT_LLM_BASE_URL = "http://127.0.0.1:1234/v1"
DEFAULT_LLM_MODEL = "local-model"
DEFAULT_LLM_API_KEY = "lm-studio"
DEFAULT_LLM_TIMEOUT_SECONDS = 60
DEFAULT_LLM_MAX_TOKENS = 512
DEFAULT_LLM_TEMPERATURE = 0.1


def read_env_text(name: str, default: str) -> str:
    value = os.environ.get(name)
    if value is None or value == "":
        return default
    return value


def read_env_int(name: str, default: int) -> int:
    raw_value = os.environ.get(name)
    if raw_value is None or raw_value == "":
        return default

    try:
        return int(raw_value)
    except ValueError as exc:
        raise PromptRunnerError(f"Environment variable {name} must be an integer.") from exc


def read_env_float(name: str, default: float) -> float:
    raw_value = os.environ.get(name)
    if raw_value is None or raw_value == "":
        return default

    try:
        return float(raw_value)
    except ValueError as exc:
        raise PromptRunnerError(f"Environment variable {name} must be a number.") from exc


def read_llm_config() -> dict[str, str | int | float]:
    return {
        "base_url": read_env_text("LLM_BASE_URL", DEFAULT_LLM_BASE_URL),
        "model": read_env_text("LLM_MODEL", DEFAULT_LLM_MODEL),
        "api_key": read_env_text("LLM_API_KEY", DEFAULT_LLM_API_KEY),
        "timeout": read_env_int("LLM_TIMEOUT", DEFAULT_LLM_TIMEOUT_SECONDS),
        "max_tokens": read_env_int("LLM_MAX_TOKENS", DEFAULT_LLM_MAX_TOKENS),
        "temperature": read_env_float("LLM_TEMPERATURE", DEFAULT_LLM_TEMPERATURE),
    }
