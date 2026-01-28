<script>
import LoginForm from '../components/LoginForm.vue';
import RegisterForm from '../components/RegisterForm.vue';

export default {
    name: 'Auth',
    components: { LoginForm, RegisterForm },
    data() {
        return {
            mode: 'login' // Default
        };
    },
    computed: {
        currentComponent() {
            return this.mode === 'login' ? LoginForm : RegisterForm;
        }
    },
    // --- NEW: Watch for URL changes ---
    watch: {
        '$route.query.mode': {
            immediate: true, // Run this check immediately when page loads
            handler(newMode) {
                if (newMode === 'register' || newMode === 'login') {
                    this.mode = newMode;
                }
            }
        }
    },
    methods: {
        switchMode(newMode) {
            this.mode = newMode;
            // Optional: Update URL without reloading page so the browser history is correct
            this.$router.replace({ query: { mode: newMode } });
        }
    }
};
</script>

<template>
    <div class="authWrapper">
        <transition name="fadeSlide" mode="out-in">
            <component :is="currentComponent" :key="mode" @switchMode="switchMode" />
        </transition>
    </div>
</template>

<style scoped>
.authWrapper {
    width: 100%;
    /* Navbar height offset */
    margin-top: 0px; 
    height: calc(100vh - 70px); 
    display: flex;
    justify-content: center;
    align-items: center;
    background: #eef2ff;
}

.fadeSlide-enter-active, .fadeSlide-leave-active {
    transition: all 0.4s ease;
}
.fadeSlide-enter-from, .fadeSlide-leave-to {
    opacity: 0;
    transform: translateY(20px);
}
</style>