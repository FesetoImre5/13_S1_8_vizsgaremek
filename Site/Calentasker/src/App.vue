<script setup>
import NavBar from './components/NavBar.vue'
</script>

<template>
  <NavBar />
  <main>
    <router-view />
  </main>
</template>

<style>
/* Global resets if you haven't added them yet */
body {
  margin: 0; 
  padding-top: 70px; 
}

</style>
