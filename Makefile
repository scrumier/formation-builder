# formation-builder
#
#   make setup   once: creates the venv and installs dependencies (uv)
#   make run     starts the server and prints the URL (Ctrl+C to stop)
#   make help    the commands and the URL
#
# Listens locally by default. Override HOST to expose it on the network.

-include local.mk
TS ?= 127.0.0.1
PORT := 5053

.PHONY: help setup run

help:
	@echo ""
	@echo "  formation-builder"
	@echo "    make setup   install dependencies (once)"
	@echo "    make run     start the demo  ->  http://$(TS):$(PORT)"
	@echo ""

setup:
	@echo "==> Creating the venv and installing dependencies (uv)..."
	@uv sync --quiet
	@echo "==> Ready. Run:  make run"

run:
	@echo ""
	@echo "==> Open:  http://$(TS):$(PORT)      (Ctrl+C to stop)"
	@echo ""
	@FLASK_HOST=$(TS) FLASK_PORT=$(PORT) uv run python app.py
