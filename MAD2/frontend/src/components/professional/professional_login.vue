<template>
  <div class="container">
    <h2 class="text-center">Professional Login</h2>
    <form @submit.prevent="loginProfessional">
      <div class="mb-3">
        <label for="username" class="form-label">Username</label>
        <input v-model="username" type="text" class="form-control" id="username" required>
      </div>
      <div class="mb-3">
        <label for="password" class="form-label">Password</label>
        <input v-model="password" type="password" class="form-control" id="password" required>
      </div>
      <button type="submit" class="btn btn-primary w-100">Login</button>
      <p v-if="errorMessage" class="text-danger mt-2">{{ errorMessage }}</p>
    </form>
    <p class="mt-3">Don't have an account? 
      <router-link to="/register/professional">Register Here</router-link>
    </p>  
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const username = ref('');
const password = ref('');
const errorMessage = ref('');
const router = useRouter();

const loginProfessional = async () => {
  try {
    const response = await fetch('http://localhost:5000/login/professional', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: "include",  // Include cookies in requests
      body: JSON.stringify({ username: username.value, password: password.value })
    });

    const data = await response.json();
    if (response.ok) {
      router.push('/professional/dashboard');  // Redirect after successful login
    } else {
      errorMessage.value = data.message || 'Login failed';
    }
  } catch (error) {
    errorMessage.value = 'An error occurred. Please try again.';
  }
};
</script>

<style scoped>
.container {
  max-width: 400px;
  margin: auto;
  padding: 20px;
}
</style>