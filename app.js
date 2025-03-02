// Function to display movies
function displayMovies(movies) {
    movieList.innerHTML = ''; // Clear any previous movies
    movies.forEach(movie => {
        const movieCard = document.createElement('div');
        movieCard.classList.add('movie-card');

        const moviePoster = document.createElement('img');
        moviePoster.classList.add('movie-poster');
        moviePoster.src = movie.Poster || 'default-poster.jpg';  // Default image if poster is not available
        moviePoster.alt = movie.Title;

        const movieTitle = document.createElement('div');
        movieTitle.classList.add('movie-title');
        movieTitle.textContent = movie.Title;

        const movieYear = document.createElement('div');
        movieYear.classList.add('movie-year');
        movieYear.textContent = movie.Year;

        movieCard.appendChild(moviePoster);
        movieCard.appendChild(movieTitle);
        movieCard.appendChild(movieYear);

        movieList.appendChild(movieCard);
    });
}
