from __future__ import annotations

import json

from core.errors import PromptRunnerError


def build_chat_messages(system_prompt: str, user_prompt: str) -> list[dict[str, str]]:
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]


def parse_final_json(raw_text: str) -> dict[str, object]:
    # Layer 2 intentionally has no JsonGate repair yet.
    try:
        data = json.loads(raw_text)
    except json.JSONDecodeError as exc:
        raise PromptRunnerError("Agent output was not valid JSON. Layer 2 has no JsonGate yet.") from exc

    if not isinstance(data, dict):
        raise PromptRunnerError("Agent output must be a JSON object.")
    if data.get("action") != "final":
        raise PromptRunnerError("Layer 2 only supports JSON with action='final'.")

    message = data.get("message")
    if not isinstance(message, str) or message.strip() == "":
        raise PromptRunnerError("Final JSON must include a non-empty string 'message'.")

    return data
