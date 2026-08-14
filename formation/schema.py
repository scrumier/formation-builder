"""Validation schema for the training module.

The HTML rendering never trusts raw LLM output: the structure is validated
first with Pydantic. If the generated JSON does not respect the contract, the
app refuses to start with a clear (debuggable) error rather than displaying a
half-broken page.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class Meta(BaseModel):
    title: str
    source: str
    reference_produit: str | None = None
    public: str
    estimated_duration: str
    generated_at: str
    source_file: str | None = None


class Security(BaseModel):
    level: str
    label: str
    instructions: list[str] = Field(min_length=1)
    consequence: str


class Step(BaseModel):
    action: str
    key_point: str | None = None


class Phase(BaseModel):
    id: str
    title: str
    steps: list[Step] = Field(min_length=1)


class ReviewNote(BaseModel):
    """Point of doubt raised to the human designer (validation before publishing).

    Used when the source is ambiguous or inconsistent: the pipeline does not
    decide silently, it flags the issue and proposes a decision to validate.
    """

    subject: str
    finding: str
    decision: str


class Question(BaseModel):
    question: str
    options: list[str] = Field(min_length=2)
    correct: int
    explanation: str

    def model_post_init(self, __context) -> None:
        if not 0 <= self.correct < len(self.options):
            raise ValueError(
                f"'correct' index ({self.correct}) out of options range for: {self.question!r}"
            )


class Module(BaseModel):
    meta: Meta
    objectives: list[str] = Field(min_length=1)
    prerequisites: list[str] = Field(min_length=1)
    security: Security
    phases: list[Phase] = Field(min_length=1)
    quiz: list[Question] = Field(min_length=1)
    review_notes: list[ReviewNote] = Field(default_factory=list)
