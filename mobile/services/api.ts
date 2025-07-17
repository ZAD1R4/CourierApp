import axios from 'axios';
import { getToken } from '../utils/auth';

const apiClient = axios.create({
  baseURL: 'http://localhost:8000',
});

apiClient.interceptors.request.use(async config => {
  const token = await getToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default apiClient;