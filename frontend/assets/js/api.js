const API_BASE = '';

async function apiRequest(path, { method = 'GET', body = null, isForm = false, token = null } = {}) {
	const headers = {};
	if (!isForm) headers['Content-Type'] = 'application/json';
	if (token) headers['Authorization'] = `Bearer ${token}`;

	const options = { method, headers, credentials: 'same-origin' };
	if (body) options.body = isForm ? body : JSON.stringify(body);

	const res = await fetch(`${API_BASE}${path}`, options);
	const data = await res.json().catch(() => ({}));
	if (!res.ok) throw new Error(data.error || 'Request failed');
	return data;
}

window.ResQApi = {
	login: (email, password, role) => apiRequest('/auth/login', { method: 'POST', body: { email, password, role } }),
	reportCase: (formData) => apiRequest('/cases', { method: 'POST', body: formData, isForm: true }),
	registerNGO: (payload) => apiRequest('/register/ngo', { method: 'POST', body: payload }),
	registerVolunteer: (payload) => apiRequest('/register/volunteer', { method: 'POST', body: payload }),
	listHospitals: () => apiRequest('/hospitals'),
	addHospital: (payload, token) => apiRequest('/hospitals', { method: 'POST', body: payload, token }),
	createDonation: (payload) => apiRequest('/donations', { method: 'POST', body: payload }),
};
