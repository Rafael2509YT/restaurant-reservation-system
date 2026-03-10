import api from './apiClient';

export default {
  // Public
  create(data) {
    return api.post('/reservations/', data);
  },
  cancel(id, uniqueCode) {
    return api.delete(`/reservations/${id}/cancel/`, {
      data: { unique_code: uniqueCode }
    });
  },

  // Admin
  fetchAll(date, status) {
    const params = new URLSearchParams();
    if (date) params.append('date', date);
    if (status) params.append('status', status);
    return api.get(`/admin/reservations/${params.toString() ? '?' + params.toString() : ''}`);
  },
  adminCancel(id) {
    return api.delete(`/admin/reservations/${id}/cancel/`);
  },
  fetchMetrics(date) {
    let url = '/admin/metrics/';
    if (date) url += `?date=${date}`;
    return api.get(url);
  },
  fetchTables() {
    return api.get('/admin/tables/');
  },
  createTable(data) {
    return api.post('/admin/tables/', data);
  },
  updateTable(id, data) {
    return api.put(`/admin/tables/${id}/`, data);
  },
  deleteTable(id) {
    return api.delete(`/admin/tables/${id}/`);
  },
  fetchConfig() {
    return api.get('/admin/config/');
  },
  updateConfig(data) {
    return api.put('/admin/config/', data);
  }
};