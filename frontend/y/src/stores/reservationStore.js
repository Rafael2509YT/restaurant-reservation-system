import { defineStore } from 'pinia'
import availabilityApi from '../api/availabilityApi'
import reservationApi from '../api/reservationApi'


export const useReservationStore = defineStore('reservation', {
  state: () => ({
    availability: [],
    adminReservations: [],
    tables: [],
    config: null,
    noCapacity: false,
    noDate: false,
    loading: false,
    error: null,
    searchDate: null,
    searchPartySize: null
  }),
  actions: {
    async fetchAvailability(date, partySize) {
      this.loading = true;
      this.error = null;
      this.noCapacity = false;
      this.noDate = false;
      try {
        this.searchDate = date;
        this.searchPartySize = partySize;
        const response = await availabilityApi.getAvailability(date, partySize);
        this.availability = response.data;

        // Si vino vacío y había party_size, verificamos si el problema es capacidad o fecha
        if (this.availability.length === 0 && partySize) {
          const fallback = await availabilityApi.getAvailability(date);
          if (fallback.data.length > 0) {
            this.noCapacity = true;
          } else {
            this.noDate = true;
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
        const response = await reservationApi.create(reservationData);
        return response.data;
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
        await reservationApi.cancel(id, uniqueCode);
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
        const response = await reservationApi.fetchAll(date, status);
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
            const response = await reservationApi.fetchMetrics(date);
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
            await reservationApi.adminCancel(id);
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
            const response = await reservationApi.fetchTables();
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
            await reservationApi.createTable(data);
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
            await reservationApi.deleteTable(id);
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
            const response = await reservationApi.fetchConfig();
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
            const response = await reservationApi.updateConfig(data);
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
            const response = await reservationApi.updateTable(id, data);
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
