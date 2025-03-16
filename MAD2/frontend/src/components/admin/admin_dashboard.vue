<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router';

const router = useRouter();
const customers = ref([])
const professionals = ref([])
const services = ref([])
const customerRequests = ref({})

const sidebarOpen = ref(false)
const sidebarContent = ref('')
const selectedService = ref(null)

const admin_name = ref('')
const admin_password = ref('')

const fetchData = async () => {
  try {
    const response = await fetch('http://localhost:5000/admin/dashboard')
    const data = await response.json()

    customers.value = data.customers
    professionals.value = data.professionals
    services.value = data.services
    customerRequests.value = data.customer_requests
  } catch (error) {
    console.error('Error fetching data:', error)
  }
}

const toggleBlockCustomer = async (id, isBlocked) => {
  try {
    const endpoint = isBlocked ? `/admin/unblock_customer/${id}` : `/admin/block_customer/${id}`
    const response = await fetch(`http://localhost:5000${endpoint}`, { method: 'POST' })
    const data = await response.json()

    if (response.ok) {
      const customer = customers.value.find(c => c.id === id)
      if (customer) customer.is_blocked = !isBlocked
      alert(data.message)
    }
  } catch (error) {
    console.error('Error updating customer status:', error)
  }
}

const toggleBlockProfessional = async (id, isBlocked) => {
  try {
    const endpoint = isBlocked ? `/admin/unblock_professional/${id}` : `/admin/block_professional/${id}`
    const response = await fetch(`http://localhost:5000${endpoint}`, { method: 'POST' })
    const data = await response.json()

    if (response.ok) {
      const professional = professionals.value.find(p => p.id === id)
      if (professional) professional.is_blocked = !isBlocked
      alert(data.message)
    }
  } catch (error) {
    console.error('Error updating professional status:', error)
  }
}

const approveProfessional = async (id) => {
  try {
    const response = await fetch(`http://localhost:5000/admin/approve_professional/${id}`, { method: 'POST' })
    const data = await response.json()

    if (response.ok) {
      const professional = professionals.value.find(p => p.id === id)
      if (professional) professional.is_approved = true
      alert(data.message)
    }
  } catch (error) {
    console.error('Error approving professional:', error)
  }
}

const deleteService = async (id) => {
  if (!confirm("Are you sure you want to delete this service?")) return

  try {
    const response = await fetch(`http://localhost:5000/admin/delete_service/${id}`, { method: 'DELETE' })
    const data = await response.json()

    if (response.ok) {
      services.value = services.value.filter(service => service.id !== id)
      alert(data.message)
    }
  } catch (error) {
    console.error('Error deleting service:', error)
  }
}

const newService = ref({
  name: '',
  base_price: '',
  location: ''
});
const createService = async () => {
  try {
    const response = await fetch('http://localhost:5000/admin/create_service', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newService.value)
    });

    const data = await response.json();

    if (response.ok) {
      services.value.push(data.service);
      alert('Service created successfully');
      closeSidebar();
    } else {
      alert(data.message || 'Failed to create service');
    }
  } catch (error) {
    console.error('Error creating service:', error);
  }
};

const updateService = async () => {
  try {
    const response = await fetch(`http://localhost:5000/admin/edit_service/${selectedService.value.id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(selectedService.value),
    });

    const data = await response.json();

    if (response.ok) {
      alert('Service updated successfully');
      closeSidebar();
      fetchData(); // Refresh data
    } else {
      alert(data.message || 'Failed to update service');
    }
  } catch (error) {
    console.error('Error updating service:', error);
  }
};

const fetchProfile = async () => {
  try {
    const response = await fetch('http://localhost:5000/admin/dashboard/profile', {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include' // Ensures cookies/session data are sent
    });

    if (!response.ok) {
      throw new Error('Failed to fetch admin profile');
    }

    const data = await response.json();
    admin_name.value = data.username;
    admin_password.value = data.password;
  } catch (error) {
    console.error('Error fetching profile:', error);
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


const openSidebar = (content, service = null) => {
  sidebarContent.value = content
  selectedService.value = { ...service }
  sidebarOpen.value = true
}

const closeSidebar = () => {
  sidebarOpen.value = false
}

onMounted(fetchProfile);
onMounted(fetchData)
</script>

<template>
  <div class="container-fluid mt-5">
    <h3 class="text-center">Admin Dashboard</h3>

    <div class="d-flex justify-content-end mb-4">
      <button @click="openSidebar('profile')" class="btn btn-primary">Profile</button>
      <button @click="logout" class="btn btn-danger float-end">Logout</button>
    </div>

    <h3>Manage Customers</h3>
    <table class="table table-bordered">
      <thead>
        <tr>
          <th>Username</th>
          <th>Service Requests</th>
          <th>Action</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="customer in customers" :key="customer.id">
          <td>{{ customer.username }}</td>
          <td>
            <ul v-if="customerRequests[customer.id]">
              <li v-for="request in customerRequests[customer.id]" :key="request.id">
                {{ request.service.name }} - {{ request.date_of_request }}
              </li>
            </ul>
            <span v-else>None</span>
          </td>
          <td>
            <button @click="toggleBlockCustomer(customer.id, customer.is_blocked)" class="btn" :class="customer.is_blocked ? 'btn-success' : 'btn-danger'">
              {{ customer.is_blocked ? 'Unblock' : 'Block' }}
            </button>
          </td>
        </tr>
      </tbody>
    </table>

    <h3>Manage Professionals</h3>
    <table class="table table-bordered">
      <thead>
        <tr>
          <th>Username</th>
          <th>Service Type</th>
          <th>Experience</th>
          <th>Approval Status</th>
          <th>Action</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="professional in professionals" :key="professional.id">
          <td>{{ professional.username }}</td>
          <td>{{ professional.service_type }}</td>
          <td>{{ professional.experience }} years</td>
          <td>{{ professional.is_approved ? 'Approved' : 'Pending' }}</td>
          <td>
            <button @click="toggleBlockProfessional(professional.id, professional.is_blocked)" class="btn" :class="professional.is_blocked ? 'btn-success' : 'btn-danger'">
              {{ professional.is_blocked ? 'Unblock' : 'Block' }}
            </button>
            <button v-if="!professional.is_approved" @click="approveProfessional(professional.id)" class="btn btn-warning">Approve</button>
          </td>
        </tr>
      </tbody>
    </table>

    <h3>Manage Services</h3>
    <table class="table table-bordered">
      <thead>
        <tr>
          <th>Service Name</th>
          <th>Base Price</th>
          <th>Location</th>
          <th>Action</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="service in services" :key="service.id">
          <td>{{ service.name }}</td>
          <td>{{ service.base_price }}</td>
          <td>{{ service.location }}</td>
          <td>
            <button @click="openSidebar('edit', service)" class="btn btn-warning">Edit</button>
            <button @click="deleteService(service.id)" class="btn btn-danger">Delete</button>
          </td>
        </tr>
      </tbody>
    </table>

    <button @click="openSidebar('create')" class="btn btn-primary mt-3">Create New Service</button>
  </div>

  <!-- Sidebar -->
  <div v-if="sidebarOpen" class="sidebar">
    <div class="sidebar-content">
      <button class="close-btn" @click="closeSidebar">×</button>
      <!-- Profile -->
      <div v-if="sidebarContent === 'profile'">
        <h2>Admin Profile</h2>
        <table class="table">
          <tr>
            <th>Username:</th>
            <td>{{ admin_name }}</td>
          </tr>
          <tr>
            <th>Password:</th>
            <td>{{ admin_password }}</td>
          </tr>
        </table>
        
      </div>

      <!-- Create Service Form -->
      <div v-if="sidebarContent === 'create'">
        <h2>Create Service</h2>
        <form @submit.prevent="createService">
          <div class="mb-3">
            <label for="name" class="form-label">Service Name</label>
            <input v-model="newService.name" type="text" class="form-control" required>
          </div>
          <div class="mb-3">
            <label for="base_price" class="form-label">Base Price</label>
            <input v-model="newService.base_price" type="number" class="form-control" required>
          </div>
          <div class="mb-3">
            <label for="location" class="form-label">Location</label>
            <input v-model="newService.location" type="text" class="form-control" required>
          </div>
          <button type="submit" class="btn btn-primary">Create Service</button>
        </form>
      </div>

      <!-- Edit Service Form -->
      <div v-if="sidebarContent === 'edit'">
        <h2>Edit Service</h2>
        <form @submit.prevent="updateService">
          <div class="mb-3">
            <label for="name">Service Name</label>
            <input v-model="selectedService.name" type="text" class="form-control" required>
          </div>
          <div class="mb-3">
            <label for="base_price">Base Price</label>
            <input v-model="selectedService.base_price" type="number" class="form-control" required>
          </div>
          <div class="mb-3">
            <label for="location">Location</label>
            <input v-model="selectedService.location" type="text" class="form-control" required>
          </div>
          <button type="submit" class="btn btn-primary">Update Service</button>
        </form>
      </div>
    </div>
  </div>
</template>


<style scoped>
.container {
  background-color: #e9edc9;
  padding: 20px;
  border-radius: 10px;
}
</style>
