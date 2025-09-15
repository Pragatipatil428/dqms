import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: JSON.parse(localStorage.getItem('auth_user')) || null,       // logged-in user object
    role: localStorage.getItem('auth_role') || null,        // "patient" or "hospital"
    token: localStorage.getItem('auth_token') || null,
    tokenExpiry: localStorage.getItem('auth_token_expiry') || null
  }),
  actions: {
    login(user, role, token, expiresInMinutes) {
      this.user = user
      this.role = role
      this.token = token
      const expiryTime = new Date().getTime() + expiresInMinutes * 60 * 1000
      this.tokenExpiry = expiryTime
      localStorage.setItem('auth_user', JSON.stringify(user))
      localStorage.setItem('auth_role', role)
      localStorage.setItem('auth_token', token)
      localStorage.setItem('auth_token_expiry', expiryTime)
    },
    logout() {
      this.user = null
      this.role = null
      this.token = null
      this.tokenExpiry = null
      localStorage.removeItem('auth_user')
      localStorage.removeItem('auth_role')
      localStorage.removeItem('auth_token')
      localStorage.removeItem('auth_token_expiry')
    },
    isLoggedIn() {
      if (!this.token || !this.tokenExpiry) return false
      return new Date().getTime() < this.tokenExpiry
    },
    checkTokenExpiry() {
      if (!this.isLoggedIn()) {
        this.logout()
      }
    }
  }
})
