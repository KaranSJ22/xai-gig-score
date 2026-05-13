import { getToken } from './auth';

const BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8001';

export async function apiRequest(endpoint, options = {}) {
  const token = getToken();
  
  const headers = {
    'Content-Type': 'application/json',
    ...options.headers,
  };

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const response = await fetch(`${BASE_URL}${endpoint}`, {
    ...options,
    headers,
  });

  const data = await response.json();

  if (!response.ok) {
    if (response.status === 401) {
      localStorage.removeItem('lender_token');
      window.location.href = '/login';
    }
    throw new Error(data.detail || 'Something went wrong');
  }

  return data;
}
