<template>
    <div class="container">
      <h2 class="text-center">Admin Login</h2>
      <form @submit.prevent="loginAdmin">
        <div class="mb-3">
          <label for="username">Username</label>
          <input v-model="username" type="text" class="form-control" required>
        </div>
        <div class="mb-3">
          <label for="password">Password</label>
          <input v-model="password" type="password" class="form-control" required>
        </div>
        <button type="submit" class="btn btn-primary w-100">Login</button>
        <p v-if="errorMessage" class="text-danger mt-2">{{ errorMessage }}</p>
      </form>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import { useRouter } from 'vue-router';
  
  const username = ref('');
  const password = ref('');
  const errorMessage = ref('');
  const router = useRouter();
  
  const loginAdmin = async () => {
    try {
      const response = await fetch('http://localhost:5000/login/admin', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username: username.value, password: password.value })
      });
  
      const data = await response.json();
      if (response.ok) {
        router.push('/admin/dashboard');
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
  