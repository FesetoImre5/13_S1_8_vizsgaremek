<script>
import LoginForm from '../components/LoginForm.vue';
import RegisterForm from '../components/RegisterForm.vue';

export default {
    name: 'Auth',
    components: { LoginForm, RegisterForm },
    data() {
        return {
            mode: 'login', // Default
            showSuccessMessage: false
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
        },
        handleRegistrationSuccess() {
            this.showSuccessMessage = true;
            this.switchMode('login');
        }
    }
};
</script>

<template>
    <div class="authWrapper">
        <transition name="fadeSlide" mode="out-in">
            <component 
                :is="currentComponent" 
                :key="mode" 
                @switchMode="switchMode" 
                @registration-success="handleRegistrationSuccess"
            />
        </transition>

        <!-- Success Message -->
        <transition name="popIn">
            <div v-if="showSuccessMessage" class="success-message">
                <div class="content">
                    <span class="icon">✅</span>
                    <span>Registration successful! Please log in</span>
                </div>
                <button class="close-btn" @click="showSuccessMessage = false">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <line x1="18" y1="6" x2="6" y2="18"></line>
                        <line x1="6" y1="6" x2="18" y2="18"></line>
                    </svg>
                </button>
            </div>
        </transition>
    </div>
</template>

<style scoped>
.authWrapper {
    width: 100%;
    /* Navbar height offset */
    margin-top: 0px; 
    min-height: calc(100vh - 70px); 
    display: flex;
    justify-content: center;
    align-items: center;
    background: var(--c-bg);
    padding: 20px 0; /* Add padding for scroll breathing room */
}

.fadeSlide-enter-active, .fadeSlide-leave-active {
    transition: all 0.4s ease;
}
.fadeSlide-enter-from, .fadeSlide-leave-to {
    opacity: 0;
    transform: translateY(20px);
}

/* Success Message Styles */
.success-message {
    position: fixed;
    bottom: 30px;
    left: 50%;
    transform: translateX(-50%);
    background: #10B981; /* Green */
    color: white;
    padding: 15px 25px;
    border-radius: 12px;
    box-shadow: 0 10px 30px rgba(16, 185, 129, 0.3);
    display: flex;
    align-items: center;
    gap: 20px;
    font-weight: 600;
    z-index: 1000;
    z-index: 1000;
    width: 90%;
    max-width: 400px;
    box-sizing: border-box;
    justify-content: space-between;
}

.content {
    display: flex;
    align-items: center;
    gap: 10px;
}

.icon {
    font-size: 1.2rem;
}

.close-btn {
    background: transparent;
    border: none;
    color: white;
    cursor: pointer;
    line-height: 0;
    opacity: 0.8;
    transition: opacity 0.2s;
    padding: 5px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
}
.close-btn:hover {
    opacity: 1;
    background: rgba(255, 255, 255, 0.2);
}

/* Animation */
.popIn-enter-active, .popIn-leave-active {
    transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}
.popIn-enter-from, .popIn-leave-to {
    opacity: 0;
    transform: translate(-50%, 50px);
}
</style>