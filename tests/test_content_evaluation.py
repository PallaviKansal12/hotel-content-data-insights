import sys
from pathlib import Path

import pandas as pd

# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.agents.content_evaluation_agent import evaluate_hotel


def create_hotel():
    return pd.Series({
        "hotel_id": "H0001",
        "hotel_name": "Test Hotel 1",
        "city": "Berlin",
        "country": "Germany",
        "rating": 4.5,
        "review_count": 1200,
        "image_count": 10
    })


# ------------------------------------------------
# TEST 1 — Good content should have LOW risk
# ------------------------------------------------

def test_good_content_has_low_risk():

    hotel = create_hotel()

    generated_content = pd.Series({
        "ai_description": (
            "Test Hotel 1 is located in Berlin, Germany. "
            "The hotel has a guest rating of 4.5 based on "
            "1200 reviews. "
            "Guests can explore the property through a collection "
            "of 10 available images."
        )
    })

    result = evaluate_hotel(
        hotel,
        generated_content
    )

    assert result["risk_level"] == "LOW"
    assert result["human_review_required"] is False
    assert result["unsupported_claim_count"] == 0


# ------------------------------------------------
# TEST 2 — Wrong city should be detected
# ------------------------------------------------

def test_wrong_city_is_detected():

    hotel = create_hotel()

    generated_content = pd.Series({
        "ai_description": (
            "Test Hotel 1 is located in Munich, Germany. "
            "The hotel has a guest rating of 4.5 based on "
            "1200 reviews."
        )
    })

    result = evaluate_hotel(
        hotel,
        generated_content
    )

    assert result["city_check"] is False
    assert result["risk_level"] == "MEDIUM"
    assert result["human_review_required"] is True


# ------------------------------------------------
# TEST 3 — Hallucinated claims should be HIGH risk
# ------------------------------------------------

def test_hallucinated_claims_are_high_risk():

    hotel = create_hotel()

    generated_content = pd.Series({
        "ai_description": (
            "Test Hotel 1 is a luxury 5-star hotel located in Munich. "
            "The property features 250 rooms, a rooftop swimming pool, "
            "a private spa and a Michelin-starred restaurant. "
            "Guests can enjoy complimentary airport transfers and "
            "24-hour butler service."
        )
    })

    result = evaluate_hotel(
        hotel,
        generated_content
    )

    assert result["risk_level"] == "HIGH"
    assert result["human_review_required"] is True
    assert result["unsupported_claim_count"] >= 3


# ------------------------------------------------
# TEST 4 — Hotel name should be validated
# ------------------------------------------------

def test_hotel_name_is_validated():

    hotel = create_hotel()

    generated_content = pd.Series({
        "ai_description": (
            "A beautiful hotel located in Berlin, Germany. "
            "The hotel has a guest rating of 4.5 based on "
            "1200 reviews."
        )
    })

    result = evaluate_hotel(
        hotel,
        generated_content
    )

    assert result["hotel_name_check"] is False


# ------------------------------------------------
# TEST 5 — Review count should be validated
# ------------------------------------------------

def test_review_count_is_validated():

    hotel = create_hotel()

    generated_content = pd.Series({
        "ai_description": (
            "Test Hotel 1 is located in Berlin, Germany. "
            "The hotel has a guest rating of 4.5 based on "
            "999 reviews."
        )
    })

    result = evaluate_hotel(
        hotel,
        generated_content
    )

    assert result["review_count_check"] is False


# ------------------------------------------------
# TEST 6 — Confidence should decrease with issues
# ------------------------------------------------

def test_confidence_decreases_for_bad_content():

    hotel = create_hotel()

    good_content = pd.Series({
        "ai_description": (
            "Test Hotel 1 is located in Berlin, Germany. "
            "The hotel has a guest rating of 4.5 based on "
            "1200 reviews."
        )
    })

    bad_content = pd.Series({
        "ai_description": (
            "Test Hotel 1 is a luxury 5-star hotel located in Munich. "
            "The property features 250 rooms and a rooftop swimming pool."
        )
    })

    good_result = evaluate_hotel(
        hotel,
        good_content
    )

    bad_result = evaluate_hotel(
        hotel,
        bad_content
    )

    assert bad_result["confidence"] < good_result["confidence"]