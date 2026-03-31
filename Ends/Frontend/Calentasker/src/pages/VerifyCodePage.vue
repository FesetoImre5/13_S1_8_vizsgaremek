<script>
import axios from 'axios';
import { useToast } from '../composables/useToast';

export default {
    data() {
        return {
            status: 'verifying', // verifying, success, error
            email: this.$route.query.email || '',
            code: '',
            codeError: '',
            message: this.$t('auth.verifying'), // Not used initially except instructions
            isEmailFocused: false,
            isCodeFocused: false,
            isLoading: false,
            isResending: false,
            resendCooldown: 0,
            resendTimer: null,
        };
    },
    setup() {
        const { addToast } = useToast();
        return { addToast };
    },
    methods: {
        async verifyCode() {
            if (!this.email || !this.code) {
                this.addToast(this.$t('auth.enterBoth') || 'Please enter both email and code.', 'error');
                return;
            }

            this.isLoading = true;
            try {
                await axios.post('http://127.0.0.1:8000/api/users/activate/', {
                    email: this.email,
                    code: this.code
                });
                this.status = 'success';
                this.addToast(this.$t('auth.accountActivated') || 'Account successfully activated!', 'success');
                
                // Redirect after a few seconds
                setTimeout(() => {
                    this.$router.push({ name: 'Auth', query: { mode: 'login' } });
                }, 2000);

            } catch (error) {
                this.status = 'error';
                const errorMsg = this.$t('auth.invalidCode') || 'Invalid Code';
                this.codeError = errorMsg;
                this.addToast(errorMsg, 'error');
            } finally {
                this.isLoading = false;
            }
        },
        startCooldown() {
            this.resendCooldown = 60;
            this.resendTimer = setInterval(() => {
                if (this.resendCooldown > 0) {
                    this.resendCooldown--;
                } else {
                    clearInterval(this.resendTimer);
                    this.resendTimer = null;
                }
            }, 1000);
        },
        async resendCode() {
            if (!this.email) {
                this.addToast(this.$t('auth.email') || 'Email required', 'error');
                return;
            }
            if (this.resendCooldown > 0) return;

            this.isResending = true;
            try {
                await axios.post('http://127.0.0.1:8000/api/users/resend_code/', {
                    email: this.email
                });
                this.addToast(this.$t('auth.codeResent') || 'Verification code resent successfully!', 'success');
                this.startCooldown();
            } catch (error) {
                const errorMsg = error.response?.data?.detail || this.$t('errors.unknown') || 'Error resending code';
                this.addToast(errorMsg, 'error');
            } finally {
                this.isResending = false;
            }
        }
    },
    beforeUnmount() {
        if (this.resendTimer) {
            clearInterval(this.resendTimer);
        }
    }
};
</script>

<template>
    <div class="verify-container">
        <div class="card">
            <h2>{{ status === 'success' ? ($t('auth.successTitle') || 'Success!') : ($t('auth.verifyAccountTitle') || 'Verify Your Account') }}</h2>
            
            <p v-if="status === 'success'" class="success">{{ $t('auth.redirectingLogin') || 'Your account has been activated! Redirecting to login...' }}</p>
            <p v-else>{{ $t('auth.verifyInstructions') || 'Please enter your email and the 6-digit verification code you received.' }}</p>

            <form v-if="status !== 'success'" @submit.prevent="verifyCode">
                <div class="inputGroup" :class="{ 'is-active': email || isEmailFocused }">
                    <input 
                        v-model="email" 
                        type="email" 
                        required
                        @focus="isEmailFocused = true" 
                        @blur="isEmailFocused = false" 
                    />
                    <label>{{ $t('auth.email') || 'Email' }}</label>
                </div>
                
                <p v-if="codeError" class="errorMessage">{{ codeError }}</p>
                <div class="inputGroup" :class="{ 'is-active': code || isCodeFocused, 'has-error': codeError }">
                    <input 
                        v-model="code" 
                        type="text" 
                        required
                        maxlength="6"
                        @input="codeError = ''"
                        @focus="isCodeFocused = true" 
                        @blur="isCodeFocused = false" 
                    />
                    <label>{{ $t('auth.verifyCodeLabel') || 'Verification Code' }}</label>
                </div>

                <button type="submit" class="primaryBtn" :disabled="isLoading || isResending">
                    {{ isLoading ? ($t('auth.verifying') || 'Verifying...') : ($t('auth.verifyBtn') || 'Verify Code') }}
                </button>
            </form>

            <div v-if="status !== 'success'" class="resend-section">
                <button 
                    @click="resendCode" 
                    type="button" 
                    class="linkBtn resendBtn" 
                    :disabled="isResending || resendCooldown > 0">
                    {{ 
                        isResending 
                            ? ($t('auth.resending') || 'Resending...') 
                            : (resendCooldown > 0 
                                ? ($t('auth.resendCooldown')?.replace('{s}', resendCooldown.toString()) || `Wait ${resendCooldown}s`)
                                : ($t('auth.resendCode') || 'Resend Code'))
                    }}
                </button>
            </div>

            <button v-if="status === 'error'" @click="$router.push({ name: 'Auth', query: { mode: 'login' } })" class="linkBtn">
                {{ $t('auth.goToLogin') || 'Back to Login' }}
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
    padding: 30px;
    border-radius: 20px;
    text-align: center;
    box-shadow: 0 10px 25px rgba(0,0,0,0.5);
    border: 1px solid #4B5563;
    max-width: 400px;
    width: 90%;
    animation: popIn 0.4s ease;
}

h2 {
    margin-bottom: 20px;
    color: var(--c-text-primary, #E5E7EB);
}

.success {
    color: #10B981;
    margin-bottom: 20px;
}

p {
    margin-bottom: 25px;
    color: var(--c-text-secondary, #9CA3AF);
}

form {
    display: flex;
    flex-direction: column;
    gap: 15px;
}

/* Error Styles */
.errorMessage {
    color: var(--c-primary, #dc2626);
    font-size: 0.8rem;
    text-align: right; 
    margin-bottom: 2px;
}

/* Base input styling (reusing from auth) */
.inputGroup {
    position: relative;
    margin-bottom: 5px; 
}

.inputGroup input {
    width: 100%;
    padding: 15px 12px 9px 12px;
    border: 1px solid var(--border-color, #333333);
    border-radius: 8px;
    background: var(--c-bg, #121212); 
    color: var(--c-text-primary, #E5E7EB);
    font-size: 1rem;
    outline: none;
    transition: all 0.2s ease;
}

.inputGroup input:focus {
    border-color: var(--c-primary, rgb(255, 68, 0));
}

.inputGroup.has-error input {
    border-color: var(--c-primary, #dc2626);
    box-shadow: 0 0 0 1px var(--c-primary, #dc2626);
}

.inputGroup label {
    position: absolute;
    top: 50%; 
    left: 12px;
    color: var(--c-text-secondary, #9CA3AF);
    pointer-events: none;
    transform: translateY(-50%);
    transition: all 0.2s ease;
    padding: 0;
}

.inputGroup.is-active label {
    top: 0px; 
    font-size: 0.75rem; 
    color: var(--c-primary, rgb(255, 68, 0)); 
    transform: translateY(-50%);
    padding: 0 5px;
    background: var(--c-surface, #1E1E1E); 
    left: 8px; 
    border-radius: 4px;
}

.inputGroup.has-error label {
    color: var(--c-primary, #dc2626);
}

.primaryBtn {
    padding: 12px;
    border: none;
    border-radius: 10px;
    background: var(--c-primary, rgb(255, 68, 0));
    color: white;
    cursor: pointer;
    font-weight: bold;
    transition: 0.2s;
    font-size: 1rem;
    margin-top: 10px;
}

.primaryBtn:hover:not(:disabled) {
    background: var(--c-primary-hover, rgb(177, 47, 0));
}

.primaryBtn:disabled {
    background: #5a2e24;
    cursor: not-allowed;
    color: #9CA3AF;
}

.linkBtn {
    margin-top: 20px;
    background: transparent;
    border: none;
    color: var(--c-accent, orangered);
    cursor: pointer;
    font-size: 0.95rem;
    font-weight: 600;
}
.linkBtn:hover {
    text-decoration: underline;
}

.resend-section {
    margin-top: 15px;
}
.resendBtn:disabled {
    color: var(--c-text-secondary, #9CA3AF);
    cursor: not-allowed;
    text-decoration: none;
}

@keyframes popIn {
    0% { opacity: 0; transform: scale(0.95); }
    100% { opacity: 1; transform: scale(1); }
}
</style>
