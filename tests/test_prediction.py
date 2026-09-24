import pandas as pd

from src.prediction import (
    prepare_input,
    predict_complaint,
)


def test_prepare_input_shape():
    features = prepare_input(
        product="Credit card",
        sub_product="Other",
        issue="Other",
        sub_issue="Other",
        submitted_via="Web",
        state="CA",
        company="BANK OF AMERICA, NATIONAL ASSOCIATION",
        received_date="2025-01-15",
        narrative="I was charged an incorrect fee.",
    )

    assert isinstance(features, pd.DataFrame)
    assert features.shape[0] == 1
    assert features.shape[1] == 262


def test_prepare_input_has_no_missing_values():
    features = prepare_input(
        product="Credit card",
        sub_product="Other",
        issue="Other",
        sub_issue="Other",
        submitted_via="Web",
        state="CA",
        company="BANK OF AMERICA, NATIONAL ASSOCIATION",
        received_date="2025-01-15",
        narrative="I was charged an incorrect fee.",
    )

    assert features.isna().sum().sum() == 0


def test_prediction_returns_valid_result():
    prediction, probabilities = predict_complaint(
        product="Credit card",
        sub_product="Other",
        issue="Other",
        sub_issue="Other",
        submitted_via="Web",
        state="CA",
        company="BANK OF AMERICA, NATIONAL ASSOCIATION",
        received_date="2025-01-15",
        narrative="I was charged an incorrect fee.",
    )

    assert prediction in probabilities
    assert len(probabilities) > 0
    assert abs(sum(probabilities.values()) - 1.0) < 1e-6