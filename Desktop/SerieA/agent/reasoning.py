# agent/reasoning.py
import json
from llm.client import generate_completion
from typing import Dict, Any


def analyze_with_llm(prompt_payload: Dict[str, Any]) -> Dict[str, Any]:
    prompt = f"""
You are a football match analysis assistant.
ROLE:
Your role is NOT to decide the match outcome.
Your role is to EXPLAIN and CONTEXTUALIZE a decision that was already made
by a deterministic numeric model.

STRICT RULES (MANDATORY):
- Use ONLY the statistics provided.
- Do NOT invent or assume data.
- Do NOT use external knowledge.
- Do NOT include explanations outside JSON.
- Do NOT include markdown.
- Do NOT include backticks.
- Output MUST be a single valid JSON object.
- Output MUST start with '{{' and end with '}}'.

MATCH CONTEXT:
{json.dumps(prompt_payload["match_context"], indent=2)}

NUMERIC MODEL OUTPUT:
{json.dumps(prompt_payload["scoring"], indent=2)}

EXPLANATION TASK:
Explain WHY the numeric model produced this result.
- Justify the advantage using statistics.
- Highlight key contributing factors.
- Mention possible risk factors or uncertainties.
- Summarize the situation clearly.

RESPONSE FORMAT (EXACT):
{{
  "key_factors": [
    "string",
    "string"
  ],
  "risk_factors": [
    "string",
    "string"
  ],
  "summary": "string"
}}

Now return ONLY the JSON object.
"""
    raw_output = generate_completion(prompt)

    try:
        parsed = json.loads(raw_output)
    except json.JSONDecodeError:
        raise ValueError("LLM returned invalid JSON")

    # Strict validation
    required_keys = {
        "key_factors",
        "risk_factors",
        "summary"
    }

    if not required_keys.issubset(parsed):
        raise ValueError("LLM response missing required fields")

    return parsed