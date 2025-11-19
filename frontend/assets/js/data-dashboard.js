/**
 * Data Dashboard JavaScript for ResQTrack
 * Handles data import, export, visualization, and management
 */

class DataDashboard {
    constructor() {
        this.api = new API(); // uses API_BASE by default
        this.charts = {};
        this.adminToken = null;
        this.init();
    }

    init() {
        this.loadStatistics();
        this.setupEventListeners();
        this.loadEmergencyServices();
        this.loadUploadedFiles();
    }

    setupEventListeners() {
        const searchInput = document.getElementById('location-search');
        if (searchInput) {
            searchInput.addEventListener('input', (e) => {
                this.searchEmergencyServices(e.target.value);
            });
        }

        const serviceTypeFilter = document.getElementById('service-type-filter');
        if (serviceTypeFilter) {
            serviceTypeFilter.addEventListener('change', (e) => {
                this.filterEmergencyServices(e.target.value);
            });
        }

        document.querySelectorAll('.import-btn').forEach(button => {
            button.addEventListener('click', () => this.handleImport(button));
        });
    }

    async ensureAdminAuth() {
        if (!this.adminToken) {
            const token = localStorage.getItem('adminToken');
            if (!token) throw new Error("Admin not logged in");
            this.adminToken = token;
        }
    }

    async loadStatistics() {
        try {
            await this.ensureAdminAuth();
            // call '/data/statistics' (API wrapper will prefix /api)
            const response = await this.api.get('/data/statistics', { token: this.adminToken });
            const data = response || {};

            // safe updates (check existence)
            const stats = data.statistics || {};
            document.getElementById('ngos-count').textContent = (stats.ngos?.total ?? 0);
            document.getElementById('volunteers-count').textContent = (stats.volunteers?.total ?? 0);
            document.getElementById('hospitals-count').textContent = (stats.hospitals?.total ?? 0);
            document.getElementById('emergency-count').textContent = (stats.emergency?.total ?? 0);
        } catch (err) {
            console.error('Failed to load statistics:', err);
            if (window.ToastManager) window.ToastManager.error('Error loading statistics');
        }
    }

    async loadEmergencyServices() {
        try {
            const response = await this.api.get('/data/emergency-services');
            const data = response || {};
            this.renderEmergencyServices(data);
        } catch (err) {
            console.error('Error loading emergency services:', err);
        }
    }

    async loadUploadedFiles() {
        try {
            const response = await this.api.get('/data/files');
            const data = response || {};
            this.renderUploadedFiles(data);
        } catch (err) {
            console.error('Error loading uploaded files:', err);
        }
    }

    async handleImport(button) {
        const input = button.parentElement.querySelector('input[type="file"]');
        if (!input || !input.files.length) {
            if (window.ToastManager) window.ToastManager.error('Please choose a file to upload.');
            return;
        }

        const datasetType = button.dataset.type;
        const formData = new FormData();
        formData.append('file', input.files[0]);

        try {
            window.ButtonLoader.setLoading(button, true);
            await this.ensureAdminAuth();

            // Use data import endpoint (API wrapper will prefix /api)
            const response = await this.api.post(`/data/import/${datasetType}`, formData, { isForm: true, token: this.adminToken });

            if (window.ToastManager) window.ToastManager.success(`Successfully imported ${datasetType} data.`);
            console.log('Import response:', response);

            // Refresh after upload
            this.loadStatistics();
            this.loadUploadedFiles();
        } catch (err) {
            console.error('Error importing dataset:', err);
            if (window.ToastManager) window.ToastManager.error(`Failed to import ${datasetType} data.`);
        } finally {
            window.ButtonLoader.setLoading(button, false);
        }
    }

    renderEmergencyServices(data) {
        const container = document.getElementById('emergency-services-list');
        if (!container) return;
        container.innerHTML = '';

        (data.services || []).forEach(service => {
            const card = document.createElement('div');
            card.classList.add('service-card');
            card.innerHTML = `
                <h4>${service.name}</h4>
                <p>Type: ${service.type}</p>
                <p>Location: ${service.location}</p>
            `;
            container.appendChild(card);
        });
    }

    renderUploadedFiles(data) {
        const table = document.getElementById('uploaded-files-table');
        if (!table) return;
        const tbody = table.querySelector('tbody');
        tbody.innerHTML = '';

        (data.files || []).forEach(file => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${file.filename}</td>
                <td>${file.dataset ?? ''}</td>
                <td>${file.uploaded_at ? new Date(file.uploaded_at).toLocaleString() : ''}</td>
                <td><a href="${file.url}" target="_blank">View</a></td>
            `;
            tbody.appendChild(row);
        });
    }

    async searchEmergencyServices(query) {
        try {
            const response = await this.api.get(`/data/emergency-services/search?q=${encodeURIComponent(query)}`);
            this.renderEmergencyServices(response || {});
        } catch (err) {
            console.error('Error searching emergency services:', err);
        }
    }

    async filterEmergencyServices(type) {
        try {
            const response = await this.api.get(`/data/emergency-services?filter=${encodeURIComponent(type)}`);
            this.renderEmergencyServices(response || {});
        } catch (err) {
            console.error('Error filtering emergency services:', err);
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    window.dashboard = new DataDashboard();
});
