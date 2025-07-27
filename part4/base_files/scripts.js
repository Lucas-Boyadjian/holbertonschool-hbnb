/* 
  This is a SAMPLE FILE to get you started.
  Please, follow the project instructions to complete the tasks.
*/

document.addEventListener('DOMContentLoaded', () => {
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

    if (!token) {
        loginLink.style.display = 'block';
    } else {
        loginLink.style.display = 'none';
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
    console.log('places:', places);
    allPlaces = places;
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
            <h2><img src="images/icon.png" alt="icon" class="icon">${place.title}</h2>
            <p>Price per night:${place.price}€</p>
            <p>${place.description ? place.description : ''}</p>
            <p>Latitude: ${place.latitude}</p>
            <p>Longitude: ${place.longitude}</p>
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
    const cards = document.querySelectorAll('.place-card');
    cards.forEach(card => {
        const priceText = card.querySelector('p').textContent;
        const price = parseFloat(priceText);
        if (selectedPrice === 'All' || price <= parseInt(selectedPrice, 10)) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
});