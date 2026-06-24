import './bootstrap';
import Alpine from 'alpinejs';

window.Alpine = Alpine;
Alpine.start();

window.app = {
  apiBase: window.location.origin,
  auth: {
    getToken: () => localStorage.getItem('access_token'),
    setToken: (token) => localStorage.setItem('access_token', token),
    clearToken: () => localStorage.removeItem('access_token'),
    isAuthenticated: () => !!localStorage.getItem('access_token'),
  },
  toast: (message, type = 'info') => {
    const event = new CustomEvent('app:toast', { detail: { message, type } });
    window.dispatchEvent(event);
  },
  api: async (endpoint, options = {}) => {
    const token = window.app.auth.getToken();
    const headers = {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...(options.headers || {}),
    };
    const response = await fetch(`${window.app.apiBase}${endpoint}`, {
      ...options,
      headers,
    });
    if (response.status === 401) {
      window.app.auth.clearToken();
      window.location.href = '/login';
    }
    return response;
  },
};

console.log('Educational Frontend initialized');