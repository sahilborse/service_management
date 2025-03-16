<template>
  <div class="container">
    <h2 class="text-center">Customer Dashboard</h2>
    <button @click="logout" class="btn btn-danger float-end">Logout</button>
    <button @click="toggleProfile" class="btn btn-secondary float-end me-2">Profile</button>

    <div v-if="showProfile" class="profile-section mt-4">
      <h3>Customer Profile</h3>
      <table class="table">
        <tr>
          <th>Username:</th>
          <td>{{ customer.username }}</td>
        </tr>
        <tr>
          <th>Email:</th>
          <td>{{ customer.email }}</td>
        </tr>
        <tr>
          <th>Status:</th>
          <td>
            <span :class="customer.is_blocked ? 'text-danger' : 'text-success'">
              {{ customer.is_blocked ? 'Blocked' : 'Active' }}
            </span>
          </td>
        </tr>
      </table>
    </div>

    <h3>Search for Services</h3>
    <form @submit.prevent="fetchServices">
      <div class="mb-3">
        <label for="search" class="form-label">Search for Service</label>
        <input type="text" class="form-control" id="search" v-model="searchQuery" placeholder="Enter service name or location">
      </div>

      <div class="mb-3">
        <label for="search_type" class="form-label">Search By</label>
        <div>
          <label class="radio-inline" style="margin-right: 35px;">
            <input type="radio" v-model="searchType" value="name"> Name
          </label>
          <label class="radio-inline">
            <input type="radio" v-model="searchType" value="location"> Location
          </label>
        </div>
      </div>

      <button type="submit" class="btn btn-primary">Search</button>
    </form>

    <h3>Available Services</h3>
    <table class="table table-bordered" v-if="services.length">
      <thead>
        <tr>
          <th>Service Type</th>
          <th>Service Price</th>
          <th>Location</th>
          <th>Action</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="service in services" :key="service.id">
          <td>{{ service.name }}</td>
          <td>₹{{ service.price }}</td>
          <td>{{ service.location }}</td>
          <td>
            <button @click="requestService(service.id)" class="btn btn-primary">Request Service</button>
          </td>
        </tr>
      </tbody>
    </table>
    <p v-else>No services available.</p>

    <h3>Your Service Requests</h3>
    <table class="table table-bordered" v-if="serviceRequests.length">
      <thead>
        <tr>
          <th>Service Type</th>
          <th>Status</th>
          <th>Completion Date</th>
          <th>Action</th>
          <th>Remarks</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="request in serviceRequests" :key="request.id">
          <td>{{ request.service ? request.service.name : 'N/A' }}</td>
          <td>
            <span :class="statusClass(request.status)">{{ request.status }}</span>
          </td>
          <td>
            <input v-if="request.status === 'Closed'" type="date" v-model="request.completion_date" @change="updateCompletionDate(request.id, request.completion_date)" class="form-control">
            <span v-else>{{ request.completion_date || 'N/A' }}</span>
          </td>
          <td>
            <button v-if="request.status === 'Requested'" @click="toggleEditForm(request)" class="btn btn-primary">Edit</button>
            <button v-if="request.status === 'Requested'" @click="closeRequest(request.id)" class="btn btn-danger">Close</button>
          </td>
          <td>
            <button v-if="request.status === 'Closed'" @click="toggleRemarkForm(request.id)" class="btn btn-secondary">
              {{ remarkForms[request.id] ? 'Hide Remark Form' : 'Give Remark' }}
            </button>
            <div v-if="remarkForms[request.id]" class="remark-form">
              <textarea v-model="remarks[request.id]" class="form-control" rows="3"></textarea>
              <button @click="submitRemark(request.id)" class="btn btn-primary mt-2">Submit Remark</button>
            </div>
            <p v-if="request.remarks"><strong>Your Remark:</strong> {{ request.remarks }}</p>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- Edit Service Request Form -->
    <div v-if="editingRequest" class="edit-form">
      <h3>Edit Service Request</h3>
      <form @submit.prevent="submitEdit">
        <div class="mb-3">
          <label for="editService" class="form-label">Service Type</label>
          <select class="form-control" id="editService" v-model="editingRequest.service_id">
            <option v-for="service in services" :key="service.id" :value="service.id">
              {{ service.name }} - ₹{{ service.price }}
            </option>
          </select>
        </div>
        <div class="mb-3">
          <label for="editLocation" class="form-label">Location</label>
          <input type="text" class="form-control" id="editLocation" v-model="editingRequest.location" required>
        </div>
        <div class="mb-3">
          <label for="editPrice" class="form-label">Price</label>
          <input type="number" class="form-control" id="editPrice" v-model="editingRequest.price" step="0.01" required>
        </div>
        <button type="submit" class="btn btn-primary">Update Request</button>
        <button type="button" @click="cancelEdit" class="btn btn-secondary">Cancel</button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const services = ref([]);
const serviceRequests = ref([]);
const searchQuery = ref('');
const searchType = ref('name');
const remarkForms = ref({});
const remarks = ref({});
const editingRequest = ref(null);
const showProfile = ref(false);
const customer = ref({});

const fetchServices = async () => {
  try {
    const response = await fetch(`http://localhost:5000/customer/dashboard?search=${searchQuery.value}&search_type=${searchType.value}`, {
      method: 'GET',
      credentials: 'include',
    });
    const data = await response.json();
    if (response.ok) {
      services.value = data.services;
      serviceRequests.value = data.service_requests;
    } else {
      console.error(data.error);
    }
  } catch (error) {
    console.error('Fetch error:', error);
  }
};

const fetchProfile = async () => {
  try {
    const response = await fetch('http://localhost:5000/customer/dashboard/profile', {
      method: 'GET',
      credentials: 'include',
    });
    const data = await response.json();
    if (response.ok) {
      customer.value = data;
    } else {
      console.error(data.error);
    }
  } catch (error) {
    console.error('Fetch profile error:', error);
  }
};

const requestService = async (serviceId) => {
  try {
    await fetch(`http://localhost:5000/customer/request_service/${serviceId}`, {
      method: 'POST',
      credentials: 'include',
    });
    fetchServices();
  } catch (error) {
    console.error('Request error:', error);
  }
};

const closeRequest = async (requestId) => {
  try {
    await fetch(`http://localhost:5000/customer/close_request/${requestId}`, {
      method: 'POST',
      credentials: 'include',
    });
    fetchServices();
  } catch (error) {
    console.error('Close request error:', error);
  }
};

const toggleEditForm = (request) => {
  editingRequest.value = { ...request, price: request.service.price };
};

const submitEdit = async () => {
  try {
    await fetch(`http://localhost:5000/customer/edit_service_request/${editingRequest.value.id}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(editingRequest.value),
      credentials: 'include',
    });
    editingRequest.value = null;
    fetchServices();
  } catch (error) {
    console.error('Edit request error:', error);
  }
};

const cancelEdit = () => {
  editingRequest.value = null;
};

const toggleRemarkForm = (requestId) => {
  remarkForms.value[requestId] = !remarkForms.value[requestId];
};

const submitRemark = async (requestId) => {
  try {
    await fetch(`http://localhost:5000/customer/add_remark/${requestId}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ remark: remarks.value[requestId] }),
      credentials: 'include',
    });
    fetchServices();
  } catch (error) {
    console.error('Submit remark error:', error);
  }
};

const updateCompletionDate = async (requestId, completionDate) => {
  try {
    await fetch(`http://localhost:5000/customer/edit_completion_date/${requestId}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ completion_date: completionDate }),
      credentials: 'include',
    });
    fetchServices();
  } catch (error) {
    console.error('Update completion date error:', error);
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

const statusClass = (status) => {
  return {
    'text-success': status === 'Accepted',
    'text-danger': status === 'Rejected',
    'text-warning': status === 'Requested',
    'text-info': status === 'Closed',
  };
};

onMounted(fetchServices);
</script>

<style scoped>
.container {
  max-width: 900px;
  margin: auto;
  padding: 20px;
}

.edit-form {
  margin-top: 20px;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
  background-color: #f9f9f9;
}

.profile-section {
  margin-top: 20px;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
  background-color: #f9f9f9;
}
</style>
