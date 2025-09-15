<template>
  <header class="sticky top-0 z-50 w-full bg-white/80 backdrop-blur-lg shadow-sm border-b border-gray-200/80">
    <div class="container mx-auto flex justify-between items-center p-4">
      <h1 class="text-2xl font-extrabold cursor-pointer transition-transform hover:scale-105" @click="$router.push('/')">
        <span class="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-teal-500">Q-Less</span>
      </h1>

      <nav class="flex items-center gap-2 sm:gap-4">
       
        <button
          v-if="authStore.role === 'patient'"
          @click="$router.push('/patient-dashboard')"
          class="nav-link"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" /></svg>
          <span class="hidden sm:inline">Dashboard</span>
        </button>
        <button
          v-if="authStore.role === 'patient'"
          @click="$router.push('/my-tokens')"
          class="nav-link"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 5v2m0 4v2m0 4v2M5 5a2 2 0 00-2 2v3a2 2 0 002 2h14a2 2 0 002-2V7a2 2 0 00-2-2H5z" /></svg>
          <span class="hidden sm:inline">My Tokens</span>
        </button>

        <button
          v-if="authStore.role === 'hospital'"
          @click="$router.push('/hospital-dashboard')"
          class="nav-link"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" /></svg>
          <span class="hidden sm:inline">Dashboard</span>
        </button>
        <button
          v-if="authStore.role === 'hospital'"
          @click="$router.push('/manage-tokens')"
          class="nav-link"
        >
           <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /></svg>
          <span class="hidden sm:inline">Manage Tokens</span>
        </button>
         <button
          @click="$router.push('/about')"
          class="nav-link"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
          <span class="hidden sm:inline">About</span>
        </button>
        <button
          @click="$router.push('/contact')"
          class="nav-link"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 4.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" /></svg>
          <span class="hidden sm:inline">Contact</span>
        </button>

        <button
          v-if="authStore.user"
          @click="logout"
          class="flex items-center gap-2 text-red-600 font-medium px-3 py-2 rounded-lg bg-red-50 hover:bg-red-100 transition-colors duration-300"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" /></svg>
          <span class="hidden sm:inline">Logout</span>
        </button>
      </nav>
    </div>
  </header>
</template>

<script>
// Logic remains unchanged
import { useAuthStore } from "../store/auth"

export default {
  setup() {
    const authStore = useAuthStore()
    return { authStore }
  },
  methods: {
    logout() {
      this.authStore.logout()
      this.$router.push("/")
    }
  }
}
</script>

<style scoped>
.nav-link {
  @apply flex items-center gap-2 text-gray-600 font-medium px-3 py-2 rounded-lg hover:bg-gray-500/10 transition-colors duration-300;
}
</style>