<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const professional = ref({});
const serviceRequests = ref([]);
const showProfile = ref(false);

const fetchProfessionalData = async () => {
  try {
    const response = await fetch('http://localhost:5000/professional/dashboard', {
      method: 'GET',
      credentials: 'include'  // Include cookies in requests
    });
    if (response.ok) {
      const data = await response.json();
      serviceRequests.value = data.service_requests;
    } else {
      alert('Failed to fetch dashboard data.');
    }
  } catch (error) {
    console.error('Error:', error);
    alert('An error occurred while fetching data.');
  }
};

const fetchProfessionalProfile = async () => {
  try {
    const response = await fetch('http://localhost:5000/professional/dashboard/profile', {
      method: 'GET',
      credentials: 'include'  // Include cookies in requests
    });
    if (response.ok) {
      const data = await response.json();
      professional.value = data.professional;
    } else {
      alert('Failed to fetch professional profile.');
    }
  } catch (error) {
    console.error('Error:', error);
    alert('An error occurred while fetching profile data.');
  }
};

const handleAction = async (action, requestId) => {
  try {
    const response = await fetch(`http://localhost:5000/professional/${action}/${requestId}`, {
      method: 'POST',
      credentials: 'include'  // Include cookies in requests
    });
    if (response.ok) {
      fetchProfessionalData(); // Refresh service requests
    } else {
      alert('Action failed. Please try again.');
    }
  } catch (error) {
    console.error('Error:', error);
    alert('An error occurred.');
  }
};

const logout = async () => {
  try {
    await fetch('http://localhost:5000/logout', {
      method: 'POST',
      credentials: 'include',
    });
    router.push('/');
  } catch (error) {
    console.error('Logout error:', error);
  }
};

const toggleProfile = () => {
  showProfile.value = !showProfile.value;
  if (showProfile.value) {
    fetchProfile();
  }
};

onMounted(() => {
  fetchProfessionalData();
  fetchProfessionalProfile();
});
</script>

<template>
  <div class="container">
    <h2 class="text-center">Professional Dashboard</h2>

    <!-- Profile and Logout Buttons -->
    <div class="d-flex justify-content-end mb-4">
      <button @click="logout" class="btn btn-danger float-end">Logout</button>
      <button @click="toggleProfile" class="btn btn-secondary float-end me-2">Profile</button>
    </div>

    <div v-if="showProfile" class="profile-section mt-4">
      <h3>Professional Profile</h3>
      <table class="table">
        <tr>
          <th>Username:</th>
          <td>{{ professional.username }}</td>
        </tr>
        <tr>
          <th>Email:</th>
          <td>{{ professional.email }}</td>
        </tr>
        <tr>
          <th>Service Type:</th>
          <td>{{ professional.service_type }}</td>
        </tr>
        <tr>
          <th>Experience:</th>
          <td>{{ professional.experience }} years</td>
        </tr>
        <tr>
          <th>Status:</th>
          <td>
            <span :class="professional.is_blocked ? 'text-danger' : 'text-success'">
              {{ professional.is_blocked ? 'Blocked' : 'Active' }}
            </span>
          </td>
        </tr>
        <tr>
          <th>Approval Status:</th>
          <td>
            <span :class="professional.is_approved ? 'text-success' : 'text-warning'">
              {{ professional.is_approved ? 'Approved' : 'Pending Approval' }}
            </span>
          </td>
        </tr>
      </table>
    </div>

    <h3>Your Service Requests</h3>
    <table class="table table-bordered">
      <thead>
        <tr>
          <th>Customer</th>
          <th>Service Type</th>
          <th>Status</th>
          <th>Action</th>
          <th>Remarks</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="request in serviceRequests" :key="request.id">
          <td>{{ request.customer ? request.customer.username : 'N/A' }}</td>
          <td>{{ request.service ? request.service.name : 'N/A' }}</td>
          <td>
            <span :class="{
              'text-success': request.status === 'Accepted',
              'text-danger': request.status === 'Rejected',
              'text-warning': request.status === 'Requested',
              'text-muted': request.status === 'Closed'
            }">
              {{ request.status }}
            </span>
          </td>
          <td>
            <button v-if="request.status === 'Requested'" @click="handleAction('accept_request', request.id)" class="btn btn-success">Accept</button>
            <button v-if="request.status === 'Requested'" @click="handleAction('reject_request', request.id)" class="btn btn-danger">Reject</button>
            <button v-if="request.status === 'Accepted'" @click="handleAction('close_request', request.id)" class="btn btn-info">Close</button>
          </td>
          <td>
            <p v-if="request.remarks">{{ request.remarks }}</p>
            <p v-else>No remark available.</p>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<style scoped>
.container {
  max-width: 800px;
  margin: auto;
}

.table {
  width: 100%;
  margin-top: 20px;
}

.btn {
  margin-right: 5px;
}

.profile-section {
  margin-top: 20px;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
  background-color: #f9f9f9;
}
</style>
