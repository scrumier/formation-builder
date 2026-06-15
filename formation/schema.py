"""Schéma de validation du module de formation.

Le rendu HTML ne fait jamais confiance à une sortie LLM brute : on valide
d'abord la structure avec Pydantic. Si le JSON généré ne respecte pas le
contrat, l'app refuse de démarrer avec une erreur claire (debuggable) plutôt
que d'afficher une page à moitié cassée.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class Meta(BaseModel):
    titre: str
    source: str
    reference_produit: str | None = None
    public: str
    duree_estimee: str
    genere_le: str
    fichier_source: str | None = None


class Securite(BaseModel):
    niveau: str
    intitule: str
    consignes: list[str] = Field(min_length=1)
    consequence: str


class Etape(BaseModel):
    action: str
    point_cle: str | None = None


class Phase(BaseModel):
    id: str
    titre: str
    etapes: list[Etape] = Field(min_length=1)


class NoteRevision(BaseModel):
    """Point de doute remonté au concepteur humain (validation avant publication).

    Sert quand la source est ambiguë ou incohérente : le pipeline ne tranche pas
    en silence, il signale et propose une décision à valider.
    """

    sujet: str
    constat: str
    decision: str


class Question(BaseModel):
    question: str
    options: list[str] = Field(min_length=2)
    correct: int
    explication: str

    def model_post_init(self, __context) -> None:
        if not 0 <= self.correct < len(self.options):
            raise ValueError(
                f"index 'correct' ({self.correct}) hors des options pour : {self.question!r}"
            )


class Module(BaseModel):
    meta: Meta
    objectifs: list[str] = Field(min_length=1)
    prerequis: list[str] = Field(min_length=1)
    securite: Securite
    phases: list[Phase] = Field(min_length=1)
    qcm: list[Question] = Field(min_length=1)
    notes_revision: list[NoteRevision] = Field(default_factory=list)
