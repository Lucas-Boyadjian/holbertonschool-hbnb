/* 
This file contains the main JavaScript logic for the HBNB (Holberton AirBnB) 
frontend application. It handles user authentication, place management, 
reviews, and API communication with the Flask backend.
*/


let authToken = null;
let allPlaces = [];

/*
Handles DOMContentLoaded event and sets up event listeners 
for filters, login, and review form.
*/
document.addEventListener('DOMContentLoaded', () => {
    checkAuthentication()
    const priceFilter = document.getElementById('price-filter');
    if (priceFilter) {
        priceFilter.innerHTML = `
            <option value="10">10</option>
            <option value="50">50</option>
            <option value="100">100</option>
            <option value="All">All</option>
        `;
        // Handles price filter changes and updates displayed places accordingly.
        document.getElementById('price-filter').addEventListener('change', (event) => {
            const selectedPrice = event.target.value;
            
            let filteredPlaces;
            if (selectedPrice === "All") {
                filteredPlaces = allPlaces;
            } else {
                filteredPlaces = allPlaces.filter(place => Number(place.price) <= Number(selectedPrice));
            }
            displayPlaces(filteredPlaces);
        });
    }
    // Handles login form submission and calls loginUser.
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            await loginUser(email, password);
        });
    }
    // Handles review form submission and calls submitReview.
    const reviewForm = document.getElementById('review-form');
    if (reviewForm) {
        reviewForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const token = getCookie('token');
            const placeId = getPlaceIdFromURL();
            const reviewText = document.getElementById('review-text').value;
            const result = await submitReview(token, placeId, reviewText);
            handleReviewResponse(result, reviewForm);
        });
    }
});


// Sends a POST request to log in the user and stores the token in a cookie.
async function loginUser(email, password) {
    const response = await fetch('http://127.0.0.1:5000/api/v1/auth/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, password })
    });
    
    const result = await handleApiResponse(response);
    
    if (result.error) {
        alert('Login failed: ' + result.error);
    } else {
        document.cookie = `token=${result.access_token}; path=/`;
        authToken = result.access_token;
        alert('Login successful! Welcome!');
        window.location.href = 'index.html';
    }
}


// Checks if the user is authenticated and updates UI accordingly.
function checkAuthentication() {
    const token = getCookie('token');
    authToken = token;
    const loginLink = document.getElementById('login-link');
    const addReviewSection = document.getElementById('add-review');
    const placeId = getPlaceIdFromURL();
    const path = window.location.pathname;
    const homeLogin = path.endsWith('index.html') || document.getElementById('login-form');

    if (!token) {
        if (loginLink) loginLink.style.display = 'block';
        if (addReviewSection) addReviewSection.style.display = 'none';
        if (!homeLogin) {
            alert('You must be logged in to access this page.');
            window.location.href = 'index.html';
        } else {
            fetchPlaces(null);
        }
        
    } else {
        if (loginLink) loginLink.style.display = 'none';
        if (addReviewSection) {
            addReviewSection.style.display = 'block';
            // Fetches place details if authenticated.
            fetchPlaceDetails(token, placeId);
        }
        // Fetch places if the user is authenticated.
        fetchPlaces(token);
    }
    return token;
}


// Fetches all places from the API and displays them.
async function fetchPlaces(token) {
    const headers = {
        'Content-Type': 'application/json'
    };
    
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }
    
    const response = await fetch('http://127.0.0.1:5000/api/v1/places/', {
        method: 'GET',
        headers: headers
    });
    
    const result = await handleApiResponse(response);
    
    if (result.error) {
        alert('Failed to fetch places: ' + result.error);
    } else {
        allPlaces = result.places || result;
        displayPlaces(result.places || result);
    }
}


// Fetches the details of a specific place and displays them.
async function fetchPlaceDetails(token, placeId) {
    const response = await fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}`, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        }
    });
    
    const result = await handleApiResponse(response);
    
    if (result.error) {
        alert('Failed to fetch place details: ' + result.error);
    } else {
        displayPlaceDetails(result);
    }
}


// Sends a POST request to submit a new review for a place.
async function submitReview(token, placeId, reviewText) {
    const reviewRating = document.getElementById('rating').value;
    const response = await fetch('http://127.0.0.1:5000/api/v1/reviews/', {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            place_id: placeId,
            text: reviewText,
            rating: Number(reviewRating)
        })
    });
    
    return await handleApiResponse(response);
}


// Handles the response after submitting a review and refreshes the place details
function handleReviewResponse(result, reviewForm) {
    if (result && !result.error) {
        alert('Review submitted successfully!');
        reviewForm.reset();
        const token = getCookie('token');
        const placeId = getPlaceIdFromURL();
        fetchPlaceDetails(token, placeId);
    } else {
        const errorMessage = result?.error || 'Failed to submit review.';
        alert(errorMessage);
    }
}


// Displays the list of places on the page.
function displayPlaces(places) {
    const placesList = document.getElementById('places-list');
    if (!placesList) {
        return;
    }
    placesList.innerHTML = '';
    places.forEach(place => {
        const placeDiv = document.createElement('div');
        placeDiv.className = 'place-card';
        placeDiv.innerHTML = `
            <h2><img src="images/icon.png" alt="icon" class="icon">${place.title}</h2>
            <img src="${place.image || 'images/icon.png'}" alt="place image" class="place-img">
            <p>Price per night: <strong>${place.price}€</strong></p>
            <button class="details-button" onclick="window.location.href='place.html?id=${place.id}'">View Details</button>
        `;
        placesList.appendChild(placeDiv);
    });
}


// Displays the details of a place, including its reviews.
function displayPlaceDetails(place) {
    const placeDetails = document.getElementById('place-details');
    console.log('place:', place);
    if (!placeDetails)
        return;
    placeDetails.innerHTML = '';

    const placeDetailsDiv = document.createElement('div');
    placeDetailsDiv.className = 'place-info';
    placeDetailsDiv.innerHTML = `
        <h2>${place.title}</h2>
        <img src="${place.image || 'images/icon.png'}" alt="place image" class="placedetails-img">
        <p><strong>Host:</strong> ${place.owner.first_name} ${place.owner.last_name}</p>
        <p><strong>Location:</strong> Latitude: ${place.latitude} | Longitude: ${place.longitude}</p>
        <p><strong>Description:</strong> ${place.description}</p>
        <p><strong>Price per night:</strong> ${place.price}€</p>
        <p><strong>Amenities:</strong> ${place.amenities.map(a => a.name).join(', ')}</p>
    `;
    placeDetails.appendChild(placeDetailsDiv);

    const reviewDetails = document.getElementById('reviews');
    if (reviewDetails) {
        reviewDetails.innerHTML = '<h2>Reviews</h2>';
        if (place.reviews && place.reviews.length > 0) {
            place.reviews.forEach(review => {
                const placeReviewDiv = document.createElement('div');
                placeReviewDiv.className = 'review-card';
                placeReviewDiv.innerHTML = `
                    <p><strong>${review.first_name} ${review.last_name} :</strong></p>
                    <p>${review.text}</p>
                    <p>Rating: ${review.rating}/5</p>
                `;
                reviewDetails.appendChild(placeReviewDiv);
            });
        }
    }
}


// Generic function to handle API responses and extract error messages.
async function handleApiResponse(response) {
    if (response.ok) {
        return await response.json();
    } else {
        const errorData = await response.json();
        return { error: errorData.error || `HTTP ${response.status}: ${response.statusText}` };
    }
}


// Retrieves a cookie value by its name.
function getCookie(name) {
    const cookies = document.cookie.split('; ');
    for (const cookie of cookies) {
        const [key, value] = cookie.split('=');
        if (key === name) {
            return decodeURIComponent(value);
        }
    }
    return null;
}


// Extracts the place ID from the URL query parameters.
function getPlaceIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get('id');
}
