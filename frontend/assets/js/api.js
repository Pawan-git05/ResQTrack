// ===============================
// ResQTrack Frontend API
// Centralized API helper + convenience methods
// ===============================

const API_BASE = 'http://127.0.0.1:5000/api';

// -------------------------------
// Generic request handler
// -------------------------------
async function apiRequest(
    path,
    { method = 'GET', body = null, isForm = false, token = null } = {},
    uiOptions = {}
) {
    const { showLoading = true, showToast = true, buttonElement = null } = uiOptions || {};
    const headers = {};

    if (!isForm) headers['Content-Type'] = 'application/json';
    if (token) headers['Authorization'] = `Bearer ${token}`;

    const fetchOptions = {
        method,
        headers,
        credentials: 'include'
    };

    if (body) fetchOptions.body = isForm ? body : JSON.stringify(body);

    try {
        if (showLoading && window.LoadingOverlay?.show) window.LoadingOverlay.show();
        if (buttonElement && window.ButtonLoader?.setLoading) window.ButtonLoader.setLoading(buttonElement, true);

        // normalize path: allow callers to pass '/data/..' or '/api/data/..'
        let normalizedPath = String(path || '');
        if (normalizedPath.startsWith('/api')) normalizedPath = normalizedPath.slice(4);
        if (!normalizedPath.startsWith('/')) normalizedPath = '/' + normalizedPath;

        const res = await fetch(`${API_BASE}${normalizedPath}`, fetchOptions);
        const data = await res.json().catch(() => ({}));

        if (!res.ok) {
            const message = data.error || data.message || 'Request failed';
            if (showToast && window.ToastManager) window.ToastManager.error(message);
            const err = new Error(message);
            err.response = res;
            err.data = data;
            throw err;
        }

        if (showToast && data.message && window.ToastManager) window.ToastManager.success(data.message);
        return data;

    } finally {
        if (showLoading && window.LoadingOverlay?.hide) window.LoadingOverlay.hide();
        if (buttonElement && window.ButtonLoader?.setLoading) window.ButtonLoader.setLoading(buttonElement, false);
    }
}

// -------------------------------
// Global convenience API (older code compatibility)
// -------------------------------
window.ResQApi = {

    // AUTH
    login: (email, password, options) =>
        apiRequest('/auth/login', { method: 'POST', body: { email, password } }, options),

    me: (token, options) =>
        apiRequest('/auth/me', { method: 'GET', token }, options),

    // CASES
    reportCase: (formData, options) =>
        apiRequest('/cases', { method: 'POST', isForm: true, body: formData }, options),

    listCases: (token, options) =>
        apiRequest('/cases', { method: 'GET', token }, options),

    // REGISTRATION
    registerNGO: (payload, options) =>
        apiRequest('/registrations/ngo', { method: 'POST', body: payload }, options),

    registerVolunteer: (payload, options) =>
        apiRequest('/registrations/volunteer', { method: 'POST', body: payload }, options),

    // HOSPITAL API
    listHospitals: (options) =>
        apiRequest('/hospitals', { method: 'GET' }, options),

    addHospital: (payload, token, options) =>
        apiRequest('/hospitals', { method: 'POST', body: payload, token }, options),

    // DONATIONS
    createDonation: (payload, options) =>
        apiRequest('/donations', { method: 'POST', body: payload }, options),

    listDonations: (options) =>
        apiRequest('/donations', { method: 'GET' }, options),

    // UPLOADS
    uploadFile: (formData, token, options) =>
        apiRequest('/uploads', { method: 'POST', isForm: true, body: formData, token }, options),

    listUploadedFiles: (options) =>
        apiRequest('/uploads/files', { method: 'GET' }, options),

    // ADMIN
    adminListNGOs: (token, options) =>
        apiRequest('/admin/ngos', { method: 'GET', token }, options),

    adminListVolunteers: (token, options) =>
        apiRequest('/admin/volunteers', { method: 'GET', token }, options),

    adminListHospitals: (token, options) =>
        apiRequest('/admin/hospitals', { method: 'GET', token }, options),

    adminListPoliceStations: (token, options) =>
        apiRequest('/admin/police-stations', { method: 'GET', token }, options),

    adminListFireStations: (token, options) =>
        apiRequest('/admin/fire-stations', { method: 'GET', token }, options),

    adminListBloodBanks: (token, options) =>
        apiRequest('/admin/blood-banks', { method: 'GET', token }, options),

    adminListEmergencyContacts: (token, options) =>
        apiRequest('/admin/emergency-contacts', { method: 'GET', token }, options),

    // Approvals (backend uses PATCH)
    approveNGO: (id, token, options) =>
        apiRequest(`/admin/ngos/${id}/approve`, { method: 'PATCH', token }, options),

    approveVolunteer: (id, token, options) =>
        apiRequest(`/admin/volunteers/${id}/approve`, { method: 'PATCH', token }, options),

    // Delete entry (if implemented on backend; adapt if route differs)
    adminDeleteEntry: (type, id, token, options) =>
        apiRequest(`/admin/${type}/${id}`, { method: 'DELETE', token }, options),

    // CSV upload for admin (explicit helper)
    adminUploadCSV: (serviceType, formData, token, options) =>
        apiRequest(`/admin/upload-csv/${serviceType}`, { method: 'POST', isForm: true, body: formData, token }, options),

    // Data import endpoints (if your backend exposes /data/import/*)
    importDataset: (datasetType, formData, token, options) =>
        apiRequest(`/data/import/${datasetType}`, { method: 'POST', isForm: true, body: formData, token }, options),

    getUploadedCSVs: (options) =>
        apiRequest('/data/files', { method: 'GET' }, options),

    getStatistics: (options) =>
        apiRequest('/data/statistics', { method: 'GET' }, options),

    getLocationDistribution: (options) =>
        apiRequest('/data/locations', { method: 'GET' }, options),
};

// -------------------------------
// Optional class wrapper (used by DataDashboard)
class API {
    constructor() {
        this.baseURL = API_BASE;
    }

    // normalize and delegate to apiRequest
    get(path, opts) { return apiRequest(path, { method: 'GET', ...(opts || {}) }, opts?.uiOptions); }
    post(path, body, opts) { 
        const { isForm = false, token = null } = opts || {};
        return apiRequest(path, { method: 'POST', body, isForm, token }, opts?.uiOptions); 
    }
    patch(path, body, opts) { 
        const { isForm = false, token = null } = opts || {};
        return apiRequest(path, { method: 'PATCH', body, isForm, token }, opts?.uiOptions); 
    }
    delete(path, opts) {
        const { token = null } = opts || {};
        return apiRequest(path, { method: 'DELETE', token }, opts?.uiOptions);
    }
}
window.API = API;
