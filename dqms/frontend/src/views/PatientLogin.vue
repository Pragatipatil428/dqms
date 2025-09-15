<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-50 to-blue-100 p-4">
    <div class="w-full max-w-md bg-white/70 backdrop-blur-xl rounded-2xl shadow-lg p-8 transform transition-all duration-500 hover:shadow-2xl">
      <div class="text-center mb-8">
        <h2 class="text-3xl font-bold text-gray-800">Patient Login</h2>
        <p class="text-gray-500 mt-2">Access your dashboard to manage tokens.</p>
      </div>
      <form @submit.prevent="login" class="space-y-6">
        <div>
          <label for="email" class="block text-sm font-medium text-gray-700">Email</label>
          <input
            id="email"
            type="email"
            v-model="email"
            placeholder="you@example.com"
            class="form-input"
            required
          />
        </div>
        <div>
          <label for="password" class="block text-sm font-medium text-gray-700">Password</label>
          <input
            id="password"
            type="password"
            v-model="password"
            placeholder="••••••••"
            class="form-input"
            required
          />
        </div>
        <button class="w-full bg-blue-600 text-white font-bold py-3 px-4 rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-all duration-300 transform hover:scale-105">
          Secure Login
        </button>
      </form>
      <p v-if="message" class="text-center mt-4 text-red-500 font-medium">{{ message }}</p>
    </div>
  </div>
</template>

<script>
// Logic remains unchanged
import api from '../axios'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../store/auth'

export default {
  data() {
    return {
      email: '',
      password: '',
      message: ''
    }
  },
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    return { router, authStore }
  },
  methods: {
    async login() {
      try {
        const res = await api.post('/auth/patient/login', {
          email: this.email,
          password: this.password
        })
        this.authStore.login(res.data.user, 'patient', res.data.token, 15)
        this.router.push('/patient-dashboard')
      } catch (err) {
        this.message = err.response?.data?.message || 'Login failed'
      }
    }
  }
}
</script>

<style scoped>
.form-input {
  @apply mt-1 block w-full px-4 py-3 bg-gray-50 border border-gray-300 rounded-lg shadow-sm placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm transition-all;
}
</style>