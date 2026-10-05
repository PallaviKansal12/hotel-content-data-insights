import pandas as pd
import re


# ---------------------------------------
# Configuration
# ---------------------------------------

HOTEL_DATA = "data/hotels.csv"
AI_CONTENT_DATA = "data/generated_content.csv"
OUTPUT_FILE = "data/content_evaluation_results.csv"


# ---------------------------------------
# Load data
# ---------------------------------------

def load_data():

    hotels = pd.read_csv(HOTEL_DATA)
    generated = pd.read_csv(AI_CONTENT_DATA)

    return hotels, generated


# ---------------------------------------
# Check whether a value appears in text
# ---------------------------------------

def value_in_text(value, text):

    if pd.isna(value):
        return False

    value = str(value).lower()
    text = str(text).lower()

    return value in text


# ---------------------------------------
# Evaluate one hotel
# ---------------------------------------

def evaluate_hotel(hotel, generated_content):

    description = generated_content["ai_description"]

    checks = {}

    # -----------------------------------
    # Hotel name
    # -----------------------------------

    checks["hotel_name"] = value_in_text(
        hotel["hotel_name"],
        description
    )


    # -----------------------------------
    # City
    # -----------------------------------

    checks["city"] = value_in_text(
        hotel["city"],
        description
    )


    # -----------------------------------
    # Rating
    # -----------------------------------

    rating = str(hotel["rating"])

    rating_present = rating in description

    checks["rating"] = rating_present


    # -----------------------------------
    # Review count
    # -----------------------------------

    review_count = str(
        int(hotel["review_count"])
    )

    checks["review_count"] = (
        review_count in description
    )


    # -----------------------------------
    # Detect unsupported claims
    # -----------------------------------

    unsupported_claims = []


    # Wrong luxury rating
    if "5-star" in description.lower():

        if hotel["rating"] != 5.0:

            unsupported_claims.append(
                "Claimed 5-star rating"
            )


    # Unsupported room count
    room_match = re.search(
        r"(\d+)\s+rooms",
        description.lower()
    )

    if room_match:

        unsupported_claims.append(
            f"Claimed {room_match.group(1)} rooms"
        )


    # Unsupported amenities
    amenities = [
        "rooftop swimming pool",
        "private spa",
        "michelin-starred restaurant",
        "airport transfers",
        "24-hour butler service"
    ]

    for amenity in amenities:

        if amenity in description.lower():

            unsupported_claims.append(
                f"Unsupported amenity: {amenity}"
            )


    # -----------------------------------
    # City mismatch detection
    # -----------------------------------

    cities = [
        "Berlin",
        "Munich",
        "Hamburg",
        "Frankfurt",
        "Cologne",
        "Dusseldorf",
        "Aachen",
        "Stuttgart"
    ]

    mentioned_cities = []

    for city in cities:

        if city.lower() in description.lower():

            mentioned_cities.append(city)


    if mentioned_cities:

        if hotel["city"] not in mentioned_cities:

            unsupported_claims.append(
                f"Wrong city: {mentioned_cities[0]}"
            )


    # -----------------------------------
    # Calculate risk
    # -----------------------------------

    failed_checks = sum(
        1 for value in checks.values()
        if not value
    )

    claim_count = len(
        unsupported_claims
    )


    total_issues = (
        failed_checks + claim_count
    )


    if total_issues == 0:

        risk = "LOW"

    elif total_issues <= 2:

        risk = "MEDIUM"

    else:

        risk = "HIGH"


    # -----------------------------------
    # Human review decision
    # -----------------------------------

    human_review_required = risk in [
        "MEDIUM",
        "HIGH"
    ]


    # -----------------------------------
    # Confidence score
    # -----------------------------------

    confidence = round(
        max(
            0,
            1 - (total_issues * 0.15)
        ),
        2
    )


    return {
        "hotel_id": hotel["hotel_id"],
        "hotel_name": hotel["hotel_name"],
        "risk_level": risk,

        "hotel_name_check": checks["hotel_name"],
        "city_check": checks["city"],
        "rating_check": checks["rating"],
        "review_count_check": checks["review_count"],

        "unsupported_claim_count": claim_count,

        "unsupported_claims": " | ".join(
            unsupported_claims
        ),

        "human_review_required":
            human_review_required,

        "confidence": confidence
    }


# ---------------------------------------
# Run evaluation
# ---------------------------------------

def run_evaluation():

    hotels, generated = load_data()

    results = []

    for _, hotel in hotels.iterrows():

        matching_content = generated[
            generated["hotel_id"]
            == hotel["hotel_id"]
        ]

        if matching_content.empty:

            continue

        generated_content = (
            matching_content.iloc[0]
        )

        result = evaluate_hotel(
            hotel,
            generated_content
        )

        results.append(result)


    results_df = pd.DataFrame(results)

    results_df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    return results_df


# ---------------------------------------
# Main
# ---------------------------------------

if __name__ == "__main__":

    results = run_evaluation()

    print("=" * 70)
    print("AI CONTENT EVALUATION AGENT")
    print("=" * 70)

    print(
        f"\nHotels evaluated: {len(results)}"
    )

    print("\nRisk distribution:")

    print(
        results["risk_level"]
        .value_counts()
    )

    print(
        "\nHuman review required:"
    )

    print(
        results[
            "human_review_required"
        ].value_counts()
    )

    print(
        "\nHigh-risk examples:"
    )

    print(
        results[
            results["risk_level"] == "HIGH"
        ][
            [
                "hotel_id",
                "hotel_name",
                "risk_level",
                "unsupported_claims"
            ]
        ]
        .head(10)
        .to_string(index=False)
    )

    print(
        "\nResults saved to:"
    )

    print(OUTPUT_FILE)