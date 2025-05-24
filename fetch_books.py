import requests
import pandas as pd

def fetch_books_from_google(query, total_results=40):
    """
    Fetch books from Google Books API based on query.
    Returns a pandas DataFrame with book titles and descriptions.
    """
    books = []
    max_results_per_request = 40  # Google Books max per request

    for start_index in range(0, total_results, max_results_per_request):
        url = (
            "https://www.googleapis.com/books/v1/volumes?"
            f"q={query}&startIndex={start_index}&maxResults={min(max_results_per_request, total_results - start_index)}"
        )
        response = requests.get(url)
        if response.status_code != 200:
            break
        data = response.json()

        items = data.get('items', [])
        for item in items:
            volume_info = item.get('volumeInfo', {})
            title = volume_info.get('title', 'No Title')
            description = volume_info.get('description', 'No Description')
            books.append({
                'title': title,
                'description': description
            })

    return pd.DataFrame(books)
