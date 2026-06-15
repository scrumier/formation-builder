# Formation Builder — launcher autonome du projet.
#
#   make setup   <- une fois : cree le venv + installe les deps (uv)
#   make run     <- demarre le serveur, affiche l'URL (Ctrl+C pour arreter)
#   make help    <- rappel des commandes + URL
#
# Bind sur l'IP Tailscale -> joignable depuis le Mac, jamais expose publiquement.

TS   := 127.0.0.1
PORT := 5053

.PHONY: help setup run

help:
	@echo ""
	@echo "  Formation Builder"
	@echo "    make setup   installe les dependances (a faire une fois)"
	@echo "    make run     demarre la demo   ->  http://$(TS):$(PORT)"
	@echo ""

setup:
	@echo "==> Creation du venv + install des deps (uv)..."
	@uv sync --quiet
	@echo "==> Pret. Lancer :  make run"

run:
	@echo ""
	@echo "==> Ouvre sur ton Mac :  http://$(TS):$(PORT)      (Ctrl+C pour arreter)"
	@echo ""
	@FLASK_HOST=$(TS) FLASK_PORT=$(PORT) uv run python app.py
