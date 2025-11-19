<template>
    <div class="authCard">
        <h2 class="title">Login</h2>

        <label>Email or Username</label>
        <!-- Clear error on input -->
        <input v-model="identifier" type="text" placeholder="Email or Username" @input="identifierError = ''" />
        <p v-if="identifierError" class="errorMessage">{{ identifierError }}</p>

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

        <div class="remember">
            <input type="checkbox" v-model="rememberMe" /> Remember me
        </div>

        <!-- Button disabled if validation fails -->
        <button class="primaryBtn" @click="login" :disabled="!isFormValid">Login</button>

        <!-- Updated event emission to 'switchMode' -->
        <p class="switch" @click="$emit('switchMode', 'register')">No account? Register</p>
    </div>
</template>

<script>
export default {
    data() {
        return {
            identifier: '',
            password: '',
            showPassword: false,
            capsLockOn: false,
            rememberMe: false,
            // New state for errors
            identifierError: '',
            passwordError: ''
        };
    },
    computed: {
        // Determine button state based on basic field presence and length
        isFormValid() {
            return this.identifier.length > 0 && this.password.length >= 6;
        }
    },
    methods: {
        checkCapsLock(e) {
            this.capsLockOn = e.getModifierState && e.getModifierState('CapsLock');
        },
        // Detailed validation logic called on submit
        validateForm() {
            let valid = true;
            this.identifierError = '';
            this.passwordError = '';

            if (this.identifier.trim() === '') {
                this.identifierError = 'Email or Username is required.';
                valid = false;
            }

            if (this.password.length < 6) {
                this.passwordError = 'Password must be at least 6 characters.';
                valid = false;
            }
            
            return valid;
        },
        login() {
            if (this.validateForm()) {
                console.log('Login successful:', this.identifier, this.password, this.rememberMe);
                // Actual login logic here
            } else {
                console.log('Validation failed. Please check errors.');
            }
        }
    }
};
</script>

<style scoped>
/* Class names changed to camelCase: authCard, passwordField, capsWarning, primaryBtn, errorMessage */

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
.passwordField {
    display: flex;
    align-items: center;
}
.toggle { margin-left: 10px; cursor: pointer; background:none; border:none; }
.capsWarning { color: red; font-size:0.85rem; margin-top:-10px; }
.remember { margin-bottom: 15px; display:flex; gap:6px; align-items:center; }
.primaryBtn { width:100%; padding:10px; border:none; border-radius:10px; background:#6366f1; color:white; cursor:pointer; font-weight:bold; transition:0.2s; }
.primaryBtn:hover { background:#4f46e5; }
.switch { text-align:center; margin-top:15px; cursor:pointer; color:#4f46e5; }
@keyframes pop { from { transform: scale(0.9); opacity:0; } to { transform: scale(1); opacity:1; } }
</style>