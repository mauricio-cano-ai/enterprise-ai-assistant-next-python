from scorers import score_case


def test_score_case_requires_expected_citation_and_text() -> None:
    result = score_case(
        answer="Use a representative golden dataset and regression thresholds.",
        citation_ids=["eval-guide"],
        unsupported=False,
        expected_citation_ids=["eval-guide"],
        required_terms=["golden dataset"],
        expected_unsupported=False,
    )

    assert result.passed is True


def test_score_case_detects_regression() -> None:
    result = score_case(
        answer="I am not sure.",
        citation_ids=[],
        unsupported=True,
        expected_citation_ids=["eval-guide"],
        required_terms=["golden dataset"],
        expected_unsupported=False,
    )

    assert result.passed is False
    assert "citation" in " ".join(result.failures).lower()
