<script setup>
</script>

<template>
  <!-- Skecthy font -->
  <div>      
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootswatch@4.5.2/dist/sketchy/bootstrap.min.css" integrity="sha384-RxqHG2ilm4r6aFRpGmBbGTjsqwfqHOKy1ArsMhHusnRO47jcGqpIQqlQK/kmGy9R" crossorigin="anonymous">
  </div>
  <header>
    <h1 class="title">Household Services</h1>
  </header>
 
  <nav>
    <router-link to="/">Home</router-link> |
    <router-link to="/register/customer">Customer Registration</router-link> |
    <router-link to="/register/professional">Professional Registration</router-link> 
  </nav>
  
  <main>
    <router-view></router-view>
  </main>
  
</template>

<style scoped>
header {
  text-align: center;
  padding: 1rem;
  background: #007bff;
  color: white;
}

nav {
  text-align: center;
  margin: 1rem 0;
}

nav a {
  text-decoration: none;
  color: #007bff;
  margin: 0 10px;
}

nav a:hover {
  text-decoration: underline;
}

main {
  padding: 2rem;
}
</style>

