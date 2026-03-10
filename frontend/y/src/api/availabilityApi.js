import api from './apiClient';

export default {
  getAvailability(date, partySize) {
    let url = `/availability/?date=${date}`;
    if (partySize) url += `&party_size=${partySize}`;
    return api.get(url);
  }
};