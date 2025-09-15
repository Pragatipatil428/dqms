import axios from 'axios'
import { useAuthStore } from './store/auth'

const api = axios.create({
    baseURL: 'http://127.0.0.1:5000/api', // backend URL
    headers: { 'Content-Type': 'application/json' }
})

// Add request interceptor to include token
api.interceptors.request.use(
    config => {
        const authStore = useAuthStore()
        if (authStore.token) {
            config.headers.Authorization = `Bearer ${authStore.token}`
        }
        return config
    },
    error => Promise.reject(error)
)

// Add response interceptor to handle token expiry
api.interceptors.response.use(
    response => response,
    error => {
        if (error.response && error.response.status === 401) {
            const authStore = useAuthStore()
            authStore.logout()
            // Optionally redirect to login
        }
        return Promise.reject(error)
    }
)

export default api
