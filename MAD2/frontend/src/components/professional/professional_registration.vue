<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const username = ref('');
const email = ref('');
const password = ref('');
const serviceType = ref('');
const experience = ref('');

const registerProfessional = async () => { 
  try {
    const response = await fetch('http://localhost:5000/register/professional', { 
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ 
        username: username.value, 
        email: email.value, 
        password: password.value,
        service_type: serviceType.value,
        experience: experience.value
      })
    });

    if (response.ok) {
      alert('Professional registered successfully! Redirecting to dashboard.');
      router.push('/login/professional'); 
    } else {
      alert('Registration failed. Please try again.');
    }
  } catch (error) {
    console.error('Error:', error);
    alert('An error occurred. Please try again.');
  }
};
</script>

<template>
  <div class="registration-container">
    <h2 class="text-center">Professional Registration</h2> 
    <form @submit.prevent="registerProfessional">
      <div class="form-group">
        <label for="username">Username</label>
        <input type="text" id="username" v-model="username" required />
      </div>
      <div class="form-group">
        <label for="email">Email</label>
        <input type="email" id="email" v-model="email" required />
      </div>
      <div class="form-group">
        <label for="password">Password</label>
        <input type="password" id="password" v-model="password" required />
      </div>
      <div class="form-group">
        <label for="serviceType">Service Type</label>
        <input type="text" id="serviceType" v-model="serviceType" required />
      </div>
      <div class="form-group">
        <label for="experience">Experience (in years)</label>
        <input type="number" id="experience" v-model="experience" required />
      </div>
      <button type="submit" class="btn">Register</button>
    </form>
  </div>
</template>

<style scoped>
.registration-container {
  max-width: 400px;
  margin: auto;
  padding: 20px;
  background-color: #e9edc9;
  border-radius: 8px;
}

.form-group {
  margin-bottom: 10px;
}

label {
  font-weight: bold;
  display: block;
}

input {
  width: 100%;
  padding: 8px;
  margin-top: 5px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.btn {
  background-color: #28a745;
  color: white;
  padding: 10px;
  border: none;
  cursor: pointer;
}

.btn:hover {
  background-color: #218838;
}
</style>
