from fetch_books import fetch_books_from_google
from fetch_movies import fetch_single_movie_with_genres
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

def main():
    print("🎬 Enter a movie name (or type 'exit' to quit):")
    while True:
        movie_name = input().strip()
        if movie_name.lower() == 'exit':
            print("Exiting...")
            break

        movie = fetch_single_movie_with_genres(movie_name)
        if movie is None:
            print("Movie not found. Try another movie.")
            continue

        print(f"\nMovie: {movie['title']}")
        print(f"Genres: {', '.join(movie['genres'])}")
        print(f"Overview: {movie['overview'][:300]}...\n")

        # Build query for books - including movie title, overview, and common genres keywords
        genre_keywords = " ".join(movie['genres']) if movie['genres'] else "fiction"
        genre_query = f"{movie['title']} {movie['overview']} {genre_keywords} romance fiction contemporary drama"

        print("Fetching books from Google Books API...")
        books_df = fetch_books_from_google(genre_query, total_results=100)

        if books_df.empty:
            print("No books found for this query.")
            continue

        print("Building embeddings and calculating similarity...")

        model = SentenceTransformer('all-mpnet-base-v2')

        movie_embed = model.encode([movie['overview']])
        book_embeds = model.encode(books_df['description'].tolist(), show_progress_bar=True)

        similarities = cosine_similarity(movie_embed, book_embeds)[0]

        top_indices = similarities.argsort()[-5:][::-1]
        recommendations = books_df.iloc[top_indices]

        print(f"\nTop book recommendations based on '{movie['title']}':\n")
        for _, row in recommendations.iterrows():
            print(f"Book: {row['title']}")
            print(f"Description: {row['description'][:300]}...\n")

if __name__ == "__main__":
    main()
