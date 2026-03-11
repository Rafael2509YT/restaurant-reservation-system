import axios from 'axios';

/**
 * [AUDITORÍA - API] Configuración centralizada de Axios.
 * Se crea una instancia única para que todas las peticiones al backend 
 * compartan la misma configuración base, facilitando el mantenimiento.
 */
const apiClient = axios.create({
  /**
   * [AUDITORÍA - DESPLIEGUE] Manejo dinámico de la URL del API.
   * 'import.meta.env.VITE_API_URL' se usa en producción (Vercel).
   * Si no está definida, hace fallback a 'http://localhost:8000/api' para desarrollo.
   */
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api',
  
  // [AUDITORÍA] Definición de headers estándar para intercambio de datos JSON.
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * [AUDITORÍA] Exportación de la instancia para ser consumida por los 
 * servicios específicos (availabilityApi, reservationApi, etc.).
 */
export default apiClient;

