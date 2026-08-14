"""Validation schema for the training module.

The HTML rendering never trusts raw LLM output: the structure is validated
first with Pydantic. If the generated JSON does not respect the contract, the
app refuses to start with a clear (debuggable) error rather than displaying a
half-broken page.
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
    """Point of doubt raised to the human designer (validation before publishing).

    Used when the source is ambiguous or inconsistent: the pipeline does not
    decide silently, it flags the issue and proposes a decision to validate.
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
                f"'correct' index ({self.correct}) out of options range for: {self.question!r}"
            )


class Module(BaseModel):
    meta: Meta
    objectifs: list[str] = Field(min_length=1)
    prerequis: list[str] = Field(min_length=1)
    securite: Securite
    phases: list[Phase] = Field(min_length=1)
    qcm: list[Question] = Field(min_length=1)
    notes_revision: list[NoteRevision] = Field(default_factory=list)
