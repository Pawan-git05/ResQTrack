/**
 * Data Dashboard JavaScript for ResQTrack
 * Handles data import, export, visualization, and management
 */

class DataDashboard {
    constructor() {
        this.api = new API();
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
        // Location search
        document.getElementById('location-search').addEventListener('input', (e) => {
            this.searchEmergencyServices(e.target.value);
        });

        // Service type filter
        document.getElementById('service-type-filter').addEventListener('change', (e) => {
            this.filterEmergencyServices(e.target.value);
        });
    }

    async loadStatistics() {
        try {
            const response = await this.api.get('/data/statistics');
            const data = response.data;
            
            // Update count cards
            document.getElementById('ngos-count').textContent = data.statistics.ngos.total;
            document.getElementById('volunteers-count').textContent = data.statistics.volunteers.total;
            document.getElementById('hospitals-count').textContent = data.statistics.hospitals.total;
            
            const emergencyServicesCount = 
                data.statistics.police_stations.total + 
                data.statistics.blood_banks.total + 
                data.statistics.fire_stations.total;
            document.getElementById('emergency-services-count').textContent = emergencyServicesCount;

            // Create charts
            this.createServiceChart(data.statistics);
            this.createLocationChart(data.location_distribution);

        } catch (error) {
            console.error('Error loading statistics:', error);
            this.showToast('Error loading statistics', 'error');
        }
    }

    async ensureAdminAuth() {
        if (this.adminToken) return;
        const res = await fetch(`${this.api.baseURL}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include',
            body: JSON.stringify({
                email: 'admin@resqtrack.com',
                password: 'admin123',
                role: 'ADMIN'
            })
        });
        const data = await res.json().catch(() => ({}));
        if (!res.ok || !data.access_token) {
            throw new Error(data.error || 'Admin authentication failed');
        }
        this.adminToken = data.access_token;
    }

    createServiceChart(statistics) {
        const ctx = document.getElementById('serviceChart').getContext('2d');
        
        const data = {
            labels: ['NGOs', 'Volunteers', 'Hospitals', 'Police Stations', 'Blood Banks', 'Fire Stations'],
            datasets: [{
                data: [
                    statistics.ngos.total,
                    statistics.volunteers.total,
                    statistics.hospitals.total,
                    statistics.police_stations.total,
                    statistics.blood_banks.total,
                    statistics.fire_stations.total
                ],
                backgroundColor: [
                    '#007bff',
                    '#28a745',
                    '#17a2b8',
                    '#dc3545',
                    '#343a40',
                    '#6c757d'
                ]
            }]
        };

        this.charts.service = new Chart(ctx, {
            type: 'doughnut',
            data: data,
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
    }

    createLocationChart(locationDistribution) {
        const ctx = document.getElementById('locationChart').getContext('2d');
        
        // Get top 10 locations across all services
        const allLocations = {};
        
        Object.values(locationDistribution).forEach(service => {
            Object.entries(service).forEach(([location, count]) => {
                allLocations[location] = (allLocations[location] || 0) + count;
            });
        });

        const topLocations = Object.entries(allLocations)
            .sort(([,a], [,b]) => b - a)
            .slice(0, 10);

        const data = {
            labels: topLocations.map(([location]) => location),
            datasets: [{
                label: 'Total Services',
                data: topLocations.map(([, count]) => count),
                backgroundColor: '#17a2b8',
                borderColor: '#17a2b8',
                borderWidth: 1
            }]
        };

        this.charts.location = new Chart(ctx, {
            type: 'bar',
            data: data,
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    }
                }
            }
        });
    }

    async importData(type) {
        const fileInput = document.getElementById(`${type.replace('-', '_')}-file`);
        const file = fileInput.files[0];

        if (!file) {
            this.showToast('Please select a file first', 'warning');
            return;
        }

        if (!file.name.endsWith('.csv')) {
            this.showToast('Please select a CSV file', 'error');
            return;
        }

        this.showLoading(true);

        try {
            // Ensure we are authenticated for protected import endpoints
            await this.ensureAdminAuth();
            const formData = new FormData();
            formData.append('file', file);

            const response = await this.api.post(`/data/import/${type}`, formData, {
                headers: {
                    // Let the browser set proper multipart boundary
                    'Authorization': `Bearer ${this.adminToken}`
                }
            });

            this.showImportResults(response.data.stats, type);
            this.loadStatistics(); // Refresh statistics
            this.loadEmergencyServices(); // Refresh emergency services

            fileInput.value = ''; // Clear file input

        } catch (error) {
            console.error('Import error:', error);
            this.showToast('Import failed: ' + (error.response?.data?.error || error.message), 'error');
        } finally {
            this.showLoading(false);
        }
    }

    showImportResults(stats, type) {
        const resultsDiv = document.getElementById('import-results');
        const statsDiv = document.getElementById('import-stats');

        const successColor = stats.successful > 0 ? 'text-success' : '';
        const errorColor = stats.failed > 0 ? 'text-danger' : '';
        const warningColor = stats.skipped > 0 ? 'text-warning' : '';

        statsDiv.innerHTML = `
            <div class="row">
                <div class="col-md-3">
                    <div class="text-center">
                        <h4 class="${successColor}">${stats.successful}</h4>
                        <p class="mb-0">Successful</p>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="text-center">
                        <h4 class="${errorColor}">${stats.failed}</h4>
                        <p class="mb-0">Failed</p>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="text-center">
                        <h4 class="${warningColor}">${stats.skipped}</h4>
                        <p class="mb-0">Skipped</p>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="text-center">
                        <h4 class="text-info">${stats.successful + stats.failed + stats.skipped}</h4>
                        <p class="mb-0">Total</p>
                    </div>
                </div>
            </div>
            ${stats.errors.length > 0 ? `
                <div class="mt-3">
                    <h6>Errors:</h6>
                    <div class="alert alert-warning">
                        <ul class="mb-0">
                            ${stats.errors.slice(0, 5).map(error => `<li>${error}</li>`).join('')}
                            ${stats.errors.length > 5 ? `<li>... and ${stats.errors.length - 5} more errors</li>` : ''}
                        </ul>
                    </div>
                </div>
            ` : ''}
        `;

        resultsDiv.style.display = 'block';
        this.showToast(`Import completed for ${type}: ${stats.successful} successful`, 'success');
    }

    async loadEmergencyServices() {
        try {
            const response = await this.api.get('/data/emergency-contacts');
            this.displayEmergencyServices(response.data.contacts);
        } catch (error) {
            console.error('Error loading emergency services:', error);
        }
    }

    displayEmergencyServices(services) {
        const container = document.getElementById('emergency-services-list');
        
        if (services.length === 0) {
            container.innerHTML = '<p class="text-muted">No emergency services found.</p>';
            return;
        }

        const servicesHtml = services.map(service => `
            <div class="card mb-2">
                <div class="card-body">
                    <div class="row">
                        <div class="col-md-8">
                            <h6 class="card-title">${service.name}</h6>
                            <p class="card-text">
                                <strong>Type:</strong> ${service.service_type}<br>
                                <strong>Phone:</strong> ${service.phone}<br>
                                ${service.location ? `<strong>Location:</strong> ${service.location}<br>` : ''}
                                ${service.description ? `<strong>Description:</strong> ${service.description}` : ''}
                            </p>
                        </div>
                        <div class="col-md-4 text-end">
                            <span class="badge ${service.is_24x7 ? 'bg-success' : 'bg-secondary'}">
                                ${service.is_24x7 ? '24/7' : 'Limited Hours'}
                            </span>
                            <br>
                            <span class="badge bg-${this.getPriorityColor(service.priority_level)}">
                                Priority ${service.priority_level}
                            </span>
                            <br>
                            <button class="btn btn-outline-danger btn-sm mt-2" onclick="deleteEntry('emergency_contact', ${service.id})">
                                <i class="fas fa-trash me-1"></i>Delete
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `).join('');

        container.innerHTML = servicesHtml;
    }

    getPriorityColor(priority) {
        switch (priority) {
            case 1: return 'danger';
            case 2: return 'warning';
            case 3: return 'info';
            default: return 'secondary';
        }
    }

    searchEmergencyServices(location) {
        // This would typically make an API call to search by location
        // For now, we'll filter the displayed services
        const services = document.querySelectorAll('#emergency-services-list .card');
        services.forEach(service => {
            const text = service.textContent.toLowerCase();
            if (text.includes(location.toLowerCase())) {
                service.style.display = 'block';
            } else {
                service.style.display = 'none';
            }
        });
    }

    filterEmergencyServices(serviceType) {
        // This would typically make an API call to filter by service type
        // For now, we'll filter the displayed services
        const services = document.querySelectorAll('#emergency-services-list .card');
        services.forEach(service => {
            if (!serviceType || service.textContent.toLowerCase().includes(serviceType.toLowerCase())) {
                service.style.display = 'block';
            } else {
                service.style.display = 'none';
            }
        });
    }

    async exportData(type) {
        try {
            const response = await this.api.get(`/data/export/${type}`);
            
            // Create download link
            const link = document.createElement('a');
            link.href = response.data.download_url;
            link.download = `${type}_export.csv`;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);

            this.showToast(`Export completed for ${type}`, 'success');

        } catch (error) {
            console.error('Export error:', error);
            this.showToast('Export failed: ' + (error.response?.data?.error || error.message), 'error');
        }
    }

    async exportAllData() {
        const types = ['ngos', 'volunteers', 'hospitals'];
        
        for (const type of types) {
            try {
                await this.exportData(type);
                // Small delay between downloads
                await new Promise(resolve => setTimeout(resolve, 500));
            } catch (error) {
                console.error(`Export error for ${type}:`, error);
            }
        }

        this.showToast('All exports completed', 'success');
    }

    showLoading(show) {
        const overlay = document.getElementById('loading-overlay');
        overlay.style.display = show ? 'flex' : 'none';
    }

    showToast(message, type = 'info') {
        const toast = document.getElementById('toast');
        const toastMessage = document.getElementById('toast-message');
        
        toastMessage.textContent = message;
        
        // Update toast header icon based on type
        const headerIcon = toast.querySelector('.toast-header i');
        headerIcon.className = `fas ${
            type === 'success' ? 'fa-check-circle text-success' :
            type === 'error' ? 'fa-exclamation-circle text-danger' :
            type === 'warning' ? 'fa-exclamation-triangle text-warning' :
            'fa-info-circle text-primary'
        } me-2`;

        const bsToast = new bootstrap.Toast(toast);
        bsToast.show();
    }

    async loadUploadedFiles() {
        try {
            const response = await this.api.get('/data/uploaded-files');
            this.displayUploadedFiles(response.data.files);
        } catch (error) {
            console.error('Error loading uploaded files:', error);
            document.getElementById('uploaded-files-list').innerHTML = '<div class="text-muted">No files found</div>';
        }
    }

    displayUploadedFiles(files) {
        const container = document.getElementById('uploaded-files-list');
        
        if (files.length === 0) {
            container.innerHTML = '<div class="text-muted">No uploaded files found</div>';
            return;
        }

        const filesHtml = files.map(file => `
            <div class="d-flex justify-content-between align-items-center mb-2 p-2 border rounded">
                <div>
                    <strong>${file.name}</strong><br>
                    <small class="text-muted">
                        Size: ${this.formatFileSize(file.size)} | 
                        Modified: ${new Date(file.modified * 1000).toLocaleDateString()}
                    </small>
                </div>
                <button class="btn btn-outline-danger btn-sm" onclick="deleteFile('${file.name}')">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
        `).join('');

        container.innerHTML = filesHtml;
    }

    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    async deleteFile(filename) {
        if (!confirm(`Are you sure you want to delete ${filename}?`)) {
            return;
        }

        try {
            await this.api.delete('/data/delete-file', { filename });
            this.showToast(`File ${filename} deleted successfully`, 'success');
            this.loadUploadedFiles(); // Refresh the list
        } catch (error) {
            console.error('Error deleting file:', error);
            this.showToast('Failed to delete file: ' + (error.response?.data?.error || error.message), 'error');
        }
    }

    async clearData(serviceType) {
        if (!confirm(`Are you sure you want to clear all ${serviceType} data? This action cannot be undone.`)) {
            return;
        }

        try {
            await this.api.delete(`/data/clear-data/${serviceType}`);
            this.showToast(`All ${serviceType} data cleared successfully`, 'success');
            this.loadStatistics(); // Refresh statistics
            this.loadEmergencyServices(); // Refresh emergency services
        } catch (error) {
            console.error('Error clearing data:', error);
            this.showToast('Failed to clear data: ' + (error.response?.data?.error || error.message), 'error');
        }
    }

    async deleteEntry(serviceType, entryId) {
        if (!confirm(`Are you sure you want to delete this ${serviceType} entry?`)) {
            return;
        }

        try {
            await this.api.delete(`/data/delete-entry/${serviceType}/${entryId}`);
            this.showToast(`${serviceType} entry deleted successfully`, 'success');
            this.loadStatistics(); // Refresh statistics
            this.loadEmergencyServices(); // Refresh emergency services
        } catch (error) {
            console.error('Error deleting entry:', error);
            this.showToast('Failed to delete entry: ' + (error.response?.data?.error || error.message), 'error');
        }
    }
}

// Global functions for HTML onclick handlers
function importData(type) {
    dataDashboard.importData(type);
}

function exportData(type) {
    dataDashboard.exportData(type);
}

function exportAllData() {
    dataDashboard.exportAllData();
}

function deleteFile(filename) {
    dataDashboard.deleteFile(filename);
}

function clearData(serviceType) {
    dataDashboard.clearData(serviceType);
}

function deleteEntry(serviceType, entryId) {
    dataDashboard.deleteEntry(serviceType, entryId);
}

// Initialize dashboard when DOM is loaded
let dataDashboard;
document.addEventListener('DOMContentLoaded', function() {
    dataDashboard = new DataDashboard();
});
