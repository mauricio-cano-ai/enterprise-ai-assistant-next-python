from dataclasses import dataclass


@dataclass(frozen=True)
class ScoreResult:
    passed: bool
    failures: tuple[str, ...]


def score_case(
    *,
    answer: str,
    citation_ids: list[str],
    unsupported: bool,
    expected_citation_ids: list[str],
    required_terms: list[str],
    expected_unsupported: bool,
) -> ScoreResult:
    failures: list[str] = []
    expected = set(expected_citation_ids)
    actual = set(citation_ids)

    missing_citations = sorted(expected - actual)
    if missing_citations:
        failures.append(f"Missing citation ids: {', '.join(missing_citations)}")

    unexpected_citations = sorted(actual - expected)
    if unexpected_citations:
        failures.append(f"Unexpected citation ids: {', '.join(unexpected_citations)}")
    for term in required_terms:
        if term.lower() not in answer.lower():
            failures.append(f"Missing required answer term: {term}")
    if unsupported is not expected_unsupported:
        failures.append(
            f"Unsupported flag was {unsupported}, expected {expected_unsupported}"
        )
    return ScoreResult(passed=not failures, failures=tuple(failures))
