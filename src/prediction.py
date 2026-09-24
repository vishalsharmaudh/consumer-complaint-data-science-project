from pathlib import Path

import joblib
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = BASE_DIR / "models"

MODEL_PATH = MODEL_DIR / "hist_gradient_boosting_model.joblib"
ENCODER_PATH = MODEL_DIR / "one_hot_encoder.joblib"
COMPANY_MAPPING_PATH = MODEL_DIR / "company_frequency_mapping.csv"


model = joblib.load(MODEL_PATH)
encoder = joblib.load(ENCODER_PATH)

company_frequency_mapping = pd.read_csv(COMPANY_MAPPING_PATH)


print("Prediction artifacts loaded successfully.")

def prepare_input(
    product,
    sub_product,
    issue,
    sub_issue,
    submitted_via,
    state,
    company,
    received_date,
    narrative="",
):
    data = pd.DataFrame([{
        "product": product,
        "sub_product": sub_product,
        "issue": issue,
        "sub_issue": sub_issue,
        "submitted_via": submitted_via,
        "state": state,
        "company": company,
        "received_date": pd.to_datetime(received_date),
    }])

    # Date features
    data["received_year"] = data["received_date"].dt.year
    data["received_month"] = data["received_date"].dt.month
    data["received_dayofweek"] = data["received_date"].dt.dayofweek
    data["received_day"] = data["received_date"].dt.day
    data["received_quarter"] = data["received_date"].dt.quarter
    data["received_hour"] = data["received_date"].dt.hour

   # Narrative features
    narrative = "" if narrative is None else str(narrative).strip()

    data["narrative_present"] = int(bool(narrative))
    data["narrative_length"] = len(narrative)
    data["narrative_word_count"] = len(narrative.split())

    # Match training-time company relabeling
    data["company"] = data["company"].replace(
        "Pending Company Match",
        "Unknown Company"
    )

    # Rare-category bucketing
    columns_to_bucket = [
        "sub_product",
        "issue",
        "sub_issue",
        "state",
    ]

    for column, categories in zip(
        columns_to_bucket,
        encoder.categories_[1:5]
    ):
        allowed_categories = set(categories) - {"Other"}

        data[column] = data[column].where(
            data[column].isin(allowed_categories),
            "Other"
        )

    # Company frequency encoding
    data["company_frequency"] = (
        data["company"]
        .map(
            company_frequency_mapping.set_index("company")[
                "company_frequency"
            ]
        )
        .fillna(0)
    )

    data = data.drop(columns=["company", "received_date"])

    categorical_features = [
        "product",
        "sub_product",
        "issue",
        "sub_issue",
        "submitted_via",
        "state",
    ]

    numeric_features = [
        "received_year",
        "received_month",
        "received_dayofweek",
        "received_day",
        "received_quarter",
        "received_hour",
        "narrative_present",
        "narrative_length",
        "narrative_word_count",
        "company_frequency",
    ]

    encoded = encoder.transform(data[categorical_features])

    encoded_df = pd.DataFrame(
        encoded,
        columns=encoder.get_feature_names_out()
    )

    final_data = pd.concat(
        [
            data[numeric_features].reset_index(drop=True),
            encoded_df.reset_index(drop=True),
        ],
        axis=1,
    )

    # Match the exact feature schema used during model training
    final_data = final_data.reindex(
        columns=model.feature_names_in_,
        fill_value=0
    )

    return final_data

def get_input_categories():
    return {
        "product": list(encoder.categories_[0]),
        "sub_product": list(encoder.categories_[1]),
        "issue": list(encoder.categories_[2]),
        "sub_issue": list(encoder.categories_[3]),
        "submitted_via": list(encoder.categories_[4]),
        "state": list(encoder.categories_[5]),
    }

def predict_complaint(
    product,
    sub_product,
    issue,
    sub_issue,
    submitted_via,
    state,
    company,
    received_date,
    narrative="",
):
    features = prepare_input(
        product=product,
        sub_product=sub_product,
        issue=issue,
        sub_issue=sub_issue,
        submitted_via=submitted_via,
        state=state,
        company=company,
        received_date=received_date,
        narrative=narrative,
    )

    prediction = model.predict(features)[0]

    probabilities = model.predict_proba(features)[0]

    probability_map = {
        class_name: float(probability)
        for class_name, probability in zip(
            model.classes_,
            probabilities
        )
    }

    return prediction, probability_map