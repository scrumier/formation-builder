# formation-builder

Turns a **technical procedure PDF** into a **structured training module**
(objectives, guided steps, safety points, flowchart, validation quiz), rendered
as a plain web page.

Use case: producing training content from the technical documentation a company
already has, with a human kept in the loop to settle the ambiguous parts.

## Run it

The short way, with any coding agent:

```bash
claude          # or codex, or whatever you run
> set this up for me
```

It reads `AGENTS.md`, installs what is missing, and hands back the command that
starts it.

The manual way:

```bash
make setup    # once: venv and dependencies (uv)
make run      # starts, prints the URL
```

## What it does today

- **Structured extraction** from a procedure PDF into a teaching module
  (objectives, prerequisites, safety instructions, phases and steps, quiz).
- **Schema validation** (Pydantic): the renderer never trusts raw LLM output, a
  non-conforming answer fails cleanly instead of reaching the page.
- **Phase flowchart** generated deterministically (Mermaid), never hallucinated.
- **Interactive quiz** with a score and explanations.
- **Review notes**: when the source is ambiguous or inconsistent (here, a French
  and English divergence in the manual about the filling plate), the pipeline
  does not decide silently. It **raises the doubt to the author** for a call.
- **Traceability**: a button back to the original manual, served as it is.

## Pipeline

```
procedure PDF  ->  text (pdfplumber)  ->  LLM (prompt + schema)  ->  validated JSON  ->  HTML page
```

The LLM step is isolated in `formation/extract.py`. For the demo it was run once
and the result frozen into `module.json`, so the demo costs zero tokens. Wiring a
backend into `call_llm` is enough to automate it.

## What is missing

- **Document OCR.** Only the **text** is extracted today (`pdfplumber`), so the
  **diagrams are lost**. An OCR pass would recover the figures, place them next
  to the right step, and pair with a vision model to caption them. On a technical
  manual, a large part of the information is in the drawings.
- **Long documents.** The single LLM call should become a map-reduce: split by
  section, one call per section, then a global synthesis and quiz.
- **Export.** PDF or SCORM output, for integration into an LMS.

## Data and compliance

The demo runs on a **public document only**: Schneider Electric manual
**PHA79813** (PowerPact B circuit breaker installation), in `data/`. No personal
data, no client data.

## A note on language

The documentation, the interface and the extraction prompt are written in French,
because the source manual and the target audience are French. The pipeline itself
has nothing language-specific in it.

## Stack

Python, Flask, Pydantic, pdfplumber. Scriptable, testable, versionable.
