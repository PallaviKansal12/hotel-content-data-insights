import pandas as pd

# Load hotel dataset
df = pd.read_csv("data/hotels.csv")

print("=" * 50)
print("HOTEL DATA QUALITY REPORT")
print("=" * 50)

# Basic information
print(f"\nTotal hotels: {len(df)}")

# 1. Missing descriptions
missing_descriptions = df["description"].isna().sum()
print(f"Missing descriptions: {missing_descriptions}")

# 2. Invalid ratings
invalid_ratings = ((df["rating"] < 0) | (df["rating"] > 5)).sum()
print(f"Invalid ratings: {invalid_ratings}")

# 3. Hotels with fewer than 3 images
low_image_count = (df["image_count"] < 3).sum()
print(f"Hotels with fewer than 3 images: {low_image_count}")

# 4. Duplicate hotel names
duplicate_names = df["hotel_name"].duplicated().sum()
print(f"Duplicate hotel names: {duplicate_names}")

# 5. Missing values across all columns
print("\nMissing values by column:")
print(df.isnull().sum())

# 6. Overall quality summary
total_issues = (
    missing_descriptions
    + invalid_ratings
    + low_image_count
    + duplicate_names
)

print("\n" + "=" * 50)
print(f"Total identified data-quality issues: {total_issues}")
print("=" * 50)