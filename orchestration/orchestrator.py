from __future__ import annotations

from agents.tool_agent import build_chat_messages, parse_final_json
from core.runtime_paths import DEFAULT_SYSTEM_PROMPT
from llm.adapter import call_llm
from tools.prompt_loader import read_text_file


def run_orchestrator(prompt: str, mode: str) -> dict[str, object]:
    system_prompt = read_text_file(DEFAULT_SYSTEM_PROMPT)
    messages = build_chat_messages(system_prompt, prompt)
    raw_output = call_llm(mode, messages)
    return parse_final_json(raw_output)
