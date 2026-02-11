<script>
import axios from 'axios';
import { useToast } from '../composables/useToast';

export default {
    data() {
        return {
            status: 'verifying', // verifying, success, error
            message: this.$t('auth.verifying'),
        };
    },
    setup() {
        const { addToast } = useToast();
        return { addToast };
    },
    async mounted() {
        const { uid, token } = this.$route.params;
        
        if (!uid || !token) {
            this.status = 'error';
            this.message = this.$t('auth.invalidLink');
            return;
        }

        try {
            await axios.post('http://127.0.0.1:8000/api/users/activate/', {
                uid,
                token
            });
            this.status = 'success';
            this.message = this.$t('auth.verified');
            this.addToast(this.$t('auth.accountActivated'), 'success');
            
            // Optional: Redirect after a few seconds
            setTimeout(() => {
                this.$router.push({ name: 'Auth', query: { mode: 'login' } });
            }, 3000);

        } catch (error) {
            this.status = 'error';
            this.message = error.response?.data?.detail || this.$t('auth.verificationFailed');
            this.addToast(this.message, 'error');
        }
    }
};
</script>

<template>
    <div class="verify-container">
        <div class="card">
            <h2 v-if="status === 'verifying'">{{ $t('auth.verifying') }}</h2>
            <h2 v-if="status === 'success'" class="success">{{ $t('auth.successTitle') }}</h2>
            <h2 v-if="status === 'error'" class="error">{{ $t('auth.errorTitle') }}</h2>

            <p>{{ message }}</p>

            <button v-if="status !== 'verifying'" @click="$router.push({ name: 'Auth', query: { mode: 'login' } })" class="primaryBtn">
                {{ $t('auth.goToLogin') }}
            </button>
        </div>
    </div>
</template>

<style scoped>
.verify-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    background: var(--c-bg, #121212);
    color: var(--c-text-primary, #E5E7EB);
}

.card {
    background: var(--c-surface, #1E1E1E);
    padding: 40px;
    border-radius: 20px;
    text-align: center;
    box-shadow: 0 10px 25px rgba(0,0,0,0.5);
    border: 1px solid #4B5563;
    max-width: 400px;
    width: 90%;
}

h2 {
    margin-bottom: 20px;
}

.success {
    color: #16a34a;
}

.error {
    color: #dc2626;
}

p {
    margin-bottom: 30px;
    color: var(--c-text-secondary, #9CA3AF);
}

.primaryBtn {
    padding: 12px 24px;
    border: none;
    border-radius: 10px;
    background: var(--c-primary, rgb(255, 68, 0));
    color: white;
    cursor: pointer;
    font-weight: bold;
    transition: 0.2s;
    font-size: 1rem;
}

.primaryBtn:hover {
    background: var(--c-primary-hover, rgb(177, 47, 0));
}
</style>
