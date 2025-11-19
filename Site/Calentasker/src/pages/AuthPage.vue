<script>
import LoginForm from '../components/LoginForm.vue';
import RegisterForm from '../components/RegisterForm.vue';

export default {
    name: 'Auth',
    components: { LoginForm, RegisterForm },
    data() {
        return {
            mode: 'login'
        };
    },
    computed: {
        currentComponent() {
            return this.mode === 'login' ? LoginForm : RegisterForm;
        }
    },
    methods: {

        switchMode(newMode) {
            this.mode = newMode;
        }
    }
};
</script>

<template>
    <div class="authWrapper">
        <transition name="fadeSlide" mode="out-in">
            <!-- Updated to listen for the camelCase event 'switchMode' -->
            <component :is="currentComponent" :key="mode" @switchMode="switchMode" />
        </transition>
    </div>
</template>


<style scoped>
/* Class names changed to camelCase: authWrapper, fadeSlide */
.authWrapper {
    width: 100%;
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    background: #eef2ff;
}

.fadeSlide-enter-active,
.fadeSlide-leave-active {
    transition: all 0.4s ease;
}
.fadeSlide-enter-from,
.fadeSlide-leave-to {
    opacity: 0;
    transform: translateY(20px);
}
</style>