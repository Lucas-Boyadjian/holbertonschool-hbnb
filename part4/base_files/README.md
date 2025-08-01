# HBNB - Part 4: Frontend Web Application

## Overview

This part of the HBNB project provides a modern and responsive web interface to interact with the HBNB backend API. It focuses on user experience, authentication, place and review management, and a clean, adaptive design.

## Main Features

- **User Authentication:**
  - Secure login with token (cookie) management
  - Display of error and success messages
  - Automatic redirection if the user is not logged in

- **Place Display:**
  - Dynamic list of available places
  - Price filtering
  - Access to detailed place information with images

- **Review Management:**
  - Display of existing reviews for each place
  - Add a new review (with duplicate prevention)
  - Error messages if a duplicate review is attempted

- **Responsive Design:**
  - Uses Flexbox and clamp() for optimal adaptation on all screens
  - Modern interface, harmonious colors, and smooth user experience

## File Structure

- `index.html`: Home page, list of places
- `place.html`: Place details, reviews, and add review form
- `login.html`: Login page
- `add_review.html`: Add review form
- `styles.css`: Main stylesheet, organized by logical sections
- `scripts.js`: JavaScript logic (authentication, place management, reviews, API calls)
- `images/`: Graphic resources

## Technologies Used

- HTML5, CSS3 (Flexbox, clamp, responsive design)
- JavaScript (ES6+, fetch API, cookie management)
- Integration with a Flask REST API

## How to Run the Project

1. Start the Flask backend (see backend documentation)
2. Open `index.html` in a modern browser
3. Browse, log in, view and add reviews!

## Author
Lucas Boyadjian