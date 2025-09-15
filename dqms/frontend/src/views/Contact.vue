<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-50 to-teal-100 p-4 sm:p-6 lg:p-8">
    <div class="container mx-auto">
      <div class="text-center mb-12">
        <h1 class="text-4xl md:text-5xl font-extrabold text-gray-800">Get In Touch</h1>
        <p class="text-lg text-gray-600 mt-4 max-w-2xl mx-auto">
          Have a question or feedback? We'd love to hear from you. Reach out to us, and we'll get back to you shortly.
        </p>
      </div>

      <div class="max-w-5xl mx-auto grid md:grid-cols-2 gap-10 bg-white/60 backdrop-blur-xl rounded-2xl shadow-lg border border-gray-200/80 p-8">
        <div class="contact-form">
          <h2 class="text-2xl font-bold text-gray-800 mb-6">Send us a Message</h2>
          <form @submit.prevent="handleSubmit" class="space-y-5">
            <div>
              <label for="name" class="form-label">Full Name</label>
              <input id="name" type="text" v-model="form.name" placeholder="John Doe" class="form-input" required />
            </div>
            <div>
              <label for="email" class="form-label">Email Address</label>
              <input id="email" type="email" v-model="form.email" placeholder="you@example.com" class="form-input" required />
            </div>
             <div>
              <label for="subject" class="form-label">Subject</label>
              <input id="subject" type="text" v-model="form.subject" placeholder="Feedback and Suggestions" class="form-input" required />
            </div>
            <div>
              <label for="message" class="form-label">Message</label>
              <textarea id="message" v-model="form.message" rows="4" placeholder="Your message..." class="form-input" required></textarea>
            </div>
            <button type="submit" class="w-full bg-teal-600 text-white font-bold py-3 px-4 rounded-lg hover:bg-teal-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-teal-500 transition-all duration-300 transform hover:scale-105">
              Submit Message
            </button>
             <p v-if="successMessage" class="text-center mt-4 text-green-600 font-medium">{{ successMessage }}</p>
          </form>
        </div>

        <div class="contact-details">
          <h2 class="text-2xl font-bold text-gray-800 mb-6">Contact Information</h2>
          <div class="space-y-6 text-gray-700">
            <div class="flex items-start gap-4">
              <span class="text-teal-500 mt-1">📍</span>
              <div>
                <h3 class="font-semibold">Our Office</h3>
                <p>123 Health Tech Avenue, Innovation City, 570023</p>
              </div>
            </div>
            <div class="flex items-start gap-4">
              <span class="text-teal-500 mt-1">✉️</span>
              <div>
                <h3 class="font-semibold">Email Us</h3>
                <p>support@qless-app.com</p>
              </div>
            </div>
            <div class="flex items-start gap-4">
               <span class="text-teal-500 mt-1">📞</span>
              <div>
                <h3 class="font-semibold">Call Us</h3>
                <p>+91 (821) 400-1234</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ContactUs',
  data() {
    return {
      form: {
        name: '',
        email: '',
        subject: '',
        message: ''
      },
      successMessage: ''
    }
  },
  methods: {
    handleSubmit() {
      // In a real application, you would send this data to a backend API.
      // For now, we'll just log it and show a success message.
      console.log('Form Submitted:', this.form);
      
      this.successMessage = "Thank you! Your message has been sent successfully.";
      
      // Reset form after submission
      this.form = { name: '', email: '', subject: '', message: '' };

      // Hide message after a few seconds
      setTimeout(() => {
        this.successMessage = '';
      }, 5000);
    }
  }
}
</script>

<style scoped>
.form-label {
  @apply block text-sm font-medium text-gray-700 mb-1;
}

.form-input {
  @apply block w-full px-4 py-3 bg-gray-50 border border-gray-300 rounded-lg shadow-sm placeholder-gray-400 focus:outline-none focus:ring-teal-500 focus:border-teal-500 sm:text-sm transition-all;
}

@keyframes slideInLeft {
  from { opacity: 0; transform: translateX(-50px); }
  to { opacity: 1; transform: translateX(0); }
}

@keyframes slideInRight {
  from { opacity: 0; transform: translateX(50px); }
  to { opacity: 1; transform: translateX(0); }
}

.contact-form {
  opacity: 0;
  animation: slideInLeft 1s ease-out forwards;
}
.contact-details {
  opacity: 0;
  animation: slideInRight 1s ease-out forwards;
  animation-delay: 200ms;
}
</style>
