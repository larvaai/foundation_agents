from __future__ import annotations

import json
import urllib.error
import urllib.request

from core.errors import PromptRunnerError
from llm.config import DEFAULT_RUN_MODE, LOCAL_RUN_MODE, read_llm_config


def get_last_user_message(messages: list[dict[str, str]]) -> str:
    for message in reversed(messages):
        if message.get("role") == "user":
            return message.get("content", "")
    return ""


def make_message_preview(message: str, limit: int = 240) -> str:
    preview = " ".join(message.split())
    if len(preview) <= limit:
        return preview
    return preview[: limit - 3] + "..."


def call_fake_llm(messages: list[dict[str, str]]) -> str:
    user_message = get_last_user_message(messages)
    fake_final = {
        "action": "final",
        "finish_reason": "fake_echo",
        "message": "Layer 2 fake LLM returned a valid final JSON object.",
        "mode": DEFAULT_RUN_MODE,
        "prompt_chars": len(user_message),
        "prompt_preview": make_message_preview(user_message),
    }
    return json.dumps(fake_final, ensure_ascii=False)


def build_chat_completions_url(base_url: str) -> str:
    return f"{base_url.rstrip('/')}/chat/completions"


def call_local_llm(messages: list[dict[str, str]]) -> str:
    config = read_llm_config()
    url = build_chat_completions_url(str(config["base_url"]))
    payload = {
        "model": config["model"],
        "messages": messages,
        "max_tokens": config["max_tokens"],
        "temperature": config["temperature"],
    }
    request_body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=request_body,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {config['api_key']}",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=int(config["timeout"])) as response:
            response_text = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        error_body = exc.read().decode("utf-8", errors="replace")
        raise PromptRunnerError(
            f"LLM HTTP error {exc.code} from {url}: {error_body[:400]}"
        ) from exc
    except urllib.error.URLError as exc:
        raise PromptRunnerError(f"Cannot reach local LLM at {url}: {exc.reason}") from exc

    try:
        response_data = json.loads(response_text)
    except json.JSONDecodeError as exc:
        raise PromptRunnerError("LLM response was not valid JSON.") from exc

    choices = response_data.get("choices") if isinstance(response_data, dict) else None
    if not isinstance(choices, list) or not choices:
        raise PromptRunnerError("LLM response did not include any choices.")

    first_choice = choices[0]
    if not isinstance(first_choice, dict):
        raise PromptRunnerError("LLM first choice was not an object.")

    message = first_choice.get("message")
    if not isinstance(message, dict):
        raise PromptRunnerError("LLM first choice did not include a message object.")

    content = message.get("content")
    if not isinstance(content, str) or content.strip() == "":
        raise PromptRunnerError("LLM message content was empty.")

    return content


def call_llm(
    mode: str,
    messages: list[dict[str, str]],
) -> str:
    if mode == DEFAULT_RUN_MODE:
        return call_fake_llm(messages)
    if mode == LOCAL_RUN_MODE:
        return call_local_llm(messages)
    raise PromptRunnerError(f"Unsupported mode: {mode}")
