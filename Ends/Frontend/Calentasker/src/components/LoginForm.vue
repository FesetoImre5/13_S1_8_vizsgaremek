<script>
import axios from 'axios';
import { useAuth } from '../composables/UseAuth';

export default {
    data() {
        return {
            identifier: '',
            password: '',
            showPassword: false,
            capsLockOn: false,
            rememberMe: false,
            
            identifierError: '',
            passwordError: '',
            
            isIdentifierFocused: false,
            isPasswordFocused: false
        };
    },
    computed: {
        isFormFilled() {
            return this.identifier.trim().length > 0 && this.password.trim().length > 0;
        }
    },
    setup() {
        const { loginUser } = useAuth();
        return { loginUser };
    },
    methods: {
        checkCapsLock(e) { this.capsLockOn = e.getModifierState && e.getModifierState('CapsLock'); },
        handleIdentifierBlur() { this.isIdentifierFocused = false; },
        handlePasswordBlur() { this.isPasswordFocused = false; },
        
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
            this.passwordError = '';
            return true;
        },

        async login() {
            this.identifierError = '';
            this.passwordError = '';

            const identifierValid = this.validateIdentifier();
            const passwordValid = this.validatePassword();

            if (!identifierValid || !passwordValid) return;

            try {
                const response = await axios.post('http://127.0.0.1:8000/api/login/', {
                    username: this.identifier, 
                    password: this.password
                });

                const data = response.data;

                // Update Auth State
                this.loginUser(data); 
                
                console.log('Login successful:', data.username);
                
                // Alert removed as requested

                this.$router.push('/profile'); 

            } catch (error) {
                if (error.response) {
                    const data = error.response.data;
                    if (data.non_field_errors) {
                        this.passwordError = "Invalid username or password.";
                    } else if (data.detail) {
                        this.passwordError = data.detail;
                    } else {
                        this.passwordError = "Login failed. Please check credentials.";
                    }
                } else {
                    this.passwordError = "Network error. Is the server running?";
                }
            }
        }
    }
};
</script>

<template>
    <div class="authCard">
        <h2 class="title">Login</h2>

        <form @submit.prevent="login">
            <p v-if="identifierError" class="errorMessage">{{ identifierError }}</p>
            <div class="inputGroup" :class="{ 'is-active': identifier || isIdentifierFocused }">
                <input v-model="identifier" type="text" @input="identifierError = ''" @focus="isIdentifierFocused = true" @blur="handleIdentifierBlur"/>
                <label>Email or Username</label>
            </div>
            
            <p v-if="passwordError" class="errorMessage">{{ passwordError }}</p>
            <div class="inputGroup passwordField" :class="{ 'is-active': password || isPasswordFocused }">
                <input :type="showPassword ? 'text' : 'password'" v-model="password" @keyup="checkCapsLock($event)" @input="passwordError = ''" @focus="isPasswordFocused = true" @blur="handlePasswordBlur"/>
                <label>Password</label>
                <button type="button" class="toggle" @click="showPassword = !showPassword">{{ showPassword ? 'Hide' : 'Show' }}</button>
            </div>
            <p v-if="capsLockOn" class="capsWarning">Caps Lock is ON</p>

            <!--div class="remember"><input type="checkbox" v-model="rememberMe" /> Remember me</div-->
            <button type="submit" class="primaryBtn" :disabled="!isFormFilled">Login</button>
        </form>
        <p class="switchText">No account? <span class="switch" @click="$emit('switchMode', 'register')">Register</span></p>
    </div>
</template>

<style scoped>
.title { 
    margin-bottom: 20px;
    color: var(--c-text-primary, #E5E7EB);
    text-align: center;
}

.inputGroup { 
    position: relative; 
    margin-bottom: 12px; 
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
    appearance: none; 
    -webkit-appearance: none; 
    line-height: 1.5; 
}

.inputGroup label { 
    position: absolute; 
    top: 50%; 
    left: 12px; 
    color: var(--c-text-secondary, #9CA3AF); 
    font-size: 1rem; 
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

.inputGroup input:focus { 
    border-color: var(--c-primary, rgb(255, 68, 0)); 
    box-shadow: 0 0 0 1px var(--c-primary, rgb(255, 68, 0)); 
}

.passwordField { 
    margin-bottom: 5px; 
}

.passwordField input { 
    padding-right: 50px; 
}

.passwordField .toggle { 
    position: absolute; 
    right: 10px; 
    top: 50%; 
    transform: translateY(-50%); 
    padding: 5px; 
    z-index: 10; 
    color: var(--c-text-secondary, #6b7280); 
    cursor: pointer; 
    background: transparent; 
    border: none; 
    font-size: 0.85rem; 
}
.passwordField .toggle:hover {
    color: var(--c-text-primary, #E5E7EB);
}

.errorMessage { 
    color: var(--c-primary, #dc2626); 
    font-size: 0.8rem; 
    text-align: right; 
    margin-bottom: 2px; 
}

.authCard { 
    background: var(--c-surface, #1E1E1E); 
    padding: 30px;
    width: 100%;
    max-width: 350px;
    border-radius: 20px; 
    box-shadow: 0 10px 25px rgba(0,0,0,0.5); 
    animation: pop 0.4s ease; 
    border: 1px solid #4B5563; /* Lighter border for visibility */
}

.capsWarning { 
    color: var(--c-primary, red); 
    font-size:0.85rem; 
    margin-top:0px; 
    margin-bottom: 5px; 
}

.remember { 
    margin-bottom: 15px; 
    display:flex; 
    gap:6px; 
    align-items:center; 
}

.primaryBtn { 
    width:100%; 
    padding:12px; 
    border:none; 
    border-radius:10px; 
    background: var(--c-primary, rgb(255, 68, 0)); 
    color:white; 
    cursor:pointer; 
    font-weight:bold; 
    transition:0.2s; 
    font-size: 1rem;
}

.primaryBtn:hover { 
    background: var(--c-primary-hover, rgb(177, 47, 0)); 
}

.primaryBtn:active { 
    background-color: rgb(97, 26, 0); 
    transition-duration: 0s; 
}
.primaryBtn:disabled { 
    background: #5a2e24; 
    color: #9CA3AF;
    cursor: not-allowed; 
}

.primaryBtn:disabled:hover { 
    background: #5a2e24; 
}

.switchText { 
    text-align: center; 
    margin-top: 20px; 
    color: var(--c-text-secondary, #9CA3AF);
    font-size: 0.95rem; 
}

.switch { 
    cursor: pointer; 
    color: var(--c-accent, orangered); 
    font-weight: bold; 
}
.switch:hover {
    text-decoration: underline;
}

@keyframes pop { 
    from {
        transform: scale(0.9); 
        opacity:0; 
    } 
    to { 
        transform: scale(1); 
        opacity:1; 
    } 
}
</style>
