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
    /* --- COLOR PALETTE (Enhanced Contrast) --- */
    --c-bg: #101113;          /* Much darker background for depth */
    --c-surface: #26272D;     /* Slightly lighter surface to pop against bg */
    --c-surface-hover: #32333A;
    
    --c-text-primary: #EDECEC; /* Brighter text */
    --c-text-secondary: #9CA3AF;
    
    --c-primary: #F97316;      
    --c-primary-hover: #EA580C;
    
    --c-accent: #F97316;       
    
    /* --- BORDERS & SPACING --- */
    --border-color: #2F3036;   /* Subtle border */
    --radius-md: 12px;
    --radius-lg: 16px;
    --nav-height: 70px;

    /* --- SHADOWS --- */
    --shadow-sm: 0 1px 3px rgba(0,0,0,0.3);
    --shadow-md: 0 4px 6px rgba(0,0,0,0.4);
    --shadow-lg: 0 10px 15px rgba(0,0,0,0.5);
    --shadow-glow: 0 0 15px rgba(249, 115, 22, 0.15); /* Orange glow */
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