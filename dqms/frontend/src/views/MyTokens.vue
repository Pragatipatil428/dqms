<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-50 to-indigo-100 p-4 sm:p-6 lg:p-8">
    <div class="container mx-auto">
      <h1 class="text-4xl font-extrabold text-center mb-10 text-gray-800">📋 My Tokens</h1>

      <div v-if="normalTokens.length > 0" class="mb-10">
        <h2 class="text-2xl font-bold mb-4 text-indigo-800">Normal Tokens</h2>
        <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div
            v-for="(token, index) in normalTokens"
            :key="token.token_number"
            class="token-card"
            :style="{ animationDelay: `${index * 100}ms` }"
          >
            <div class="p-6">
              <div class="flex justify-between items-start">
                  <div>
                      <p class="text-sm font-medium text-indigo-500">{{ token.hospital_name }}</p>
                      <h3 class="text-2xl font-bold text-indigo-900">Token #{{ token.token_number }}</h3>
                  </div>
                  <span class="px-3 py-1 text-xs font-semibold rounded-full" :class="isToday(token.date) ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'">{{ formatDate(token.date) }}</span>
              </div>
              <p class="text-indigo-600 my-3">Scheduled Time: <span class="font-bold">{{ token.time_slot }}</span></p>

              <div v-if="isToday(token.date)" class="mt-4 pt-4 border-t border-indigo-100 space-y-2">
                 <p class="text-sm text-green-700 font-semibold" v-if="queueInfo[token.hospital_id] && queueInfo[token.hospital_id].running_token">
                  ▶️ Now Serving: #{{ queueInfo[token.hospital_id].running_token.token_number }}
                </p>
                <p class="text-sm text-blue-700 font-semibold" v-if="tokenPosition[token.token_number]">
                  ⏳ {{ tokenPosition[token.token_number].ahead }} people ahead | Est. Time: ~{{ tokenPosition[token.token_number].estimated_time }}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div v-if="scheduledTokens.length > 0">
        <h2 class="text-2xl font-bold mb-4 text-indigo-800">Scheduled Tokens</h2>
        <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div
                v-for="(token, index) in scheduledTokens"
                :key="token.token_number"
                class="token-card"
                :style="{ animationDelay: `${index * 100}ms` }"
             >
                <div class="p-6">
                    <div class="flex justify-between items-start">
                        <div>
                            <p class="text-sm font-medium text-indigo-500">{{ token.hospital_name }}</p>
                            <h3 class="text-2xl font-bold text-indigo-900">Token #{{ token.token_number }}</h3>
                        </div>
                         <span class="px-3 py-1 text-xs font-semibold rounded-full" :class="isToday(token.date) ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'">{{ formatDate(token.date) }}</span>
                    </div>
                    <p class="text-indigo-600 my-3">Scheduled Time: <span class="font-bold">{{ token.time_slot }}</span></p>
                </div>
            </div>
        </div>
      </div>
      
      <div v-if="tokens.length === 0" class="text-center mt-12">
        <p class="text-indigo-600 text-lg">You haven’t booked any tokens yet.</p>
        <button @click="$router.push('/patient-dashboard')" class="mt-4 bg-indigo-600 text-white font-bold py-3 px-6 rounded-lg hover:bg-indigo-700 transition">Book a Token Now</button>
      </div>
    </div>
  </div>
</template>

<script>
// Logic remains unchanged
import api from "../axios"
import { useAuthStore } from "../store/auth"

export default {
  data() {
    return {
      tokens: [],
      queueInfo: {},
      tokenPosition: {}
    }
  },
  setup() {
    const authStore = useAuthStore()
    return { authStore }
  },
  computed: {
    normalTokens() {
      return this.tokens.filter(token => token.slot_type === 'normal').sort((a, b) => a.token_number - b.token_number)
    },
    scheduledTokens() {
      return this.tokens.filter(token => token.slot_type === 'scheduled').sort((a, b) => a.token_number - b.token_number)
    }
  },
  async created() {
    try {
      const res = await api.get('/patients/my-tokens')
      this.tokens = res.data
      await this.fetchQueueInfo()
    } catch (err) {
      console.error("Error fetching tokens", err)
    }
  },
  methods: {
    isToday(dateStr) {
      const today = new Date().toISOString().split('T')[0]
      return dateStr === today
    },
    formatDate(dateStr) {
      if (this.isToday(dateStr)) return 'Today'
      const date = new Date(dateStr)
      return date.toLocaleDateString('en-GB', { day: 'numeric', month: 'short' })
    },
    async fetchQueueInfo() {
      const uniqueHospitalIds = [...new Set(this.tokens.filter(t => this.isToday(t.date)).map(t => t.hospital_id))]
      for (const hospitalId of uniqueHospitalIds) {
        try {
          const res = await api.get(`/hospitals/current-queue/${hospitalId}`)
          this.queueInfo[hospitalId] = res.data
          this.calculatePositions(hospitalId, res.data)
        } catch (err) {
          console.error("Error fetching queue", err)
        }
      }
    },
    calculatePositions(hospitalId, queueData) {
      const runningToken = queueData.running_token
      const upcoming = queueData.upcoming_tokens
      if (runningToken) {
        const myUpcomingTokens = this.tokens.filter(t => t.hospital_id === hospitalId && upcoming.some(ut => ut.token_number === t.token_number));
        
        myUpcomingTokens.forEach(token => {
          const positionInUpcoming = upcoming.findIndex(ut => ut.token_number === token.token_number);
          if (positionInUpcoming !== -1) {
            const ahead = positionInUpcoming + 1; // +1 because index is 0-based
            const estimatedMinutes = ahead * 10;
            const now = new Date();
            const estimatedDateTime = new Date(now.getTime() + estimatedMinutes * 60000);
            const estimatedTime = estimatedDateTime.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', hour12: true });

            this.tokenPosition[token.token_number] = {
              ahead: ahead,
              estimated_time: estimatedTime
            }
          }
        });
      }
    }
  }
}
</script>

<style scoped>
@keyframes slideInUp {
  from { opacity: 0; transform: translateY(50px); }
  to { opacity: 1; transform: translateY(0); }
}
.token-card {
  @apply bg-white/80 backdrop-blur-lg rounded-2xl shadow-md border border-indigo-100 overflow-hidden transition-all duration-300 hover:shadow-xl hover:-translate-y-1;
  opacity: 0;
  animation: slideInUp 0.5s ease-out forwards;
}
</style>