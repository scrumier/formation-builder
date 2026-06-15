"""Serveur de la démo Formation Builder.

Charge le module pré-généré, le valide contre le schéma, construit le
logigramme des phases, puis sert la page de formation.

    make run        # via Makefile (bind Tailscale + affiche l'URL)
    FLASK_HOST=... FLASK_PORT=... uv run python app.py
"""

from __future__ import annotations

import os
from pathlib import Path

from flask import Flask, abort, render_template, send_from_directory

from formation.extract import load_module

BASE = Path(__file__).parent
app = Flask(__name__)

MODULE = load_module(BASE / "module.json")


def logigramme(module) -> str:
    """Définition Mermaid du flux des phases (déterministe, jamais halluciné)."""
    noeuds = ["    secu([Sécurité préalable])"]
    liens = []
    precedent = "secu"
    for phase in module.phases:
        noeuds.append(f'    {phase.id}["{phase.titre}"]')
        liens.append(f"    {precedent} --> {phase.id}")
        precedent = phase.id
    return "flowchart TD\n" + "\n".join(noeuds) + "\n" + "\n".join(liens)


@app.route("/")
def index():
    return render_template(
        "module.html",
        m=MODULE,
        mermaid=logigramme(MODULE),
        nb_etapes=sum(len(p.etapes) for p in MODULE.phases),
    )


@app.route("/source")
def source():
    """Sert la notice PDF d'origine (consultation des sources)."""
    fichier = MODULE.meta.fichier_source
    if not fichier:
        abort(404)
    return send_from_directory(BASE / "data", fichier)


if __name__ == "__main__":
    host = os.environ.get("FLASK_HOST", "127.0.0.1")
    port = int(os.environ.get("FLASK_PORT", "5053"))
    app.run(host=host, port=port, debug=False)
