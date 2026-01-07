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
    margin-bottom: 13px; 
}

.inputGroup { 
    position: relative; 
    margin-bottom: 10px; 
}

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
    color: #6b7280; 
    cursor: pointer; 
    background: transparent; 
    border: none; 
    font-size: 0.85rem; 
}

.errorMessage { 
    color: #dc2626; 
    font-size: 0.8rem; 
    text-align: right; 
    margin-bottom: -2px; 
}

.authCard { 
    background: white; 
    padding: 30px; 
    width: 350px; 
    border-radius: 20px; 
    box-shadow: 0 8px 20px rgba(0,0,0,0.1); 
    animation: pop 0.4s ease; 
}

.capsWarning { 
    color: red; 
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
    padding:10px; 
    border:none; 
    border-radius:10px; 
    background:rgb(255, 68, 0); 
    color:white; 
    cursor:pointer; 
    font-weight:bold; 
    transition:0.2s; 
}

.primaryBtn:hover { 
    background:rgb(177, 47, 0); 
}

.primaryBtn:active { 
    background-color: rgb(97, 26, 0); 
    transition-duration: 0s; 
}
.primaryBtn:disabled { 
    background: rgb(255, 169, 137); 
    cursor: not-allowed; 
}

.primaryBtn:disabled:hover { 
    background: rgb(255, 126, 79); 
}

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