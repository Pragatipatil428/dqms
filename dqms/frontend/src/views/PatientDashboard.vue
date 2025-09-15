<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-50 to-blue-100 p-4 sm:p-6 lg:p-8">
    <div class="container mx-auto">
      <h1 class="text-4xl font-extrabold text-center mb-10 text-gray-800">Book Your Token</h1>

      <div v-if="normalTokens.length > 0" class="mb-10">
        <h2 class="text-2xl font-bold mb-4 text-blue-800">Your Current Tokens</h2>
        <div class="bg-white/80 backdrop-blur-xl rounded-2xl shadow-lg p-6">
          <div v-for="token in normalTokens" :key="token.token_number" class="mb-4 last:mb-0">
            <h3 class="text-2xl font-bold text-gray-800">Token #{{ token.token_number }}</h3>
            <p class="text-gray-600">{{ token.hospital_name }}</p>
            <p class="text-sm text-green-700 mt-2" v-if="queueInfo[token.hospital_id] && queueInfo[token.hospital_id].running_token">
              Now Serving: #{{ queueInfo[token.hospital_id].running_token.token_number }}
            </p>
            <p class="text-sm text-blue-700" v-if="queueInfo[token.hospital_id] && queueInfo[token.hospital_id].running_token && token.token_number === queueInfo[token.hospital_id].running_token.token_number">
              Your turn now!
            </p>
            <p class="text-sm text-blue-700" v-else-if="tokenPosition[token.token_number]">
              {{ tokenPosition[token.token_number].ahead }} people ahead | Est. Time: {{ tokenPosition[token.token_number].estimated_time }}
            </p>
          </div>
        </div>
      </div>

      <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
        <div
          v-for="(hospital, index) in hospitals"
          :key="hospital.id"
          class="hospital-card bg-white/70 backdrop-blur-xl rounded-2xl shadow-lg p-6 transition-all duration-300 hover:shadow-2xl hover:-translate-y-1"
          :style="{ animationDelay: `${index * 100}ms` }"
        >
          <div class="flex items-center mb-4">
            <div class="bg-blue-100 text-blue-600 rounded-full p-3 mr-4">
               <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" /></svg>
            </div>
            <div>
              <h2 class="text-xl font-bold text-gray-800">{{ hospital.name }}</h2>
              <p class="text-sm text-gray-500">{{ hospital.email }}</p>
            </div>
          </div>

          <div class="mb-4 bg-blue-50 rounded-lg p-1 flex">
            <label class="flex-1 text-center py-2 rounded-md cursor-pointer transition-colors" :class="selectedQueue === 'normal' ? 'bg-blue-500 text-white shadow' : 'text-blue-700'">
              <input type="radio" value="normal" v-model="selectedQueue" class="sr-only"/> Normal
            </label>
            <label class="flex-1 text-center py-2 rounded-md cursor-pointer transition-colors" :class="selectedQueue === 'scheduled' ? 'bg-blue-500 text-white shadow' : 'text-blue-700'">
              <input type="radio" value="scheduled" v-model="selectedQueue" class="sr-only"/> Scheduled
            </label>
          </div>

          <div v-if="selectedQueue === 'scheduled'" class="mb-4 time-input">
            <label class="block mb-2 text-sm font-semibold text-gray-600">Select Date and Time</label>
            <input type="datetime-local" v-model="preferredTime" class="border-gray-300 rounded-lg px-3 py-2 w-full focus:outline-none focus:ring-2 focus:ring-blue-500"/>
          </div>

          <button @click="requestToken(hospital.id, selectedQueue)" class="w-full bg-blue-600 text-white font-bold py-3 rounded-lg hover:bg-blue-700 transition transform hover:scale-105">
            Request Token
          </button>
        </div>
      </div>
      
       <div v-if="message" class="fixed bottom-10 right-10 p-4 rounded-lg shadow-2xl text-white font-semibold animate-bounce" :class="message.startsWith('✅') ? 'bg-green-500' : 'bg-red-500'">
         {{ message }}
       </div>
    </div>
  </div>
</template>

<script>
// Logic remains unchanged
import api from '../axios'
import { useAuthStore } from '../store/auth'

export default {
  data() {
    return {
      hospitals: [],
      preferredTime: "",
      message: "",
      selectedQueue: "normal",
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
      return this.tokens.filter(token => token.slot_type === 'normal' && this.isToday(token.date)).sort((a, b) => a.token_number - b.token_number)
    }
  },
  async created() {
    const res = await api.get('/patients/hospitals')
    this.hospitals = res.data
    await this.fetchTokens()
  },
  methods: {
    async requestToken(hospitalId, type) {
      try {
        const res = await api.post('/patients/request-token', {
          patient_id: this.authStore.user.id,
          hospital_id: hospitalId,
          slot_type: type,
          preferred_time: this.preferredTime
        })
        this.message = `✅ ${res.data.message} | Token: ${res.data.token_number}, Time: ${res.data.time_slot}`
        await this.fetchTokens()
      } catch (err) {
        this.message = `❌ ${err.response?.data?.message || 'Error requesting token'}`
      }
      setTimeout(() => this.message = "", 4000)
    },
    async fetchTokens() {
      try {
        const res = await api.get('/patients/my-tokens')
        this.tokens = res.data
        await this.fetchQueueInfo()
      } catch (err) {
        console.error("Error fetching tokens", err)
      }
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
    },
    isToday(dateStr) {
      const today = new Date().toISOString().split('T')[0]
      return dateStr === today
    }
  }
}
</script>

<style scoped>
@keyframes slideInUp {
  from { opacity: 0; transform: translateY(50px); }
  to { opacity: 1; transform: translateY(0); }
}
.hospital-card {
  opacity: 0;
  animation: slideInUp 0.5s ease-out forwards;
}

@keyframes growIn {
  from { opacity: 0; transform: scale(0.9); }
  to { opacity: 1; transform: scale(1); }
}
.time-input {
  animation: growIn 0.3s ease-out;
}
</style>