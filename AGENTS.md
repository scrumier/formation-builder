# formation-builder

Turns a technical procedure PDF into a structured training module: guided steps,
safety points, flowchart, validation quiz.

## When asked to set this up

Follow this sequence, in order, without improvising.

1. Check `uv`: `uv --version`. If it is missing, install it with
   `curl -LsSf https://astral.sh/uv/install.sh | sh`, then say so.
2. `make setup`
3. Give the user the command that matters: `make run`, then
   http://127.0.0.1:5053.

Do nothing else unless asked: no refactoring, no added dependency, no commit and
no push.

## What actually breaks

- This repo needs no API key, unlike the other tools on this account. Do not go
  looking for one, there is no `.env.example` here.
- Port 5053 may be taken. `PORT=5063 make run` changes it.
- A scanned PDF yields no text, it needs OCR first.
- The interface and the extraction prompt are in French on purpose, the source
  manual being French. Do not translate them as part of a setup request.

## Shape of the repo

`formation/` holds the code, `app.py` the server, `module.json` the produced
structure, `templates/` the rendering, `data/` the source manual.
