import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL
  || `http://${window.location.hostname}:8000/api`;

function getSessionId() {
  let sid = localStorage.getItem('zoo_session_id');
  if (!sid) {
    sid = crypto.randomUUID ? crypto.randomUUID() : (
      'xxxx-xxxx-xxxx'.replace(/x/g, () => Math.floor(Math.random() * 16).toString(16))
    );
    localStorage.setItem('zoo_session_id', sid);
  }
  return sid;
}

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: { 'Content-Type': 'application/json' },
});

api.interceptors.request.use(config => {
  config.headers['X-Session-ID'] = getSessionId();
  return config;
});

export const getProducts = (params = {}) => api.get('/products/', { params });
export const getProductBySlug = (slug) => api.get(`/products/${slug}/`);
export const getCategories = () => api.get('/categories/');
export const getBrands = () => api.get('/brands/');
export const getAnimalTypes = () => api.get('/animal-types/');
export const trackProductView = (slug) => api.post(`/products/${slug}/track-view/`);
export const getSimilarProducts = (slug) => api.get(`/products/${slug}/similar/`);
export const getPopularProducts = () => api.get('/products/popular/');
export const getRecommendedProducts = () => api.get('/products/recommended/');

export default api;
