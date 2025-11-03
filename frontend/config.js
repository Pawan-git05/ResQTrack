// Configuration file for ResQTrack frontend
// Using OpenStreetMap + Leaflet.js (no API key required)

const CONFIG = {
    // API Base URL
    API_BASE_URL: 'http://localhost:5000',
    
    // Map default settings (OpenStreetMap + Leaflet)
    MAP_DEFAULT_CENTER: { lat: 20.5937, lng: 78.9629 }, // India center
    MAP_DEFAULT_ZOOM: 5,
    MAP_MAX_ZOOM: 19,
    
    // OpenStreetMap tile layer settings
    MAP_TILE_LAYER: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
    MAP_ATTRIBUTION: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    
    // Nominatim geocoding settings
    NOMINATIM_BASE_URL: 'https://nominatim.openstreetmap.org',
    NOMINATIM_SEARCH_LIMIT: 5,
    NOMINATIM_COUNTRY_CODES: 'in', // India
    
    // Upload settings
    MAX_FILE_SIZE: 10 * 1024 * 1024, // 10MB
    ALLOWED_FILE_TYPES: ['csv', 'json']
};

// Make config available globally
window.CONFIG = CONFIG;
