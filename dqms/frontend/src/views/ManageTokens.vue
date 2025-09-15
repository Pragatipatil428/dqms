<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-50 to-teal-100 p-4 sm:p-6 lg:p-8">
    <div class="container mx-auto">
      <h1 class="text-4xl font-extrabold text-center mb-10 text-gray-800">🛠 Manage Tokens</h1>

      <div v-if="uncompletedTokens.length > 0" class="mb-10">
        <h2 class="text-2xl font-bold mb-4 text-teal-800">Upcoming Tokens ({{ uncompletedTokens.length }})</h2>
        <div class="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
          <transition-group name="list">
            <div
              v-for="token in uncompletedTokens"
              :key="token.token_number"
              class="flex flex-col bg-white/80 backdrop-blur-xl rounded-2xl shadow-lg transition-all duration-300 hover:shadow-xl hover:scale-105"
            >
              <div class="p-5 flex-grow">
                <span class="px-3 py-1 text-xs font-semibold rounded-full capitalize" :class="token.slot_type === 'normal' ? 'bg-teal-100 text-teal-800' : 'bg-blue-100 text-blue-800'">
                  {{ token.slot_type }}
                </span>
                <h3 class="text-2xl font-bold text-gray-800 mt-2">Token #{{ token.token_number }}</h3>
                <p class="text-gray-600 font-medium">{{ token.patient_name }}</p>
                <p class="text-sm text-gray-500 mt-1">Time: {{ token.time_slot }}</p>
              </div>
              <div class="p-4 bg-gray-50/50 rounded-b-2xl">
                <button
                  @click="updateStatus(token.token_number, 'completed')"
                  class="w-full bg-green-500 text-white px-4 py-2 rounded-lg font-semibold hover:bg-green-600 transition"
                >
                  Mark as Completed
                </button>
              </div>
            </div>
          </transition-group>
        </div>
      </div>
      
       <div v-if="completedTokens.length > 0" class="mt-12">
        <h2 class="text-2xl font-bold mb-4 text-gray-600">Completed Tokens ({{ completedTokens.length }})</h2>
        <div class="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
           <transition-group name="list-completed">
            <div
              v-for="token in completedTokens"
              :key="token.token_number"
              class="bg-green-100/60 backdrop-blur-xl rounded-2xl shadow-md p-5 opacity-80"
            >
              <h3 class="text-xl font-bold text-green-900">Token #{{ token.token_number }}</h3>
              <p class="text-green-800 font-medium">{{ token.patient_name }}</p>
              <p class="text-sm text-green-700 mt-1">Time: {{ token.time_slot }} ✅</p>
            </div>
          </transition-group>
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
import { useAuthStore } from "../store/auth"

export default {
  data() {
    return {
      tokens: []
    }
  },
  setup() {
    const authStore = useAuthStore()
    return { authStore }
  },
  computed: {
    uncompletedTokens() {
        return this.tokens.filter(token => token.status !== 'completed').sort((a, b) => a.token_number - b.token_number)
    },
    completedTokens() {
      return this.tokens.filter(token => token.status === 'completed').sort((a, b) => b.token_number - a.token_number)
    }
  },
  async created() {
    await this.fetchTokens()
  },
  methods: {
    async fetchTokens() {
      try {
        const res = await api.get(`/hospitals/token-requests/${this.authStore.user.id}`)
        this.tokens = res.data
      } catch (err) {
        console.error("Error fetching tokens", err)
      }
    },
    async updateStatus(tokenNumber, status) {
      try {
        // Optimistically update UI
        const tokenIndex = this.tokens.findIndex(t => t.token_number === tokenNumber);
        if (tokenIndex !== -1) {
          this.tokens[tokenIndex].status = status;
        }

        await api.post(`/hospitals/update-token-status`, {
          hospital_id: this.authStore.user.id,
          token_number: tokenNumber,
          status: status
        })
      } catch (err) {
        console.error("Error updating token", err)
        // Revert UI on error
        await this.fetchTokens();
      }
    }
  }
}
</script>

<style scoped>
/* Upcoming list transitions */
.list-move,
.list-enter-active,
.list-leave-active {
  transition: all 0.5s cubic-bezier(0.55, 0, 0.1, 1);
}
.list-enter-from,
.list-leave-to {
  opacity: 0;
  transform: scale(0.5);
}
.list-leave-active {
  position: absolute;
}

/* Completed list transitions */
.list-completed-enter-active {
  transition: all 0.5s ease;
  transition-delay: 0.5s; /* Delay enter to allow leave animation to finish */
}
.list-completed-enter-from {
  opacity: 0;
  transform: translateY(30px);
}
</style>