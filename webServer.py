from flask import Flask, request, render_template
import pickle
import requests
import pandas as pd
from scipy.sparse import csr_matrix

app = Flask(__name__)

knn = pickle.load(open('knn_model.pkl', 'rb'))

final_dataset = pd.read_csv('final_dataset.csv')
movies = pd.read_csv('movies.csv')
csr_data = csr_matrix(final_dataset.values)
final_dataset.reset_index(inplace=True)

API_KEY = '2ba5537a'

# Function to fetch movie data from OMDb API
def get_movie_info(movie_title):
    url = f"http://www.omdbapi.com/?t={movie_title}&apikey={API_KEY}"
    try:
        response = requests.get(url)
        data = response.json()

        if data and data.get('Response', 'False') == 'True':
            return {
                "title": data.get('Title', 'N/A'),
                "poster": data.get('Poster', 'N/A'),
                "year": data.get('Year', 'N/A')
            }
        else:
            # Handle case where no data is returned
            return {
                "title": movie_title,
                "poster": None,
                "year": "N/A"
            }
    except Exception as e:
        print(f"Error fetching data from OMDb API: {e}")
        # In case of error, return default values
        return {
            "title": movie_title,
            "poster": None,
            "year": "N/A"
        }

def Recommendation(movie_name):
    movie_name_lower = movie_name.lower()
    movie_list = movies[movies['title'].str.lower().str.contains(movie_name_lower, na=False)]
    
    if not movie_list.empty:
        movie_idx = movie_list.iloc[0]['movieId']
        movie_idx = final_dataset[final_dataset['movieId'] == movie_idx].index[0]
        
        distance, indices = knn.kneighbors(csr_data[movie_idx], n_neighbors=11)
        
        rec_movies_indices = sorted(
            list(zip(indices.squeeze().tolist(), distance.squeeze().tolist())),
            key=lambda x: x[1]
        )[:0:-1]
        
        recommended_movies = []
        for val in rec_movies_indices:
            movie_idx = final_dataset.iloc[val[0]]['movieId']
            idx = movies[movies['movieId'] == movie_idx].index[0]
            movie_title = movies.iloc[idx]['title']

            # Fetch movie info from OMDb API
            movie_info = get_movie_info(movie_title)

            recommended_movies.append({
                'Title': movie_info['title'],
                'Poster': movie_info['poster'],
                'Year': movie_info['year'],
                'Distance': val[1]
            })
        
        return recommended_movies
    else:
        return "Movie not found..."

print(final_dataset.shape)  # This should show (num_samples, 378) or whatever number of features your model was trained on

# Check the shape of your csr_data
print(csr_data.shape) 

@app.route('/', methods=['GET', 'POST'])
def index():
    recommendations = []
    selected_movie_name = None
    
    if request.method == 'POST':
        selected_movie_name = request.form['movie']
        recommendations = Recommendation(selected_movie_name)  # The new Recommendation returns a list of dictionaries
        
    return render_template('index.html', movies=movies['title'].values, recommendations=recommendations, selected_movie_name=selected_movie_name)


if __name__ == '__main__':
    app.run(debug=True)