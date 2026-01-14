import axios from 'axios';

// Use direct backend URL to avoid proxy issues
const API_BASE_URL = 'http://localhost:8000/api';

const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Add auth token to requests
api.interceptors.request.use((config) => {
    const token = localStorage.getItem('token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

// Handle auth errors - but not on the login endpoint itself
api.interceptors.response.use(
    (response) => response,
    (error) => {
        // Don't redirect on login failures - let the login page handle it
        const isLoginEndpoint = error.config?.url?.includes('/auth/login');

        if (error.response?.status === 401 && !isLoginEndpoint) {
            localStorage.removeItem('token');
            localStorage.removeItem('user');
            window.location.href = '/login';
        }
        return Promise.reject(error);
    }
);

// Auth
export const authService = {
    login: async (email, password) => {
        const formData = new URLSearchParams();
        formData.append('username', email);
        formData.append('password', password);
        const response = await api.post('/auth/login', formData, {
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        });
        return response.data;
    },
    getMe: async () => {
        const response = await api.get('/auth/me');
        return response.data;
    },
};

// States
export const statesService = {
    list: async () => {
        const response = await api.get('/states');
        return response.data;
    },
    getJurisdictions: async (stateId) => {
        const response = await api.get(`/jurisdictions/by-state/${stateId}`);
        return response.data;
    },
};

// Assessments
export const assessmentsService = {
    list: async (filters = {}) => {
        const params = new URLSearchParams();
        Object.entries(filters).forEach(([key, value]) => {
            if (value) params.append(key, value);
        });
        const response = await api.get(`/assessments?${params}`);
        return response.data;
    },
    get: async (id) => {
        const response = await api.get(`/assessments/${id}`);
        return response.data;
    },
    create: async (data) => {
        const response = await api.post('/assessments', data);
        return response.data;
    },
    update: async (id, data) => {
        const response = await api.put(`/assessments/${id}`, data);
        return response.data;
    },
    delete: async (id) => {
        await api.delete(`/assessments/${id}`);
    },
    getFespItems: async () => {
        const response = await api.get('/assessments/fesp-items/definition');
        return response.data;
    },
};

// Dashboard
export const dashboardService = {
    getSummary: async (assessmentId) => {
        const response = await api.get(`/dashboard/summary/${assessmentId}`);
        return response.data;
    },
    getLatest: async (stateId, jurisdictionId = null) => {
        const params = new URLSearchParams({ state_id: stateId });
        if (jurisdictionId) params.append('jurisdiction_id', jurisdictionId);
        const response = await api.get(`/dashboard/latest?${params}`);
        return response.data;
    },
    compare: async (id1, id2) => {
        const response = await api.get(`/dashboard/compare?assessment_id_1=${id1}&assessment_id_2=${id2}`);
        return response.data;
    },
    getHistory: async (stateId, jurisdictionId = null) => {
        const params = new URLSearchParams({ state_id: stateId });
        if (jurisdictionId) params.append('jurisdiction_id', jurisdictionId);
        const response = await api.get(`/dashboard/history?${params}`);
        return response.data;
    },
};

// Reports
export const reportsService = {
    downloadPdf: async (assessmentId) => {
        const response = await api.get(`/reports/pdf/${assessmentId}`, {
            responseType: 'blob',
        });
        return response.data;
    },
    downloadCsv: async (filters = {}) => {
        const params = new URLSearchParams();
        Object.entries(filters).forEach(([key, value]) => {
            if (value) params.append(key, value);
        });
        const response = await api.get(`/reports/csv?${params}`, {
            responseType: 'blob',
        });
        return response.data;
    },
};

// Users (Admin)
export const usersService = {
    list: async () => {
        const response = await api.get('/users');
        return response.data;
    },
    create: async (data) => {
        const response = await api.post('/users', data);
        return response.data;
    },
    update: async (id, data) => {
        const response = await api.put(`/users/${id}`, data);
        return response.data;
    },
    delete: async (id) => {
        await api.delete(`/users/${id}`);
    },
};

export default api;
