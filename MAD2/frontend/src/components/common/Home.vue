<script setup>
import { ref, onMounted } from 'vue'

const homeData = ref({})

onMounted(async () => {
  try {
    const response = await fetch('http://127.0.0.1:5000/')
    homeData.value = await response.json()
  } catch (error) {
    console.error("Error fetching home data:", error)
  }
})
</script>

<template>
  <div class="home-container">
    <h1>{{ homeData.message }}</h1>
    <p>{{ homeData.description }}</p>

    <div class="login-buttons">
      <router-link :to="homeData.login_routes?.customer" class="btn btn-primary">Customer Login</router-link>
      <router-link :to="homeData.login_routes?.professional" class="btn btn-secondary">Professional Login</router-link>
      <router-link :to="homeData.login_routes?.admin" class="btn btn-danger">Admin Login</router-link>
    </div>

    <p>Don't have an account? 
      <router-link :to="homeData.registration_routes?.customer">Register as Customer</router-link> or 
      <router-link :to="homeData.registration_routes?.professional">Register as Professional</router-link>
    </p>
  </div>
</template>

<style scoped>
.home-container {
  text-align: center;
  padding: 20px;
}

.login-buttons {
  margin-top: 20px;
}

.btn {
  margin: 5px;
  padding: 10px 20px;
  text-decoration: none;
  border-radius: 5px;
}

.btn-primary {
  background-color: #007bff;
  color: white;
}

.btn-secondary {
  background-color: #6c757d;
  color: white;
}

.btn-danger {
  background-color: #dc3545;
  color: white;
}
</style>
