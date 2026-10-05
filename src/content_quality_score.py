import pandas as pd
import numpy as np


df = pd.read_csv("data/hotels.csv")


# 1. Description Quality Score

def description_score(description):

    if pd.isna(description):
        return 0

    length = len(str(description))

    if length >= 250:
        return 100
    elif length >= 150:
        return 80
    elif length >= 100:
        return 60
    else:
        return 30


df["description_score"] = df["description"].apply(
    description_score
)


# ---------------------------------
# 2. Image Quality Score
# ---------------------------------

df["image_score"] = (
    df["image_count"] / 20 * 100
).clip(upper=100)


# ---------------------------------
# 3. Rating Quality Score
# ---------------------------------

def rating_score(rating):

    if pd.isna(rating):
        return 0

    if 0 <= rating <= 5:
        return 100

    return 0


df["rating_score"] = df["rating"].apply(
    rating_score
)


# ---------------------------------
# 4. Review Coverage Score
# ---------------------------------

df["review_score"] = (
    df["review_count"] / 1000 * 100
).clip(upper=100)


# ---------------------------------
# 5. Overall Content Quality Score
# ---------------------------------

df["content_quality_score"] = (
    df["description_score"] * 0.30
    + df["image_score"] * 0.25
    + df["rating_score"] * 0.20
    + df["review_score"] * 0.25
)


df["content_quality_score"] = (
    df["content_quality_score"].round(2)
)


# ---------------------------------
# 6. Quality Category
# ---------------------------------

def quality_category(score):

    if score >= 85:
        return "Excellent"

    elif score >= 70:
        return "Good"

    elif score >= 50:
        return "Needs Improvement"

    else:
        return "Poor"


df["quality_category"] = df["content_quality_score"].apply(
    quality_category
)


# ---------------------------------
# 7. Save Results
# ---------------------------------

output_file = "data/hotels_with_quality_score.csv"

df.to_csv(
    output_file,
    index=False
)


# ---------------------------------
# 8. Print Summary
# ---------------------------------

print("=" * 60)
print("HOTEL CONTENT QUALITY SCORE")
print("=" * 60)

print(f"\nTotal hotels analysed: {len(df)}")

print("\nQuality category distribution:")
print(
    df["quality_category"]
    .value_counts()
    .sort_index()
)

print("\nAverage content quality score:")
print(
    round(df["content_quality_score"].mean(), 2)
)

print("\nTop 10 hotels:")
print(
    df[
        [
            "hotel_name",
            "city",
            "content_quality_score",
            "quality_category"
        ]
    ]
    .sort_values(
        "content_quality_score",
        ascending=False
    )
    .head(10)
    .to_string(index=False)
)

print("\nLowest 10 hotels:")
print(
    df[
        [
            "hotel_name",
            "city",
            "content_quality_score",
            "quality_category"
        ]
    ]
    .sort_values(
        "content_quality_score"
    )
    .head(10)
    .to_string(index=False)
)

print("\nSaved to:")
print(output_file)