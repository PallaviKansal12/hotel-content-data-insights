import pandas as pd
import random


# ---------------------------------------
# Configuration
# ---------------------------------------

INPUT_FILE = "data/hotels.csv"
OUTPUT_FILE = "data/generated_content.csv"

random.seed(42)


# ---------------------------------------
# Load hotel data
# ---------------------------------------

def load_hotels():

    return pd.read_csv(INPUT_FILE)


# ---------------------------------------
# Generate AI-style content
# ---------------------------------------

def generate_description(row, content_type):

    hotel_name = row["hotel_name"]
    city = row["city"]
    country = row["country"]
    rating = row["rating"]
    review_count = row["review_count"]
    image_count = row["image_count"]

    # -----------------------------------
    # GOOD: Factually consistent
    # -----------------------------------

    if content_type == "good":

        return (
            f"{hotel_name} is located in {city}, {country}. "
            f"The hotel has a guest rating of {rating} based on "
            f"{review_count} reviews. "
            f"Guests can explore the property through a collection "
            f"of {image_count} available images."
        )

    # -----------------------------------
    # MINOR ERROR: Wrong city
    # -----------------------------------

    elif content_type == "minor_error":

        wrong_city = random.choice(
            [
                city,
                "Berlin",
                "Munich",
                "Hamburg",
                "Frankfurt"
            ]
        )

        # Make sure it is actually different
        while wrong_city == city:

            wrong_city = random.choice(
                [
                    "Berlin",
                    "Munich",
                    "Hamburg",
                    "Frankfurt"
                ]
            )

        return (
            f"{hotel_name} is located in {wrong_city}, {country}. "
            f"The hotel has a guest rating of {rating} based on "
            f"{review_count} reviews."
        )

    # -----------------------------------
    # HALLUCINATION: Unsupported claims
    # -----------------------------------

    elif content_type == "hallucination":

        return (
            f"{hotel_name} is a luxury 5-star hotel located in Munich. "
            f"The property features 250 rooms, a rooftop swimming pool, "
            f"a private spa and a Michelin-starred restaurant. "
            f"Guests can enjoy complimentary airport transfers and "
            f"24-hour butler service."
        )

    return ""


# ---------------------------------------
# Create generated content dataset
# ---------------------------------------

def generate_content():

    hotels = load_hotels()

    generated_content = []

    for _, row in hotels.iterrows():

        # Randomly assign content quality
        content_type = random.choices(
            [
                "good",
                "minor_error",
                "hallucination"
            ],
            weights=[
                70,
                20,
                10
            ],
            k=1
        )[0]

        ai_description = generate_description(
            row,
            content_type
        )

        generated_content.append(
            {
                "hotel_id": row["hotel_id"],
                "hotel_name": row["hotel_name"],
                "content_type": content_type,
                "original_city": row["city"],
                "original_rating": row["rating"],
                "original_review_count": row["review_count"],
                "ai_description": ai_description
            }
        )

    result = pd.DataFrame(generated_content)

    result.to_csv(
        OUTPUT_FILE,
        index=False
    )

    return result


# ---------------------------------------
# Main
# ---------------------------------------

if __name__ == "__main__":

    df = generate_content()

    print("=" * 60)
    print("AI CONTENT GENERATION")
    print("=" * 60)

    print(f"\nTotal descriptions generated: {len(df)}")

    print("\nContent types:")

    print(
        df["content_type"]
        .value_counts()
    )

    print("\nSample generated content:\n")

    print(
        df[
            [
                "hotel_id",
                "content_type",
                "ai_description"
            ]
        ]
        .head(5)
        .to_string(index=False)
    )

    print("\nSaved to:")
    print(OUTPUT_FILE)