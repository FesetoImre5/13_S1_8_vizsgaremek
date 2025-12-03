<script setup>
import { onMounted } from 'vue';
import NavBar from './components/NavBar.vue';
import { useAuth } from './composables/UseAuth';

// Initialize Authentication Check
const { checkAuth } = useAuth();

onMounted(() => {
    checkAuth();
});
</script>

<template>
  <NavBar />
  <main>
    <!-- 
      We use the v-slot API to expose the current route component 
      so we can wrap it in a <transition>
    -->
    <router-view v-slot="{ Component }">
      <transition name="fadeSlide" mode="out-in">
        <component :is="Component" />
      </transition>
    </router-view>
  </main>
</template>

<style>
/* Global resets */
body {
  margin: 0; 
  padding-top: 70px; 
  overflow-x: hidden; /* Prevents scrollbars from flickering during animation */
  background-color: #f8f9fa;
}

/* --- PAGE TRANSITIONS (Matching AuthPage.vue) --- */

/* 1. The Duration and Easing */
.fadeSlide-enter-active,
.fadeSlide-leave-active {
    transition: all 0.4s ease;
}

/* 2. The Start/End State 
  - Enter From: Starts invisible and 20px down
  - Leave To: Ends invisible and 20px down
  This creates the effect where the old page drops down/fades out, 
  and the new page rises up/fades in. */
.fadeSlide-enter-from,
.fadeSlide-leave-to {
    opacity: 0;
    transform: translateY(20px);
}
</style>