<script setup>
import { onMounted } from 'vue';
import NavBar from './components/NavBar.vue';
import { useAuth } from './composables/UseAuth.js';

// Initialize Authentication Check
const { checkAuth } = useAuth();

onMounted(() => {
    checkAuth();
});
</script>

<template>
  <NavBar />
  <main>
    <router-view />
  </main>
</template>

<style>
/* Global resets */
body {
  margin: 0; 
  padding-top: 70px; 
}
</style>