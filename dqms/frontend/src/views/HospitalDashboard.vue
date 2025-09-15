<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-50 to-teal-100 p-4 sm:p-6 lg:p-8">
    <div class="container mx-auto">
      <h1 class="text-4xl font-extrabold text-center mb-10 text-gray-800">Today's Token Requests</h1>

      <div v-if="normalTokens.length > 0" class="mb-10">
        <h2 class="text-2xl font-bold mb-4 text-teal-800">Normal Queue</h2>
        <div class="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div
            v-for="(token, index) in normalTokens"
            :key="token.token_number"
            class="token-card bg-white/70 backdrop-blur-xl"
            :style="{ animationDelay: `${index * 80}ms` }"
          >
            <div class="border-t-4 border-teal-500 rounded-t-xl"></div>
            <div class="p-5">
              <h3 class="text-xl font-bold text-gray-800">Token #{{ token.token_number }}</h3>
              <p class="text-gray-600 font-medium">{{ token.patient_name }}</p>
              <p class="text-sm text-gray-500 mt-2">Time: {{ token.time_slot }}</p>
            </div>
          </div>
        </div>
      </div>

      <div v-if="scheduledTokens.length > 0" class="mb-10">
        <h2 class="text-2xl font-bold mb-4 text-blue-800">Scheduled Queue</h2>
        <div class="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div
            v-for="(token, index) in scheduledTokens"
            :key="token.token_number"
            class="token-card bg-white/70 backdrop-blur-xl"
            :style="{ animationDelay: `${index * 80}ms` }"
          >
             <div class="border-t-4 border-blue-500 rounded-t-xl"></div>
             <div class="p-5">
              <h3 class="text-xl font-bold text-gray-800">Token #{{ token.token_number }}</h3>
              <p class="text-gray-600 font-medium">{{ token.patient_name }}</p>
              <p class="text-sm text-gray-500 mt-2">Time: {{ token.time_slot }}</p>
            </div>
          </div>
        </div>
      </div>

      <div v-if="tokens.length === 0" class="text-center mt-12 py-16 bg-white/50 rounded-2xl">
        <p class="text-teal-700 text-xl font-semibold">No token requests for today. ✨</p>
      </div>
    </div>
  </div>
</template>

<script>
// Logic remains unchanged
import api from "../axios"
import { useAuthStore } from '../store/auth'

export default {
  data() {
    return { tokens: [] }
  },
  setup() {
    const authStore = useAuthStore()
    return { authStore }
  },
  computed: {
    normalTokens() {
      return this.tokens.filter(token => token.slot_type === 'normal')
    },
    scheduledTokens() {
      return this.tokens.filter(token => token.slot_type === 'scheduled')
    }
  },
  async created() {
    try {
      const res = await api.get(`/hospitals/token-requests/${this.authStore.user.id}`)
      this.tokens = res.data
    } catch (err) {
      console.error("Error fetching tokens", err)
    }
  }
}
</script>

<style scoped>
@keyframes popIn {
  from { opacity: 0; transform: scale(0.8); }
  to { opacity: 1; transform: scale(1); }
}
.token-card {
  @apply rounded-xl shadow-lg transition-all duration-300 hover:shadow-xl hover:-translate-y-1;
  opacity: 0;
  animation: popIn 0.4s ease-out forwards;
}
</style>