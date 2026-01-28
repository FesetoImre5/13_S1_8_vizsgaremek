<script setup>
import { onMounted } from 'vue';
import NavBar from './components/NavBar.vue';
import ToastContainer from './components/ToastContainer.vue';
import { useAuth } from './composables/UseAuth';

// Initialize Authentication Check
const { checkAuth } = useAuth();

onMounted(() => {
    checkAuth();
});
</script>

<template>
  <NavBar />
  <ToastContainer />
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
:root {
    /* --- COLOR PALETTE FROM IMAGE --- */
    --c-bg: #313338;          /* Discord Dark Background */
    --c-surface: #2B2D31;     /* Discord Dark Surface */
    --c-surface-hover: #404249;
    
    --c-text-primary: #E5E7EB; /* The Light Gray */
    --c-text-secondary: #9CA3AF;
    
    --c-primary: #F97316;      /* Orange */
    --c-primary-hover: #EA580C;
    
    --c-accent: #F97316;       /* The Bright Orange */
    
    /* --- BORDERS & SPACING --- */
    --border-color: #333333;
    --radius-md: 12px;
    --radius-lg: 16px;
    --nav-height: 70px;
}
main {
    background-color: var(--c-bg);
} 

body {
    margin: 0; 
    padding-top: var(--nav-height); 
    overflow-x: hidden;
    background-color: var(--c-bg); /* App is now Dark by default */
    color: var(--c-text-primary);
    font-family: 'Inter', Arial, sans-serif; /* Recommend importing Inter font */
}

/* Transitions */
.fadeSlide-enter-active, .fadeSlide-leave-active { transition: all 0.3s ease; }
.fadeSlide-enter-from, .fadeSlide-leave-to { opacity: 0; transform: translateY(20px); }

/* Scrollbar Styling for modern look */
::-webkit-scrollbar { width: 8px; }
::-webkit-scrollbar-track { background: var(--c-bg); }
::-webkit-scrollbar-thumb { background: var(--c-surface-hover); border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: var(--c-accent); }

/* Skeleton Loader */
.skeleton {
    background: linear-gradient(90deg, var(--c-surface) 25%, #2a2a2a 50%, var(--c-surface) 75%);
    background-size: 200% 100%;
    animation: shimmer 1.5s infinite;
    border-radius: 6px;
}

@keyframes shimmer {
    0% { background-position: 200% 0; }
    100% { background-position: -200% 0; }
}
</style>