const API_BASE = 'http://localhost:5000';

async function apiRequest(path, { method = 'GET', body = null, isForm = false, token = null } = {}, uiOptions = {}) {
    const { showLoading = true, showToast = true, buttonElement = null } = uiOptions || {};
    const headers = {};
    if (!isForm) headers['Content-Type'] = 'application/json';
    if (token) headers['Authorization'] = `Bearer ${token}`;

    const fetchOptions = { method, headers, credentials: 'include' };
    if (body) fetchOptions.body = isForm ? body : JSON.stringify(body);

    try {
        if (showLoading && window.LoadingOverlay && window.LoadingOverlay.show) window.LoadingOverlay.show();
        if (buttonElement && window.ButtonLoader && window.ButtonLoader.setLoading) window.ButtonLoader.setLoading(buttonElement, true);

        const res = await fetch(`${API_BASE}${path}`, fetchOptions);
        const data = await res.json().catch(() => ({}));
        if (!res.ok) {
            const msg = data && (data.error || data.message) ? (data.error || data.message) : 'Request failed';
            if (showToast && window.ToastManager) window.ToastManager.error(msg);
            const err = new Error(msg);
            err.status = res.status;
            throw err;
        }
        if (showToast && data && data.message && window.ToastManager) window.ToastManager.success(data.message);
        return data;
    } catch (err) {
        const networkMsg = (err && err.status) ? err.message : 'Network error. Please try again.';
        if (showToast && window.ToastManager && !err.status) window.ToastManager.error(networkMsg);
        throw err;
    } finally {
        if (showLoading && window.LoadingOverlay && window.LoadingOverlay.hide) window.LoadingOverlay.hide();
        if (buttonElement && window.ButtonLoader && window.ButtonLoader.setLoading) window.ButtonLoader.setLoading(buttonElement, false);
    }
}

// API Class for data dashboard
class API {
    constructor() {
        this.baseURL = API_BASE;
    }

    async request(path, options = {}) {
        const { method = 'GET', body = null, headers = {} } = options;
        
        const isFormData = (typeof FormData !== 'undefined') && body instanceof FormData;
        const baseHeaders = isFormData ? {} : { 'Content-Type': 'application/json' };
        const config = {
            method,
            headers: {
                ...baseHeaders,
                ...headers
            },
            credentials: 'include'
        };

        if (body) {
            config.body = isFormData ? body : JSON.stringify(body);
        }

        try {
            const response = await fetch(`${this.baseURL}${path}`, config);
            const data = await response.json().catch(() => ({}));
            
            if (!response.ok) {
                throw new Error(data.error || data.message || 'Request failed');
            }
            
            return { data, status: response.status };
        } catch (error) {
            console.error('API Request failed:', error);
            throw error;
        }
    }

    async get(path, options = {}) {
        return this.request(path, { method: 'GET', ...options });
    }

    async post(path, body, options = {}) {
        return this.request(path, { method: 'POST', body, ...options });
    }

    async put(path, body, options = {}) {
        return this.request(path, { method: 'PUT', body, ...options });
    }

    async delete(path, body, options = {}) {
        return this.request(path, { method: 'DELETE', body, ...options });
    }
}

window.ResQApi = {
    login: (email, password, role, options) => apiRequest('/auth/login', { method: 'POST', body: { email, password, role } }, options),
    reportCase: (formData, options) => apiRequest('/cases', { method: 'POST', body: formData, isForm: true }, options),
    registerNGO: (payload, options) => apiRequest('/register/ngo', { method: 'POST', body: payload }, options),
    registerVolunteer: (payload, options) => apiRequest('/register/volunteer', { method: 'POST', body: payload }, options),
    listHospitals: (options) => apiRequest('/hospitals', {}, options),
    addHospital: (payload, token, options) => apiRequest('/hospitals', { method: 'POST', body: payload, token }, options),
    createDonation: (payload, options) => apiRequest('/donations', { method: 'POST', body: payload }, options),
};
