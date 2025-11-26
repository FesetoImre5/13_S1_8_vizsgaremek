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
            passwordError: '',
            loginGeneralError: '', // NEW state for general error message
            // New focus states for floating label logic
            isIdentifierFocused: false,
            isPasswordFocused: false
        };
    },
    computed: {
        isFormFilled() {
            // Determines if the button should be enabled (has content in both fields)
            return this.identifier.trim().length > 0 && this.password.trim().length > 0;
        }
    },
    methods: {
        checkCapsLock(e) {
            this.capsLockOn = e.getModifierState && e.getModifierState('CapsLock');
        },
        // Kept validation methods for use during the login attempt
        validateIdentifier() {
            return this.identifier.trim() !== '';
        },
        validatePassword() {
            return this.password.length >= 6;
        },
        
        login() {
            this.loginGeneralError = ''; // Clear previous error

            // 1. Perform client-side validation for required/minimum fields
            const identifierValid = this.validateIdentifier();
            const passwordValid = this.validatePassword();

            if (!identifierValid || !passwordValid) {
                // Display general error for missing fields/invalid format
                this.loginGeneralError = 'Please ensure you have entered an email/username and a password of at least 6 characters.';
                console.log('Pre-submission validation failed.');
                return;
            } 

            // 2. Simulate API call failure (for demonstration purposes)
            const simulatedLoginSuccess = false; 

            if (simulatedLoginSuccess) {
                console.log('Login successful:', this.identifier, this.password, this.rememberMe);
            } else {
                // Display the general error message for failed credentials
                this.loginGeneralError = 'Invalid email/username or password.';
                console.log('Simulated login failed.');
            }
        }
    }
};
</script>

<template>
    <div class="authCard">
        <h2 class="title">Login</h2>

        <!-- Email/Username Input Group -->
        <div class="inputGroup" :class="{ 'is-active': identifier || isIdentifierFocused }">
            <input 
                v-model="identifier" 
                type="text" 
                @input="identifierError = ''" 
                @focus="isIdentifierFocused = true" 
                @blur="isIdentifierFocused = false"
            />
            <label>Email or Username</label>
        </div>
        <!-- Inline identifierError message removed -->

        <!-- Password Input Group -->
        <div class="inputGroup passwordField" :class="{ 'is-active': password || isPasswordFocused }">
            <input
                :type="showPassword ? 'text' : 'password'"
                v-model="password"
                @keyup="checkCapsLock($event)"
                @input="passwordError = ''"
                @focus="isPasswordFocused = true"
                @blur="isPasswordFocused = false"
            />
            <label>Password</label>
            <button type="button" class="toggle" @click="showPassword = !showPassword">
                {{ showPassword ? 'Hide' : 'Show' }}
            </button>
        </div>
        <p v-if="capsLockOn" class="capsWarning">Caps Lock is ON</p>
        <!-- Inline passwordError message removed -->

        <div class="remember">
            <input type="checkbox" v-model="rememberMe" /> Remember me
        </div>

        <!-- NEW: General error message appears under 'Remember me' on submission failure -->
        <p v-if="loginGeneralError" class="errorMessage generalError">{{ loginGeneralError }}</p>

        <!-- Button disabled until fields are filled -->
        <button class="primaryBtn" @click="login" :disabled="!isFormFilled">Login</button>

        <!-- Only the word "Register" is clickable -->
        <p class="switchText">No account? <span class="switch" @click="$emit('switchMode', 'register')">Register</span></p>
    </div>
</template>

<style scoped>
.title{
    margin-bottom: 13px;
}

/* New styles for floating label effect */
.inputGroup {
    position: relative;
    margin-bottom: 10px; 
}

/* Base input styling (overrides previous implicit styles) */
.inputGroup input {
    width: 100%;
    /* Adjusted padding: Shifts content down 3px (18+6 -> 15+9) for better vertical centering */
    padding: 15px 12px 9px 12px;
    border: 1px solid #d1d5db; /* gray-300 */
    border-radius: 8px;
    background: #f9fafb; /* gray-50 */
    font-size: 1rem;
    outline: none;
    transition: all 0.2s ease;
    -webkit-appearance: none;
    line-height: 1.5; /* Ensures consistent height */
}

/* Floating Label Styling */
.inputGroup label {
    position: absolute;
    top: 50%; /* Center vertically when acting as placeholder */
    left: 12px;
    color: #6b7280; /* gray-500 */
    font-size: 1rem;
    pointer-events: none; /* Allows clicks to pass through to the input */
    transform: translateY(-50%);
    transition: all 0.2s ease;
    padding: 0;
}

/* Active State (Focused or Filled) */
.inputGroup.is-active label {
    top: 0px; /* Moves to the top */
    font-size: 0.75rem; /* Shrinks */
    color: rgb(255, 68, 0); /* Used primary color for focused label */
    transform: translateY(-50%);
    padding: 0 5px;
    background: white; /* Provides the "cut-out" background for the label */
    left: 8px; 
}

/* Input Focus Border and Shadow */
.inputGroup input:focus {
    border-color: rgb(255, 68, 0); /* Used primary color for focused border */
    box-shadow: 0 0 0 1px rgb(255, 68, 0);
}

/* Specific adjustments for password input/toggle combination */
.passwordField {
    /* Set margin-bottom to 5px to leave room for the caps lock warning */
    margin-bottom: 5px; 
}
.passwordField input {
    /* Ensure input takes up space inside flex container */
    padding-right: 50px; /* Make space for the toggle button */
}

.passwordField .toggle {
    position: absolute;
    right: 10px;
    top: 50%;
    transform: translateY(-50%);
    padding: 5px;
    z-index: 10; /* Ensure button is above the input */
    color: #6b7280;
    cursor: pointer;
    background: transparent;
    border: none;
    font-size: 0.85rem;
}


/* --- Error Styles --- */
.errorMessage {
    color: #dc2626; /* red-600 for visibility */
    font-size: 0.8rem;
    margin-top: 0; 
    margin-bottom: 10px;
}

.generalError {
    text-align: center;
    margin-bottom: 15px !important;
    margin-top: -10px !important;
}

/* --- Button Styles --- */

.primaryBtn:disabled {
    background: rgb(255, 169, 137); /* Lighter color when disabled */
    cursor: not-allowed;
}
.primaryBtn:disabled:hover {
    background: rgb(255, 126, 79); /* Lighter color when disabled */
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

.capsWarning { color: red; font-size:0.85rem; margin-top:0px; margin-bottom: 5px; }

.remember { margin-bottom: 15px; display:flex; gap:6px; align-items:center; }
.primaryBtn { width:100%; padding:10px; border:none; border-radius:10px; background:rgb(255, 68, 0); color:white; cursor:pointer; font-weight:bold; transition:0.2s; }
.primaryBtn:hover { background:rgb(177, 47, 0); }
.primaryBtn:active { background-color: rgb(97, 26, 0); transition-duration: 0s; }

.switchText { 
    text-align: center; 
    margin-top: 15px; 
    font-size: 1rem;
}
.switch { 
    cursor: pointer; 
    color: orangered; 
    font-weight: bold;
}
@keyframes pop { from { transform: scale(0.9); opacity:0; } to { transform: scale(1); opacity:1; } }
</style>