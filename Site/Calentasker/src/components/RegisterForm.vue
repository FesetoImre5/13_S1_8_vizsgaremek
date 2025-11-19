<template>
    <div class="authCard">
        <h2 class="title">Register</h2>

        <label>Email</label>
        <input v-model="email" type="email" @input="emailError = ''" />
        <p v-if="emailError" class="errorMessage">{{ emailError }}</p>

        <label>Username</label>
        <input v-model="username" type="text" @input="usernameError = ''" />
        <p v-if="usernameError" class="errorMessage">{{ usernameError }}</p>

        <label>Password</label>
        <div class="passwordField">
        <input
            :type="showPassword ? 'text' : 'password'"
            v-model="password"
            @keyup="checkCapsLock($event)"
            @input="passwordError = ''"
        />
        <button type="button" class="toggle" @click="showPassword = !showPassword">
            {{ showPassword ? 'Hide' : 'Show' }}
        </button>
    </div>
    <p v-if="capsLockOn" class="capsWarning">Caps Lock is ON</p>
    <p v-if="passwordError" class="errorMessage">{{ passwordError }}</p>

    <div class="strengthMeter" v-if="password">
        <div class="strengthBar" :style="{ width: strength.width, background: strength.color }"></div>
            <small :style="{ color: strength.color }">{{ strength.label }}</small>
        </div>

        <!-- Button disabled if validation fails -->
        <button class="primaryBtn" @click="register" :disabled="!isFormValid">Create Account</button>

        <!-- Updated event emission to 'switchMode' -->
        <p class="switch" @click="$emit('switchMode', 'login')">Already have an account? Login</p>
    </div>
</template>

<script>
export default {
    data() {
        return {
            email: '',
            username: '',
            password: '',
            showPassword: false,
            capsLockOn: false,
            // New state for errors
            emailError: '',
            usernameError: '',
            passwordError: ''
        };
    },
    computed: {
        strength() {
            let score = 0;
            if (this.password.length >= 6) score++;
            if (/[A-Z]/.test(this.password)) score++;
            if (/[0-9]/.test(this.password)) score++;
            if (/[^A-Za-z0-9]/.test(this.password)) score++;
            if (score <= 1) return { label: 'Weak', color: '#dc2626', width: '33%' };
            if (score === 2) return { label: 'Medium', color: '#f59e0b', width: '66%' };
            return { label: 'Strong', color: '#16a34a', width: '100%' };
        },
        // Determine button state based on basic field presence, email format, and password length
        isFormValid() {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            return emailRegex.test(this.email) && 
                   this.username.length > 0 && 
                   this.password.length >= 6;
        }
    },
    methods: {
        checkCapsLock(e) {
            this.capsLockOn = e.getModifierState && e.getModifierState('CapsLock');
        },
        // Detailed validation logic called on submit
        validateForm() {
            let valid = true;
            this.emailError = '';
            this.usernameError = '';
            this.passwordError = '';

            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            
            if (!emailRegex.test(this.email)) {
                this.emailError = 'Please enter a valid email address.';
                valid = false;
            }

            if (this.username.trim() === '') {
                this.usernameError = 'Username is required.';
                valid = false;
            }

            if (this.password.length < 6) {
                this.passwordError = 'Password must be at least 6 characters.';
                valid = false;
            }
            
            return valid;
        },
        register() {
            if (this.validateForm()) {
                console.log('Registration successful:', this.email, this.username, this.password);
                // Actual registration logic here
            } else {
                console.log('Validation failed. Please check errors.');
            }
        }
    }
};
</script>

<style scoped>
/* Class names changed to camelCase: authCard, passwordField, capsWarning, strengthMeter, strengthBar, primaryBtn, errorMessage */

.errorMessage {
    color: #dc2626; /* red-600 for visibility */
    font-size: 0.8rem;
    margin-top: -8px;
    margin-bottom: 10px;
}

.primaryBtn:disabled {
    background: #a5b4fc; /* Lighter color when disabled */
    cursor: not-allowed;
}

.authCard {
    background: white;
    padding: 30px;
    width: 350px;
    border-radius: 20px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.1);
    animation: pop 0.4s ease;
}
.passwordField { display:flex; align-items:center; }
.toggle { margin-left:10px; cursor:pointer; background:none; border:none; }
.capsWarning { color:red; font-size:0.85rem; margin-top:-10px; }
.strengthMeter { margin-bottom: 10px; }
.strengthBar { height: 8px; border-radius: 10px; background:#e5e7eb; }
.primaryBtn { width:100%; padding:10px; border:none; border-radius:10px; background:#6366f1; color:white; cursor:pointer; font-weight:bold; transition:0.2s; }
.primaryBtn:hover { background:#4f46e5; }
.switch { text-align:center; margin-top:15px; cursor:pointer; color:#4f46e5; }
@keyframes pop { from { transform: scale(0.9); opacity:0; } to { transform: scale(1); opacity:1; } }
</style>