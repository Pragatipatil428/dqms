<template>
  <div class="min-h-screen w-full bg-gradient-to-br from-gray-50 to-blue-100 overflow-hidden">
    <div class="container mx-auto px-6 py-12 text-center">
      <div class="hero-section">
        <h1 class="text-5xl md:text-6xl font-extrabold text-gray-800 mb-4 leading-tight">
          Welcome to <span class="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-teal-500">Q-Less</span>
        </h1>
        <p class="text-lg text-gray-600 max-w-3xl mx-auto mb-10">
          Revolutionizing hospital visits. Say goodbye to long waits and hello to smart, seamless appointment management. Your health, on your schedule.
        </p>
      </div>

      <div class="grid md:grid-cols-2 gap-8 max-w-4xl mx-auto role-cards">
        <div class="card bg-white/60 backdrop-blur-lg p-8 rounded-2xl shadow-lg border border-gray-200/80 transform hover:-translate-y-2 transition-all duration-300">
          <div class="mb-4">
            <span class="text-5xl">❤️</span>
          </div>
          <h2 class="text-2xl font-bold text-blue-800 mb-3">For Patients</h2>
          <p class="text-gray-700 mb-6">Find hospitals, book your spot in the queue, and get real-time updates—all from the comfort of your home.</p>
          <div class="flex flex-col sm:flex-row gap-4 justify-center">
            <button @click="$router.push('/patient-login')" class="btn-primary">
              Patient Login
            </button>
            <button @click="$router.push('/patient-signup')" class="btn-secondary">
              Sign Up
            </button>
          </div>
        </div>

        <div class="card bg-white/60 backdrop-blur-lg p-8 rounded-2xl shadow-lg border border-gray-200/80 transform hover:-translate-y-2 transition-all duration-300">
          <div class="mb-4">
            <span class="text-5xl">🏥</span>
          </div>
          <h2 class="text-2xl font-bold text-teal-800 mb-3">For Hospitals</h2>
          <p class="text-gray-700 mb-6">Streamline your patient flow, manage appointments effortlessly, and reduce administrative overhead.</p>
          <div class="flex flex-col sm:flex-row gap-4 justify-center">
            <button @click="$router.push('/hospital-login')" class="btn-primary-teal">
              Hospital Login
            </button>
            <button @click="$router.push('/hospital-signup')" class="btn-secondary">
              Register
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// Logic remains unchanged
export default {}
</script>

<style scoped>
@keyframes fadeInDown {
  from { opacity: 0; transform: translateY(-20px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(30px); }
  to { opacity: 1; transform: translateY(0); }
}

.hero-section {
  animation: fadeInDown 1s ease-out forwards;
}

.role-cards .card {
  opacity: 0;
  animation: fadeInUp 0.8s ease-out forwards;
}

.role-cards .card:nth-child(2) {
  animation-delay: 0.2s;
}

.btn-primary {
  @apply bg-blue-600 text-white font-semibold px-6 py-3 rounded-lg shadow-md hover:bg-blue-700 transform hover:scale-105 transition-all duration-300;
}

.btn-primary-teal {
  @apply bg-teal-600 text-white font-semibold px-6 py-3 rounded-lg shadow-md hover:bg-teal-700 transform hover:scale-105 transition-all duration-300;
}

.btn-secondary {
  @apply bg-gray-200 text-gray-800 font-semibold px-6 py-3 rounded-lg hover:bg-gray-300 transform hover:scale-105 transition-all duration-300;
}
</style>