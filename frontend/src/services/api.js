import axios from 'axios';

// Use environment variable for production, fallback to localhost for development
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const api = axios.create({
    baseURL: API_BASE_URL,
    timeout: 60000, // 60 seconds for slow connections
    headers: {
        'Content-Type': 'application/json',
    },
});

// States
export const statesService = {
    list: async () => {
        const response = await api.get('/states');
        return response.data;
    },
    get: async (id) => {
        const response = await api.get(`/states/${id}`);
        return response.data;
    },
};

// Jurisdictions
export const jurisdictionsService = {
    getByState: async (stateId) => {
        const response = await api.get(`/states/${stateId}`);
        return response.data.jurisdictions || [];
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
        let url = `/dashboard/latest?state_id=${stateId}`;
        if (jurisdictionId) {
            url += `&jurisdiction_id=${jurisdictionId}`;
        }
        const response = await api.get(url);
        return response.data;
    },
    compare: async (id1, id2) => {
        const response = await api.get(`/dashboard/compare?assessment_id_1=${id1}&assessment_id_2=${id2}`);
        return response.data;
    },
    getHistory: async (stateId, jurisdictionId = null, limit = 10) => {
        let url = `/dashboard/history?state_id=${stateId}&limit=${limit}`;
        if (jurisdictionId) {
            url += `&jurisdiction_id=${jurisdictionId}`;
        }
        const response = await api.get(url);
        return response.data;
    },
};

// Reports
export const reportsService = {
    downloadHtml: async (assessmentId) => {
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

// For backward compatibility
export const authService = {
    login: async () => ({ user: { name: 'Administrador', role: 'admin' } }),
    getMe: async () => ({ name: 'Administrador', role: 'admin' }),
};

export const usersService = {
    list: async () => [],
    create: async () => ({}),
    update: async () => ({}),
    delete: async () => { },
};

export default api;
