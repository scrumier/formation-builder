# Formation Builder

Transforme un **PDF de procédure technique** en **module de formation structuré**
(objectifs, étapes guidées, points de sécurité, logigramme, QCM de validation),
rendu dans une page web claire.

Cas d'usage : automatiser la production de contenu de formation à partir de la
documentation technique existante, en gardant un humain dans la boucle pour
valider les zones ambiguës.

## Ce que ça fait aujourd'hui

- **Extraction structurée** d'un PDF de procédure vers un module pédagogique
  (objectifs, prérequis, consignes de sécurité, phases et étapes, QCM).
- **Validation par schéma** (Pydantic) : le rendu ne fait jamais confiance à une
  sortie LLM brute ; une sortie non conforme casse proprement.
- **Logigramme des phases** généré de façon déterministe (Mermaid), jamais halluciné.
- **QCM interactif** de validation des acquis (score + explications).
- **Notes de révision** : si la source est ambiguë ou incohérente (ex. ici une
  divergence FR/EN de la notice sur la plaque de remplissage), le pipeline ne
  tranche pas en silence, il **remonte le doute au concepteur** pour validation.
- **Traçabilité** : bouton vers la **notice d'origine** (le PDF source est servi tel quel).

## Pipeline

```
PDF procédure  ->  texte (pdfplumber)  ->  LLM (prompt + schéma)  ->  JSON validé  ->  page HTML
```

L'étape LLM est isolée dans `formation/extract.py` (prompt d'ingénieur
pédagogique). Pour la démo, elle a été exécutée une fois et le résultat figé dans
`module.json` (zéro token consommé) ; brancher un backend dans `call_llm` suffit
pour l'automatiser.

## Prochaines améliorations

- **OCR documentaire (Mistral Document AI)** : aujourd'hui seul le **texte** est
  extrait (`pdfplumber`), les **schémas sont perdus**. Un OCR type Mistral
  permettrait de récupérer les figures, les réinsérer à côté de la bonne étape, et
  coupler à un modèle vision pour les comprendre/légender. Sur une notice
  technique, le visuel porte une grande partie de l'information.
- **Documents longs** : remplacer l'appel LLM unique par un map-reduce
  (segmentation par section -> un appel par section -> synthèse + QCM global).
- **Export** : génération PDF/SCORM du module pour intégration LMS.

## Données & conformité

Démo alimentée **uniquement** par un document **public** : notice Schneider
Electric **PHA79813** (installation disjoncteur PowerPact B), dans `data/`.
Aucune donnée personnelle, aucune donnée client. RGPD-safe par construction.

## Lancer

```
make setup    # une fois : venv + dépendances (uv)
make run      # démarre, affiche l'URL
```

## Stack

Python · Flask · Pydantic · pdfplumber. Code scriptable, testable et versionnable.
