"""Pipeline d'extraction : PDF de procédure -> module de formation structuré.

Architecture (volontairement simple et scalable) :

    PDF  ->  texte (pdfplumber)  ->  LLM (prompt + schéma)  ->  Module validé

Pour cette démo, l'étape LLM a été exécutée par Claude (l'assistant qui a
construit le projet), et le résultat est figé dans `module.json`. La fonction
`call_llm` ci-dessous est le seul point à brancher pour passer en automatique :
n'importe quel backend (Anthropic, OpenRouter, modèle local) renvoyant du JSON
conforme à `formation.schema.Module` fait l'affaire.

Pour des documents très longs (catalogue de centaines de pages), on remplace
l'appel unique par un map-reduce : segmentation par section -> un appel par
section en parallèle -> un appel de synthèse + génération du QCM global.
"""

from __future__ import annotations

import json
from pathlib import Path

from .schema import Module

PROMPT_SYSTEME = """\
Tu es ingénieur pédagogique pour la formation technique en environnement
industriel électrique. À partir d'une procédure technique brute, tu produis un
module de formation structuré, fidèle à la source, sans rien inventer.

Règles :
- Reformuler en français clair, orienté apprenant, sans perdre les valeurs
  chiffrées (couples de serrage, calibres, références produit).
- Isoler les consignes de sécurité en bloc dédié.
- Découper la procédure en phases ordonnées, chaque étape = une action + un
  point clé optionnel (sécurité, valeur critique, piège fréquent).
- Générer un QCM de validation : chaque question teste un point réellement
  présent dans la procédure (séquence, couple, règle conditionnelle...).
- Répondre UNIQUEMENT par un JSON conforme au schéma fourni.
"""


def pdf_to_text(pdf_path: str | Path) -> str:
    """Extrait le texte brut d'un PDF de procédure."""
    import pdfplumber

    pages: list[str] = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            pages.append(page.extract_text() or "")
    return "\n\n".join(pages)


def call_llm(system: str, user: str) -> str:  # pragma: no cover - point d'intégration
    """Point d'intégration LLM.

    Non câblé dans la démo (zéro token consommé) : le module est déjà dans
    `module.json`. Brancher ici le backend de son choix pour l'automatiser.
    """
    raise NotImplementedError(
        "Backend LLM non câblé pour la démo. Le module pré-généré est dans "
        "module.json. Brancher Anthropic/OpenRouter ici pour passer en live."
    )


def build_module(pdf_path: str | Path) -> Module:
    """Pipeline complet PDF -> Module validé (mode live)."""
    texte = pdf_to_text(pdf_path)
    brut = call_llm(PROMPT_SYSTEME, texte)
    return Module.model_validate_json(brut)


def load_module(json_path: str | Path) -> Module:
    """Charge et valide un module déjà généré (mode démo)."""
    data = json.loads(Path(json_path).read_text(encoding="utf-8"))
    return Module.model_validate(data)
