import { createRouter, createWebHistory } from 'vue-router';
import Home from '../components/common/Home.vue';
import AdminDashboard from '../components/admin/admin_dashboard.vue';
import CustomerDashboard from '../components/customer/customer_dashboard.vue';
import ProfessionalDashboard from '../components/professional/professional_dashboard.vue';
import AdminLogin from '../components/admin/admin_login.vue';
import CustomerLogin from '../components/customer/customer_login.vue';
import ProfessionalLogin from '../components/professional/professional_login.vue';
import CustomerRegistration from '../components/customer/customer_registration.vue';
import ProfessionalRegistration from '../components/professional/professional_registration.vue';

const routes = [
  { path: '/', component: Home },
  { path: '/register/customer', component: CustomerRegistration },
  { path: '/register/professional', component: ProfessionalRegistration },
  { path: '/login/admin', component: AdminLogin },
  { path: '/login/customer', component: CustomerLogin },
  { path: '/login/professional', component: ProfessionalLogin },
  { path: '/admin/dashboard', component: AdminDashboard },
  { path: '/customer/dashboard', component: CustomerDashboard },
  { path: '/professional/dashboard', component: ProfessionalDashboard },
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
