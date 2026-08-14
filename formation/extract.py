"""Extraction pipeline: procedure PDF -> structured training module.

Architecture (deliberately simple and scalable):

    PDF  ->  text (pdfplumber)  ->  LLM (prompt + schema)  ->  validated Module

For this demo, the LLM step was run by Claude (the assistant that built the
project), and the result is frozen in `module.json`. The `call_llm` function
below is the only point to wire up to go live: any backend (Anthropic,
OpenRouter, local model) returning JSON conforming to `formation.schema.Module`
will do.

For very long documents (a catalog of hundreds of pages), the single call is
replaced by a map-reduce: split by section -> one call per section in
parallel -> a synthesis call + global quiz generation.
"""

from __future__ import annotations

import json
from pathlib import Path

from .schema import Module

PROMPT_SYSTEME = """\
You are an instructional designer for technical training in an industrial
electrical environment. From a raw technical procedure, you produce a
structured training module, faithful to the source, without inventing
anything.

Rules:
- Rephrase in clear, learner-oriented English, without losing the numeric
  values (torque specs, ratings, product references).
- Isolate the safety instructions in a dedicated block.
- Break the procedure down into ordered phases, each step = one action + an
  optional key point (safety, critical value, common pitfall).
- Generate a validation quiz: each question tests a point actually present
  in the procedure (sequence, torque, conditional rule...).
- Respond ONLY with JSON conforming to the schema provided.
"""


def pdf_to_text(pdf_path: str | Path) -> str:
    """Extracts the raw text from a procedure PDF."""
    import pdfplumber

    pages: list[str] = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            pages.append(page.extract_text() or "")
    return "\n\n".join(pages)


def call_llm(system: str, user: str) -> str:  # pragma: no cover - integration point
    """LLM integration point.

    Not wired up in the demo (zero tokens consumed): the module is already in
    `module.json`. Wire up the backend of your choice here to automate it.
    """
    raise NotImplementedError(
        "LLM backend not wired up for the demo. The pre-generated module is in "
        "module.json. Wire up Anthropic/OpenRouter here to go live."
    )


def build_module(pdf_path: str | Path) -> Module:
    """Full pipeline PDF -> validated Module (live mode)."""
    texte = pdf_to_text(pdf_path)
    brut = call_llm(PROMPT_SYSTEME, texte)
    return Module.model_validate_json(brut)


def load_module(json_path: str | Path) -> Module:
    """Loads and validates an already-generated module (demo mode)."""
    data = json.loads(Path(json_path).read_text(encoding="utf-8"))
    return Module.model_validate(data)
