import axios from 'axios';
import './app.css';

// Set up axios CSRF token
const token = document.querySelector('meta[name="csrf-token"]');
if (token) {
    axios.defaults.headers.common['X-CSRF-TOKEN'] = token.getAttribute('content');
}

// Global app initialization
document.addEventListener('DOMContentLoaded', () => {
    console.log('DILG Dashboard initialized');
});
