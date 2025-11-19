<template>
    <div class="authCard">
        <h2 class="title">Register</h2>

        <!-- First Name Input Group -->
        <p v-if="firstNameError" class="errorMessage">{{ firstNameError }}</p>
        <div class="inputGroup" :class="{ 'is-active': firstName || isFirstNameFocused }">
            <input 
                v-model="firstName" 
                type="text" 
                @input="firstNameError = ''" 
                @focus="isFirstNameFocused = true" 
                @blur="handleFirstNameBlur" 
            />
            <label>First Name</label>
        </div>

        <!-- Last Name Input Group -->
        <p v-if="lastNameError" class="errorMessage">{{ lastNameError }}</p>
        <div class="inputGroup" :class="{ 'is-active': lastName || isLastNameFocused }">
            <input 
                v-model="lastName" 
                type="text" 
                @input="lastNameError = ''" 
                @focus="isLastNameFocused = true" 
                @blur="handleLastNameBlur" 
            />
            <label>Last Name</label>
        </div>

        <!-- Email Input Group -->
        <p v-if="emailError" class="errorMessage">{{ emailError }}</p>
        <div class="inputGroup" :class="{ 'is-active': email || isEmailFocused }">
            <input 
                v-model="email" 
                type="email" 
                @input="emailError = ''" 
                @focus="isEmailFocused = true" 
                @blur="handleEmailBlur" 
            />
            <label>Email</label>
        </div>

        <!-- Username Input Group -->
        <p v-if="usernameError" class="errorMessage">{{ usernameError }}</p>
        <div class="inputGroup" :class="{ 'is-active': username || isUsernameFocused }">
            <input 
                v-model="username" 
                type="text" 
                @input="usernameError = ''" 
                @focus="isUsernameFocused = true" 
                @blur="handleUsernameBlur" 
            />
            <label>Username</label>
        </div>

        <!-- Password Input Group -->

        <!-- Note: This p tag must not have the 'inputError' class applied if the strengthMeter is present -->
        <p v-if="passwordError" class="errorMessage" :class="{ 'inputError': !password }">{{ passwordError }}</p>

        <div class="inputGroup passwordField" :class="{ 'is-active': password || isPasswordFocused }">
            <input
                :type="showPassword ? 'text' : 'password'"
                v-model="password"
                @keyup="checkCapsLock($event)"
                @input="passwordError = ''"
                @focus="isPasswordFocused = true"
                @blur="handlePasswordBlur"
            />
            <label>Password</label>
            <button type="button" class="toggle" @click="showPassword = !showPassword">
                {{ showPassword ? 'Hide' : 'Show' }}
            </button>
        </div>
        <p v-if="capsLockOn" class="capsWarning">Caps Lock is ON</p>
        

        <div class="strengthMeter" v-if="password">
            <div class="strengthBar" :style="{ width: strength.width, background: strength.color }"></div>
            <small :style="{ color: strength.color }">{{ strength.label }}</small>
        </div>

        <!-- Button disabled if computed form validity fails -->
        <button class="primaryBtn" @click="register" :disabled="!isFormValid">Create Account</button>

        <!-- Only the word "Login" is clickable -->
        <p class="switchText">Already have an account? <span class="switch" @click="$emit('switchMode', 'login')">Login</span></p>
    </div>
</template>

<script>
export default {
    data() {
        return {
            email: '',
            username: '',
            password: '',
            firstName: '', // NEW
            lastName: '',  // NEW
            showPassword: false,
            capsLockOn: false,
            // New state for errors
            emailError: '',
            usernameError: '',
            passwordError: '',
            firstNameError: '', // NEW
            lastNameError: '',  // NEW
            // New focus states for floating label logic
            isEmailFocused: false,
            isUsernameFocused: false,
            isPasswordFocused: false,
            isFirstNameFocused: false, // NEW
            isLastNameFocused: false  // NEW
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
        isFormValid() {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            // Added check for new fields
            return emailRegex.test(this.email) && 
                   this.username.length > 0 && 
                   this.password.length >= 6 &&
                   this.firstName.length > 0 &&
                   this.lastName.length > 0;
        }
    },
    methods: {
        checkCapsLock(e) {
            this.capsLockOn = e.getModifierState && e.getModifierState('CapsLock');
        },
        
        // --- Dedicated Blur Handlers (New) ---
        handleFirstNameBlur() {
            this.validateFirstName();
            this.isFirstNameFocused = false;
        },
        handleLastNameBlur() {
            this.validateLastName();
            this.isLastNameFocused = false;
        },
        handleEmailBlur() {
            this.validateEmail();
            this.isEmailFocused = false;
        },
        handleUsernameBlur() {
            this.validateUsername();
            this.isUsernameFocused = false;
        },
        handlePasswordBlur() {
            this.validatePassword();
            this.isPasswordFocused = false;
        },
        
        // --- Validation Methods (Existing) ---
        validateFirstName() {
            if (this.firstName.trim() === '') {
                this.firstNameError = 'First Name is required.';
                return false;
            }
            this.firstNameError = '';
            return true;
        },
        validateLastName() {
            if (this.lastName.trim() === '') {
                this.lastNameError = 'Last Name is required.';
                return false;
            }
            this.lastNameError = '';
            return true;
        },
        validateEmail() {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(this.email)) {
                this.emailError = 'Please enter a valid email address.';
                return false;
            }
            this.emailError = '';
            return true;
        },
        validateUsername() {
            if (this.username.trim() === '') {
                this.usernameError = 'Username is required.';
                return false;
            }
            this.usernameError = '';
            return true;
        },
        validatePassword() {
            if (this.password.length < 6) {
                this.passwordError = 'Password must be at least 6 characters.';
                return false;
            }
            this.passwordError = '';
            return true;
        },
        validateForm() {
            const emailValid = this.validateEmail();
            const usernameValid = this.validateUsername();
            const passwordValid = this.validatePassword();
            const firstNameValid = this.validateFirstName(); // NEW
            const lastNameValid = this.validateLastName();   // NEW
            return emailValid && usernameValid && passwordValid && firstNameValid && lastNameValid;
        },
        register() {
            if (this.validateForm()) {
                console.log('Registration successful:', this.email, this.username, this.password);
            } else {
                console.log('Validation failed. Please check errors.');
            }
        }
    }
};
</script>

<style scoped>
.title{
    margin-bottom: 13px;
}

/* New styles for floating label effect */
.inputGroup {
    position: relative;
    /* Use standard margin-bottom and adjust error margin instead of relying on negative margin */
    margin-bottom: 10px; 
}

/* Base input styling (overrides previous implicit styles) */
.inputGroup input {
    width: 100%;
    /* Adjusted padding for vertical alignment: 15px top, 9px bottom */
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

/* --- Error Styles (New spacing logic) --- */

.errorMessage {
    color: #dc2626; /* red-600 for visibility */
    font-size: 0.8rem;
    /* Reset margins for generic error message */
    text-align: right; 
    margin-bottom: -2px;
}

/* New class to pull the error message closer to the input when it appears directly after an inputGroup */
.inputError {
    margin-bottom: -2px; /* Pulls it up into the space left by inputGroup's margin-bottom */
    text-align: right;
}

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
.capsWarning { color:red; font-size:0.85rem; margin-top:0; margin-bottom: 5px; } 
.strengthMeter { margin-bottom: 10px; }
.strengthBar { height: 8px; border-radius: 10px; background:#e5e7eb; }
.primaryBtn { width:100%; padding:10px; border:none; border-radius:10px; background:rgb(255, 68, 0); color:white; cursor:pointer; font-weight:bold; transition:0.2s; }
.primaryBtn:hover { background:rgb(177, 47, 0); }
.primaryBtn:active { background-color: rgb(97, 26, 0); transition-duration: 0s; }

/* NEW CLASS: switchText centers the whole line */
.switchText { 
    text-align: center; 
    margin-top: 15px; 
    font-size: 1rem; /* Adjust font size to match surrounding text */
}

/* EXISTING CLASS: switch applies click styling only to the span */
.switch { 
    cursor: pointer; 
    color: orangered; 
    font-weight: bold; /* Make the link stand out more */
}

@keyframes pop { from { transform: scale(0.9); opacity:0; } to { transform: scale(1); opacity:1; } }
</style>