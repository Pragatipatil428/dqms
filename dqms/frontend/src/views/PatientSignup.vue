<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-50 to-blue-100 p-4">
    <div class="w-full max-w-md bg-white/70 backdrop-blur-xl rounded-2xl shadow-lg p-8 transform transition-all duration-500 hover:shadow-2xl">
      <div class="text-center mb-8">
        <h2 class="text-3xl font-bold text-gray-800">Create Patient Account</h2>
        <p class="text-gray-500 mt-2">Join us to streamline your hospital visits.</p>
      </div>
      <form @submit.prevent="signup" class="space-y-6">
        <div>
          <label for="name" class="block text-sm font-medium text-gray-700">Full Name</label>
          <input id="name" type="text" v-model="name" placeholder="John Doe" class="form-input" required />
        </div>
        <div>
          <label for="email" class="block text-sm font-medium text-gray-700">Email</label>
          <input id="email" type="email" v-model="email" placeholder="you@example.com" class="form-input" required />
        </div>
        <div>
          <label for="password" class="block text-sm font-medium text-gray-700">Password</label>
          <input id="password" type="password" v-model="password" placeholder="••••••••" class="form-input" required />
        </div>
        <button class="w-full bg-green-600 text-white font-bold py-3 px-4 rounded-lg hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 transition-all duration-300 transform hover:scale-105">
          Create Account
        </button>
      </form>
      <p v-if="message" class="text-center mt-4 font-medium" :class="message.includes('success') ? 'text-green-600' : 'text-red-500'">{{ message }}</p>
    </div>
  </div>
</template>

<script>
// Logic remains unchanged
import api from '../axios'
import { useRouter } from 'vue-router'

export default {
  data() {
    return {
      name: '',
      email: '',
      password: '',
      message: ''
    }
  },
  setup() {
    const router = useRouter()
    return { router }
  },
  methods: {
    async signup() {
      try {
        const res = await api.post('/auth/patient/signup', {
          name: this.name,
          email: this.email,
          password: this.password
        })
        this.message = res.data.message + " Redirecting to login..."
        setTimeout(() => this.router.push('/patient-login'), 2000);
      } catch (err) {
        this.message = err.response.data.message
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