import pandas as pd
import numpy as np
from faker import Faker
import random

fake = Faker()

random.seed(42)
np.random.seed(42)

cities = [
    "Dusseldorf",
    "Cologne",
    "Aachen",
    "Berlin",
    "Munich",
    "Hamburg",
    "Frankfurt",
    "Stuttgart"
]

hotels = []

for i in range(1, 501):

    city = random.choice(cities)

    rating = round(np.random.uniform(2.5, 5.0), 1)
    review_count = random.randint(5, 5000)
    image_count = random.randint(1, 30)

    description = fake.text(
        max_nb_chars=random.randint(100, 400)
    )

    hotels.append({
        "hotel_id": f"H{i:04d}",
        "hotel_name": f"{fake.last_name()} Hotel {i}",
        "city": city,
        "country": "Germany",
        "rating": rating,
        "review_count": review_count,
        "description": description,
        "image_count": image_count,
        "price": round(random.uniform(50, 350), 2)
    })

df = pd.DataFrame(hotels)

# ---------------------------------
# Introduce data-quality problems
# ---------------------------------

# Missing descriptions
missing_indices = np.random.choice(
    df.index,
    size=25,
    replace=False
)

df.loc[missing_indices, "description"] = None

# Invalid ratings
invalid_indices = np.random.choice(
    df.index,
    size=10,
    replace=False
)

df.loc[invalid_indices, "rating"] = 5.8

# Very few images
low_image_indices = np.random.choice(
    df.index,
    size=20,
    replace=False
)

df.loc[low_image_indices, "image_count"] = 1

# Duplicate hotel names
df.loc[100, "hotel_name"] = df.loc[50, "hotel_name"]
df.loc[200, "hotel_name"] = df.loc[150, "hotel_name"]

# Save dataset
df.to_csv(
    "data/hotels.csv",
    index=False
)

print("Hotel dataset created successfully!")
print(f"Number of hotels: {len(df)}")
print("Saved to: data/hotels.csv")