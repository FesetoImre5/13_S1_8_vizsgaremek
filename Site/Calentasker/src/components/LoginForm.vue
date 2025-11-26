<script>
export default {
    data() {
        return {
            identifier: '',
            password: '',
            showPassword: false,
            capsLockOn: false,
            rememberMe: false,
            
            // Error states
            identifierError: '',
            passwordError: '',
            
            // Focus states
            isIdentifierFocused: false,
            isPasswordFocused: false
        };
    },
    computed: {
        // Button remains disabled until fields have content
        isFormFilled() {
            return this.identifier.trim().length > 0 && this.password.trim().length > 0;
        }
    },
    methods: {
        checkCapsLock(e) {
            this.capsLockOn = e.getModifierState && e.getModifierState('CapsLock');
        },

        // --- BLUR HANDLERS ---
        // We only clear focus here. Validation happens on button click.
        handleIdentifierBlur() {
            this.isIdentifierFocused = false;
        },
        handlePasswordBlur() {
            this.isPasswordFocused = false;
        },

        // --- BASIC CLIENT-SIDE VALIDATION ---
        validateIdentifier() {
            if (this.identifier.trim() === '') {
                this.identifierError = 'Email or Username is required.';
                return false;
            }
            this.identifierError = '';
            return true;
        },
        validatePassword() {
            if (this.password.length === 0) {
                this.passwordError = 'Password is required.';
                return false;
            }
            // Optional: You can keep length checks here if you want to prevent 
            // sending obviously short passwords to the server.
            this.passwordError = '';
            return true;
        },

        login() {
            // 1. Reset Errors
            this.identifierError = '';
            this.passwordError = '';

            // 2. Basic Client Validation (Empty fields?)
            const identifierValid = this.validateIdentifier();
            const passwordValid = this.validatePassword();

            if (!identifierValid || !passwordValid) {
                return;
            }

            // ---------------------------------------------------------
            // MOCK BACKEND LOGIC (Replace this with your real API call)
            // ---------------------------------------------------------
            
            // A. Simulate a database of users
            const mockUsers = [
                { username: 'user', email: 'user@example.com', password: 'password123' },
                { username: 'admin', email: 'admin@test.com', password: 'password123' }
            ];

            // B. Determine if input is Email or Username
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            const isEmail = emailRegex.test(this.identifier);

            // C. Find the user in the "Database"
            // If isEmail is true, we look for a matching email. Otherwise, matching username.
            const userFound = mockUsers.find(u => 
                isEmail ? u.email === this.identifier : u.username === this.identifier
            );

            // D. Scenario: User NOT found
            if (!userFound) {
                if (isEmail) {
                    this.identifierError = 'Not registered email';
                } else {
                    this.identifierError = 'Not registered username';
                }
                return; // Stop here
            }

            // E. Scenario: User found, check password
            if (userFound.password !== this.password) {
                this.passwordError = 'Incorrect password';
                return; // Stop here
            }

            // ---------------------------------------------------------
            // SUCCESS
            // ---------------------------------------------------------
            console.log('Login successful for:', userFound.username);
            // alert("Login Successful!"); 
        }
    }
};
</script>

<template>
    <div class="authCard">
        <h2 class="title">Login</h2>

        <!-- Identifier Error Message -->
        <p v-if="identifierError" class="errorMessage">{{ identifierError }}</p>
        
        <!-- Email/Username Input Group -->
        <div class="inputGroup" :class="{ 'is-active': identifier || isIdentifierFocused }">
            <input 
                v-model="identifier" 
                type="text" 
                @input="identifierError = ''" 
                @focus="isIdentifierFocused = true" 
                @blur="handleIdentifierBlur"
            />
            <label>Email or Username</label>
        </div>

        <!-- Password Error Message -->
        <p v-if="passwordError" class="errorMessage">{{ passwordError }}</p>

        <!-- Password Input Group -->
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

        <div class="remember">
            <input type="checkbox" v-model="rememberMe" /> Remember me
        </div>

        <!-- Button triggers logic -->
        <button class="primaryBtn" @click="login" :disabled="!isFormFilled">Login</button>

        <p class="switchText">No account? <span class="switch" @click="$emit('switchMode', 'register')">Register</span></p>
    </div>
</template>

<style scoped>
.title{ margin-bottom: 13px; }

/* Input Groups */
.inputGroup { position: relative; margin-bottom: 10px; }
.inputGroup input {
    width: 100%;
    padding: 15px 12px 9px 12px;
    border: 1px solid #d1d5db;
    border-radius: 8px;
    background: #f9fafb;
    font-size: 1rem;
    outline: none;
    transition: all 0.2s ease;
    -webkit-appearance: none;
    line-height: 1.5;
}

/* Floating Labels */
.inputGroup label {
    position: absolute;
    top: 50%;
    left: 12px;
    color: #6b7280;
    font-size: 1rem;
    pointer-events: none;
    transform: translateY(-50%);
    transition: all 0.2s ease;
    padding: 0;
}
.inputGroup.is-active label {
    top: 0px;
    font-size: 0.75rem;
    color: rgb(255, 68, 0);
    transform: translateY(-50%);
    padding: 0 5px;
    background: white;
    left: 8px; 
}
.inputGroup input:focus {
    border-color: rgb(255, 68, 0);
    box-shadow: 0 0 0 1px rgb(255, 68, 0);
}

/* Password Field */
.passwordField { margin-bottom: 5px; }
.passwordField input { padding-right: 50px; }
.passwordField .toggle {
    position: absolute;
    right: 10px;
    top: 50%;
    transform: translateY(-50%);
    padding: 5px;
    z-index: 10;
    color: #6b7280;
    cursor: pointer;
    background: transparent;
    border: none;
    font-size: 0.85rem;
}

/* Errors */
.errorMessage {
    color: #dc2626;
    font-size: 0.8rem;
    text-align: right; 
    margin-bottom: -2px; 
}

/* Button & Card */
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
.primaryBtn:disabled { background: rgb(255, 169, 137); cursor: not-allowed; }
.primaryBtn:disabled:hover { background: rgb(255, 126, 79); }

.switchText { text-align: center; margin-top: 15px; font-size: 1rem; }
.switch { cursor: pointer; color: orangered; font-weight: bold; }
@keyframes pop { from { transform: scale(0.9); opacity:0; } to { transform: scale(1); opacity:1; } }
</style>