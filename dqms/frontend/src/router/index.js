import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../store/auth'

import Home from '../views/Home.vue'
import About from '../views/About.vue'
import PatientLogin from '../views/PatientLogin.vue'
import PatientSignup from '../views/PatientSignup.vue'
import HospitalLogin from '../views/HospitalLogin.vue'
import HospitalSignup from '../views/HospitalSignup.vue'
import PatientDashboard from '../views/PatientDashboard.vue'
import HospitalDashboard from '../views/HospitalDashboard.vue'
import MyTokens from '../views/MyTokens.vue'
import ManageTokens from '../views/ManageTokens.vue'
import Contact from '../views/Contact.vue'

const routes = [
  { path: '/', component: Home },
  { path: '/about', component: About },
  { path: '/patient-login', component: PatientLogin },
  { path: '/patient-signup', component: PatientSignup },
  { path: '/hospital-login', component: HospitalLogin },
  { path: '/hospital-signup', component: HospitalSignup },
  { path: '/patient-dashboard', component: PatientDashboard, meta: { requiresAuth: true, role: 'patient' } },
  { path: '/my-tokens', component: MyTokens, meta: { requiresAuth: true, role: 'patient' } },
  { path: '/hospital-dashboard', component: HospitalDashboard, meta: { requiresAuth: true, role: 'hospital' } },
  { path: '/manage-tokens', component: ManageTokens, meta: { requiresAuth: true, role: 'hospital' } },
  { path: '/contact', component: Contact }
]


const router = createRouter({
  history: createWebHistory(),
  routes
})

// 🔹 Global Navigation Guard
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()

  authStore.checkTokenExpiry()

  if (to.meta.requiresAuth) {
    if (!authStore.isLoggedIn()) {
      // Not logged in or token expired → redirect to Home
      return next('/')
    }
    if (to.meta.role && authStore.role !== to.meta.role) {
      // Wrong role → redirect to Home
      return next('/')
    }
  }

  next()
})

export default router
