/* 
  This is a SAMPLE FILE to get you started.
  Please, follow the project instructions to complete the tasks.
*/

document.addEventListener('DOMContentLoaded', () => {
    checkAuthentication();
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            // Your code to handle form submission
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            await loginUser(email, password);
        });
    }       
});

async function loginUser(email, password) {
    const response = await fetch('http://127.0.0.1:5000/api/v1/auth/login', {
        method: 'POST',
        headers: {
                    'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, password })
    });
    // Handle the response
    if (response.ok) {
        const data = await response.json();
        document.cookie = `token=${data.access_token}; path=/`;
        window.location.href = 'index.html';
    } else {
        alert('Login failed: ' + response.statusText);
    }
}

function checkAuthentication() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');
    const addReviewSection = document.getElementById('add-review');
    const placeId = getPlaceIdFromURL();
    const path = window.location.pathname;
    const homeLogin = path.endsWith('index.html') || document.getElementById('login-form');

    if (!token) {
        if (loginLink) loginLink.style.display = 'block';
        if (addReviewSection) addReviewSection.style.display = 'none';
        if (!homeLogin) window.location.href = 'index.html';
        
    } else {
        if (loginLink) loginLink.style.display = 'none';
        if (addReviewSection) {
            addReviewSection.style.display = 'block';
            // Store the token for later use
            fetchPlaceDetails(token, placeId);
        }
        // Fetch places data if the user is authenticated
        fetchPlaces(token);
    }
}

function getCookie(name) {
    // Function to get a cookie value by its name
    // Your code here
    const cookies = document.cookie.split('; ');
    for (const cookie of cookies) {
        const [key, value] = cookie.split('=');
        if (key === name) {
            return decodeURIComponent(value);
        }
    }
    return null;
}

async function fetchPlaces(token) {
    // Make a GET request to fetch places data
    // Include the token in the Authorization header
    // Handle the response and pass the data to displayPlaces function
    const response = await fetch('http://127.0.0.1:5000/api/v1/places/', {
        method: 'GET',
        headers: { 
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        }
    });
    if (response.ok) {
        const data = await response.json();
        allPlaces = data.places || data;
        displayPlaces(data.places || data);
    } else {
        alert('Failed to fetch places');
    }
}

let allPlaces = [];

function displayPlaces(places) {
    // Clear the current content of the places list
    // Iterate over the places data
    // For each place, create a div element and set its content
    // Append the created element to the places list
    const placesList = document.getElementById('places-list');
    if (!placesList) {
        console.error("#places-list element not found in HTML.");
        return;
    }
    placesList.innerHTML = '';
    places.forEach(place => {
        const placeDiv = document.createElement('div');
        placeDiv.className = 'place-card';
        placeDiv.innerHTML = `
            <h2>${place.title}</h2>
            <img src="${place.image || 'images/icon.png'}" alt="place image" class="place-img">
            <p>Price per night: <strong>${place.price}€</strong></p>
            <button class="details-button" onclick="window.location.href='place.html?id=${place.id}'">View Details</button>
        `;
        placesList.appendChild(placeDiv);
    });
}

document.addEventListener('DOMContentLoaded', () => {
    const priceFilter = document.getElementById('price-filter');
    if (priceFilter) {
        priceFilter.innerHTML = `
            <option value="10">10</option>
            <option value="50">50</option>
            <option value="100">100</option>
            <option value="All">All</option>
        `;
    }
    checkAuthentication();
});

document.getElementById('price-filter').addEventListener('change', (event) => {
     // Get the selected price value
    // Iterate over the places and show/hide them based on the selected price
    const selectedPrice = event.target.value;
    const token = getCookie('token');
    if (!token) {
        const cards = document.querySelectorAll('.place-card');
        cards.forEach(card => {
            const priceText = card.querySelector('p').textContent;
            const match = priceText.match(/(\d+)/);
            const price = match ? parseFloat(match[1]) : 0;
            if (selectedPrice === "All" || price <= Number(selectedPrice)) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        });
    } else {
        let filteredPlaces;
        if (selectedPrice === "All") {
            filteredPlaces = allPlaces;
        } else {
            filteredPlaces = allPlaces.filter(place => Number(place.price) <= Number(selectedPrice));
        }
        displayPlaces(filteredPlaces);
    }
});

function getPlaceIdFromURL() {
    // Extract the place ID from window.location.search
    // Your code here
    const params = new URLSearchParams(window.location.search);
    return params.get('id');
}

async function fetchPlaceDetails(token, placeId) {
    // Make a GET request to fetch place details
    // Include the token in the Authorization header
    // Handle the response and pass the data to displayPlaceDetails function
    const response = await fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}`, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        }
    });
    if (response.ok) {
        const data = await response.json();
        displayPlaceDetails(data);
    } else {
        alert('Failed to fetch place details');
    }
}

function displayPlaceDetails(place) {
    // Clear the current content of the place details section
    // Create elements to display the place details (name, description, price, amenities and reviews)
    // Append the created elements to the place details section
    const placeDetailsSection = document.getElementById('place-details');
    if (!placeDetailsSection) 
        return;
    placeDetailsSection.innerHTML = '';

    const infoDiv = document.createElement('div');
    infoDiv.className = 'place-info';

    const bigImg = document.createElement('img');
    bigImg.src = place.image || 'images/icon.png';
    bigImg.className = 'placedetails-img';
    infoDiv.appendChild(bigImg);

    const title = document.createElement('h2');
    title.textContent = place.title;
    infoDiv.appendChild(title);

    if (place.description) {
        const desc = document.createElement('p');
        desc.innerHTML = `<strong>Description:</strong> ${place.description}`;
        infoDiv.appendChild(desc);
    }

    if (place.price !== undefined) {
        const price = document.createElement('p');
        price.innerHTML = `<strong>Price per night:</strong> ${place.price}€`;
        infoDiv.appendChild(price);
    }

    if (place.amenities && place.amenities.length > 0) {
        const amenities = document.createElement('p');
        amenities.innerHTML = `<strong>Amenities:</strong> ${place.amenities.map(a => a.name).join(', ')}`;
        infoDiv.appendChild(amenities);
    }
    document.getElementById('place-details').appendChild(infoDiv);

}