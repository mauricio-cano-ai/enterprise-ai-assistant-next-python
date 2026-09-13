from typing import Protocol


class AnswerQualityScorer(Protocol):
    async def score(
        self,
        *,
        question: str,
        answer: str,
        reference: str | None = None,
    ) -> dict[str, float]: ...
