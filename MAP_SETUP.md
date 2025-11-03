# ResQTrack - Map Integration Setup

## OpenStreetMap + Leaflet.js Integration

The ResQTrack application now uses OpenStreetMap with Leaflet.js for enhanced map functionality. This implementation is completely free and requires no API keys.

### 1. Features Added

#### Map Improvements
- **OpenStreetMap Integration**: Uses free OpenStreetMap tiles with Leaflet.js
- **No API Key Required**: Completely free to use with no billing concerns
- **Enhanced Geocoding**: Uses Nominatim API for accurate location resolution
- **Custom Markers**: Hospital and police station markers with custom icons
- **Interactive Popups**: Click on markers to see detailed information
- **Location Picker**: Interactive map for selecting precise locations

#### Data Management Features
- **CSV File Management**: View and delete uploaded CSV files
- **Bulk Data Clearing**: Clear all data for specific service types (hospitals, police stations, etc.)
- **Individual Entry Deletion**: Delete specific entries from emergency services
- **File Upload Tracking**: Monitor uploaded files with size and modification date

### 2. New API Endpoints

The following new endpoints have been added to the backend:

- `GET /data/uploaded-files` - List uploaded CSV files
- `DELETE /data/delete-file` - Delete a specific CSV file
- `DELETE /data/clear-data/<service_type>` - Clear all data for a service type
- `DELETE /data/delete-entry/<service_type>/<entry_id>` - Delete a specific entry

### 3. Usage

#### Location Picker (`location-picker.html`)
- Search for locations using Nominatim geocoding
- Use device location with geolocation API
- Click on map to select precise coordinates
- Copy coordinates or send to backend
- Mobile-friendly responsive design

#### Hospitals Page
- Switch between List View and Map View
- Click on map markers to see hospital details
- Hospitals are geocoded automatically from their location field

#### Admin Dashboard
- View all emergency services on interactive maps
- Add new locations using the location picker map
- Manage uploaded CSV files
- Clear data or delete individual entries

#### Data Dashboard
- Import CSV files for different service types
- View uploaded files and delete them
- Clear all data for specific service types
- Delete individual emergency service entries

### 4. Technical Implementation

#### Libraries Used
- **Leaflet.js**: Open-source JavaScript library for interactive maps
- **OpenStreetMap**: Free, open-source map data
- **Nominatim**: Free geocoding service for OpenStreetMap

#### Configuration
The map settings are configured in `frontend/config.js`:
```javascript
const CONFIG = {
    MAP_DEFAULT_CENTER: { lat: 20.5937, lng: 78.9629 }, // India center
    MAP_DEFAULT_ZOOM: 5,
    MAP_MAX_ZOOM: 19,
    MAP_TILE_LAYER: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
    NOMINATIM_BASE_URL: 'https://nominatim.openstreetmap.org',
    NOMINATIM_SEARCH_LIMIT: 5,
    NOMINATIM_COUNTRY_CODES: 'in'
};
```

### 5. Mobile-Friendly Features

- Responsive design that works on all screen sizes
- Touch-friendly map interactions
- Optimized marker sizes for mobile devices
- Geolocation support for mobile browsers
- Search functionality with autocomplete

### 6. Advantages Over Google Maps

- **No API Key Required**: No need to register or manage API keys
- **No Billing**: Completely free with no usage limits
- **Open Source**: Full control over the implementation
- **Privacy**: No data sent to Google
- **Customizable**: Easy to customize markers, popups, and styling

### 7. Troubleshooting

If maps don't load:
1. Check browser console for error messages
2. Ensure internet connection is available
3. Verify that Leaflet.js is loading correctly
4. Check that OpenStreetMap tiles are accessible

For more information, visit the [Leaflet.js documentation](https://leafletjs.com/) and [OpenStreetMap](https://www.openstreetmap.org/).
