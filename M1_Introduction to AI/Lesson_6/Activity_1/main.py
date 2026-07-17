'''
Movie Recommendation System
'''

import time
import pandas as pd
from textblob import TextBlob

# Load the dataset
try:
    df = pd.read_csv("imdb_top_1000.csv")
except FileNotFoundError:
    print("Error: 'imdb_top_1000.csv' not found.")
    exit()

# Get all unique genres
genres = sorted({
    genre.strip()
    for row in df["Genre"].dropna().str.split(", ")
    for genre in row
})

# Loading animation
def dots():
    for _ in range(3):
        print(".", end="", flush=True)
        time.sleep(0.5)
    print()

# Convert polarity to mood
def sentiment(polarity):
    if polarity > 0:
        return "Positive"
    elif polarity < 0:
        return "Negative"
    else:
        return "Neutral"

# Recommend movies
def recommend(genre=None, mood=None, rating=None, n=5):

    data = df

    # Filter by genre
    if genre:
        data = data[data["Genre"].str.contains(genre, case=False, na=False)]

    # Filter by rating
    if rating is not None:
        data = data[data["IMDB_Rating"] >= rating]

    if data.empty:
        return "No suitable movie recommendations found."

    recommendations = []

    for _, row in data.sample(frac=1).iterrows():

        overview = row["Overview"]

        if pd.isna(overview):
            continue

        polarity = TextBlob(overview).sentiment.polarity

        # Recommend only positive-overview movies
        if mood:
            if polarity >= 0:
                recommendations.append((row["Series_Title"], polarity))
        else:
            recommendations.append((row["Series_Title"], polarity))

        if len(recommendations) == n:
            break

    if recommendations:
        return recommendations
    else:
        return "No suitable movie recommendations found."

# Display recommendations
def show(recommendations):

    print("\nMovie Recommendations:\n")

    for i, (title, polarity) in enumerate(recommendations, start=1):
        print(f"{i}. {title}")
        print(f"   Sentiment: {sentiment(polarity)}")
        print(f"   Polarity : {polarity:.2f}\n")

# Get genre
def get_genre():

    print("\nAvailable Genres:\n")

    for i, genre in enumerate(genres, start=1):
        print(f"{i}. {genre}")

    while True:

        choice = input("\nEnter genre number or name: ").strip()

        if choice.isdigit():

            index = int(choice)

            if 1 <= index <= len(genres):
                return genres[index - 1]

        if choice.title() in genres:
            return choice.title()

        print("Invalid input. Try again.")

# Get minimum rating
def get_rating():

    while True:

        choice = input("Enter minimum IMDB rating (7.6-9.3) or 'skip': ")

        if choice.lower() == "skip":
            return None

        try:
            rating = float(choice)

            if 7.6 <= rating <= 9.3:
                return rating

            print("Rating should be between 7.6 and 9.3.")

        except ValueError:
            print("Invalid input.")

# ---------------- MAIN PROGRAM ----------------

print("Welcome to the AI Movie Recommendation System\n")

name = input("Enter your name: ")

genre = get_genre()

mood = input("\nHow do you feel today? ")

print("\nAnalyzing your mood", end="")
dots()

mood_score = TextBlob(mood).sentiment.polarity

print(f"Detected Mood: {sentiment(mood_score)}")
print(f"Polarity Score: {mood_score:.2f}")

rating = get_rating()

print("\nFinding movies", end="")
dots()

movies = recommend(
    genre=genre,
    mood=mood,
    rating=rating,
    n=5
)

if isinstance(movies, str):
    print(movies)
else:
    print(f"\nHello {name}!\n")
    show(movies)

while True:

    choice = input("Do you want more recommendations? (yes/no): ").lower()

    if choice == "yes":

        movies = recommend(
            genre=genre,
            mood=mood,
            rating=rating,
            n=5
        )

        if isinstance(movies, str):
            print(movies)
        else:
            show(movies)

    elif choice == "no":
        print("Enjoy your movie!")
        break

    else:
        print("Invalid choice.")