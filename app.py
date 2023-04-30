import streamlit as st
import requests
import webbrowser

# Define TMDB API endpoint and API key
TMDB_ENDPOINT = "https://api.themoviedb.org/3"
API_KEY = "2ad720fe7992ff4f30cf6f9e8afb8544"

def search_movies(query):
    # Construct search URL
    search_url = f"{TMDB_ENDPOINT}/search/movie"
    params = {
        "api_key": API_KEY,
        "query": query,
        "page": 1
    }

    # Send request and get response
    response = requests.get(search_url, params=params)
    data = response.json()

    # Extract relevant movie information
    movies = []
    for movie in data["results"]:
        movies.append({
            "id": movie["id"],
            "title": movie["title"],
            "release_date": movie["release_date"],
            "poster_path": movie["poster_path"],
            "overview": movie["overview"]
        })

    return movies


def recommend_movies(movie_id):
    # Construct recommendation URL
    recommend_url = f"{TMDB_ENDPOINT}/movie/{movie_id}/recommendations"
    params = {
        "api_key": API_KEY,
        "page": 1
    }

    # Send request and get response
    response = requests.get(recommend_url, params=params)
    data = response.json()

    # Extract relevant movie information
    movies = []
    for movie in data["results"]:
        movies.append({
            "id": movie["id"],
            "title": movie["title"],
            "release_date": movie["release_date"],
            "poster_path": movie["poster_path"],
            "overview": movie["overview"]
        })

    return movies


def get_trailer(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&append_to_response=videos"
    response = requests.get(url)
    data = response.json()
    if "videos" in data and "results" in data["videos"] and data["videos"]["results"]:
        return data["videos"]["results"][0]["key"]
    return None


# Define Streamlit app layout
st.set_page_config(page_title="Movie Recommendation System")
st.title("Movie Recommendation System")

# Get user input for search query
query = st.text_input("Enter a movie title to search")

if query:
    # Perform search and display results
    movies = search_movies(query)
    if movies:
        st.subheader("Search Results")
        for movie in movies:
            st.write(f"{movie['title']} ({movie['release_date']})")
            if movie["poster_path"]:
                poster_url = f"https://image.tmdb.org/t/p/w500{movie['poster_path']}"
                st.image(poster_url, width=300)
            # Display movie overview
            st.write(f"Overview: {movie['overview']}")
            # Store movie id to display download link and trailer later
            movie_id = movie['id']
            trailer_key = get_trailer(movie_id)
            if trailer_key:
                trailer_url = f"https://www.youtube.com/watch?v={trailer_key}"
                st.write(f"You can watch the trailer here: {trailer_url}")
            # Display download button for the movie
            # download_url = f"https://vegamovies.party/{movie['title']}"
            # st.write(f"Download {movie['title']} here:")
            # if st.button("Download", key=f"download_{movie['title']}"):
            # webbrowser.open(download_url, new=2)
            st.write("---")
    else:
        st.write("No Result Found! Please Search Again..")
