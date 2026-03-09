import { defineStore } from 'pinia'
import api from '../api/apiClient'


export const useReservationStore = defineStore('reservation', {
  state: () => ({
    availability: [],
    adminReservations: [],
    tables: [],
    config: null,
    noCapacity: false,
    noDate: false,
    loading: false,
    error: null
  }),
  actions: {
    async fetchAvailability(date, partySize) {
      this.loading = true;
      this.error = null;
      this.noCapacity = false;
      this.noDate = false;
      try {
        let url = `/availability/?date=${date}`;
        if (partySize) url += `&party_size=${partySize}`;
        const response = await api.get(url);
        this.availability = response.data;

        // Si vino vacío y había party_size, verificamos si el problema es capacidad o fecha
        if (this.availability.length === 0 && partySize) {
          const fallback = await api.get(`/availability/?date=${date}`);
          if (fallback.data.length > 0) {
            this.noCapacity = true;  // Hay mesas pero ninguna aguanta ese party_size
          } else {
            this.noDate = true;      // No hay disponibilidad para esa fecha en general
          }
        } else if (this.availability.length === 0) {
          this.noDate = true;
        }
      } catch (err) {
        this.error = "Failed to load availability.";
      } finally {
        this.loading = false;
      }
    },
    async createReservation(reservationData) {
      this.loading = true;
      this.error = null;
      try {
        // Note: The instruction uses API_URL and axios directly.
        // If you want to keep using the 'api' client, you'd adjust this.
        // For now, I'm following the instruction's code snippet, but using 'api' client.
        const response = await api.post('/reservations/', reservationData); // Changed from axios.post to api.post
        return response.data; // Now returns the data containing unique_code
      } catch (err) {
        const msg = err.response?.data?.error;
        this.error = msg ? (typeof msg === 'string' ? msg : JSON.stringify(msg)) : "Failed to create reservation.";
        throw err;
      } finally {
        this.loading = false;
      }
    },
    
    async cancelReservation(id, uniqueCode) {
      this.loading = true;
      this.error = null;
      try {
        // Note: The instruction uses API_URL and axios directly.
        // If you want to keep using the 'api' client, you'd adjust this.
        // For now, I'm following the instruction's code snippet, but using 'api' client.
        await api.delete(`/reservations/${id}/cancel/`, { // Changed from axios.delete to api.delete
          data: { unique_code: uniqueCode }
        });
      } catch (err) {
        this.error = err.response?.data?.error || "Failed to cancel reservation.";
        throw err;
      } finally {
        this.loading = false;
      }
    },
    async fetchAdminReservations(date, status) {
      this.loading = true; this.error = null;
      try {
        let url = '/admin/reservations/';
        const params = new URLSearchParams();
        if (date) params.append('date', date);
        if (status) params.append('status', status);
        if (params.toString()) {
            url += '?' + params.toString();
        }
        const response = await api.get(url);
        this.adminReservations = response.data;
      } catch (err) {
        this.error = "Failed to load admin reservations.";
      } finally {
        this.loading = false;
      }
    },
    async fetchMetrics(date) {
        this.loading = true; this.error = null;
        try {
            let url = '/admin/metrics/';
            if (date) url += `?date=${date}`;
            const response = await api.get(url);
            return response.data;
        } catch (err) {
            this.error = "Failed to load metrics.";
            return null;
        } finally {
            this.loading = false;
        }
    },
    async adminCancelReservation(id) {
        this.loading = true; this.error = null;
        try {
            await api.delete(`/admin/reservations/${id}/cancel/`);
        } catch (err) {
            this.error = err.response?.data?.error || "Failed to cancel reservation.";
            throw err;
        } finally {
            this.loading = false;
        }
    },
    async fetchTables() {
        this.loading = true; this.error = null;
        try {
            const response = await api.get('/admin/tables/');
            this.tables = response.data;
        } catch (err) {
            this.error = "Failed to load tables.";
        } finally {
            this.loading = false;
        }
    },
    async createTable(data) {
        this.loading = true; this.error = null;
        try {
            await api.post('/admin/tables/', data);
            await this.fetchTables();
        } catch (err) {
            this.error = err.response?.data?.error || "Failed to create table.";
            throw err;
        } finally {
            this.loading = false;
        }
    },
    async deleteTable(id) {
        this.loading = true; this.error = null;
        try {
            await api.delete(`/admin/tables/${id}/`);
            await this.fetchTables();
        } catch (err) {
            this.error = err.response?.data?.error || "Failed to delete table.";
            throw err;
        } finally {
            this.loading = false;
        }
    },
    async fetchConfig() {
        this.loading = true; this.error = null;
        try {
            const response = await api.get('/admin/config/');
            this.config = response.data;
        } catch (err) {
            this.error = "Failed to load config.";
        } finally {
            this.loading = false;
        }
    },
    async updateConfig(data) {
        this.loading = true; this.error = null;
        try {
            const response = await api.put('/admin/config/', data);
            this.config = response.data;
        } catch (err) {
            this.error = err.response?.data?.error || "Failed to update config.";
            throw err;
        } finally {
            this.loading = false;
        }
    },
    async toggleTableStatus(table) {
        return this.updateTable(table.id, { is_active: !table.is_active });
    },
    async updateTable(id, data) {
        this.loading = true; this.error = null;
        try {
            const response = await api.put(`/admin/tables/${id}/`, data);
            // Update the table in the local list
            const index = this.tables.findIndex(t => t.id === id);
            if (index !== -1) {
                this.tables[index] = response.data;
            }
            return response.data;
        } catch (err) {
            this.error = err.response?.data?.error || "Failed to update table.";
            throw err;
        } finally {
            this.loading = false;
        }
    }
  }
})
