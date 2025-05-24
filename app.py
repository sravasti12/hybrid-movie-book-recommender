from flask import Flask, render_template, request
from fetch_movies import fetch_single_movie_with_genres
from fetch_books import fetch_books_from_google
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

model = SentenceTransformer('all-mpnet-base-v2')

@app.route("/", methods=["GET", "POST"])
def home():
    movie = None
    poster_url = None
    recommendations = []

    if request.method == "POST":
        movie_name = request.form.get("movie_name", "").strip()
        if movie_name:
            movie = fetch_single_movie_with_genres(movie_name)

            if movie:
                # Construct full poster URL if available
                if movie.get("poster_path"):
                    poster_url = f"https://image.tmdb.org/t/p/w500{movie['poster_path']}"

                # Prepare genre query for books
                genre_query = f"{movie['title']} {movie['overview']} " + " ".join(movie['genres']) or "fiction"

                # Fetch books based on genre query (adjust total_results as needed)
                books_df = fetch_books_from_google(genre_query, total_results=100)

                # Compute embeddings
                movie_embed = model.encode([movie['overview']])
                book_embeds = model.encode(books_df['description'].tolist(), show_progress_bar=False)

                # Compute similarities
                similarities = cosine_similarity(movie_embed, book_embeds)[0]

                # Pick top 5 books
                top_indices = similarities.argsort()[-5:][::-1]
                recommendations = books_df.iloc[top_indices].to_dict(orient="records")
            else:
                movie = None  # movie not found

    return render_template("index.html", movie=movie, poster_url=poster_url, recommendations=recommendations)

if __name__ == "__main__":
    app.run(debug=True)
