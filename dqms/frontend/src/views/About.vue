<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-50 to-blue-100 overflow-hidden">
    <div class="container mx-auto px-6 py-16">
      <section class="text-center hero-section">
        <h1 class="text-4xl md:text-5xl font-extrabold text-gray-800 mb-4">
          Redefining the Hospital Waiting Room
        </h1>
        <p class="text-lg text-gray-600 max-w-3xl mx-auto">
          At <span class="font-semibold text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-teal-500">Q-Less</span>, our mission is to eliminate the stress and uncertainty of hospital queues. We leverage technology to create a seamless, efficient, and patient-centric healthcare experience.
        </p>
      </section>

      <section class="mt-20">
        <h2 class="text-3xl font-bold text-center text-gray-800 mb-12">How We Help</h2>
        <div class="grid md:grid-cols-2 gap-8 max-w-4xl mx-auto">
          <div class="feature-card bg-white/60 backdrop-blur-lg p-8 rounded-2xl shadow-lg border border-gray-200/80">
            <div class="mb-4">
              <span class="text-4xl">❤️</span>
            </div>
            <h3 class="text-2xl font-bold text-blue-800 mb-3">For Patients</h3>
            <p class="text-gray-700">
              Book appointments from anywhere, receive real-time updates on your token status, and know exactly when it's your turn. Spend less time waiting and more time on what matters.
            </p>
          </div>
          <div class="feature-card bg-white/60 backdrop-blur-lg p-8 rounded-2xl shadow-lg border border-gray-200/80" style="animation-delay: 200ms;">
            <div class="mb-4">
              <span class="text-4xl">🏥</span>
            </div>
            <h3 class="text-2xl font-bold text-teal-800 mb-3">For Hospitals</h3>
            <p class="text-gray-700">
              Automate your queue management, reduce administrative workload, and improve patient flow. Our platform provides the tools to enhance operational efficiency and patient satisfaction.
            </p>
          </div>
        </div>
      </section>

      <section class="mt-20 text-center max-w-3xl mx-auto vision-section">
         <h2 class="text-3xl font-bold text-center text-gray-800 mb-6">Our Vision</h2>
         <p class="text-lg text-gray-600">
           We envision a future where technology bridges the gap between healthcare providers and patients, creating an ecosystem built on transparency, efficiency, and compassion. A future where every patient feels valued and every hospital operates at its best.
         </p>
      </section>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AboutUs'
}
</script>

<style scoped>
@keyframes fadeInDown {
  from { opacity: 0; transform: translateY(-30px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(40px); }
  to { opacity: 1; transform: translateY(0); }
}

.hero-section {
  animation: fadeInDown 1s ease-out forwards;
}

.feature-card, .vision-section {
  opacity: 0;
  animation: fadeInUp 0.8s ease-out forwards;
}

.vision-section {
  animation-delay: 400ms;
}
</style>
