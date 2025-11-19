<script>
export default {
    name: "Register",
    data() {
        return {
            username: "",
            firstname: "",
            lastname: "",
            email: "",
            password: "",
            errors: {}
        };
    },

    computed: {
        passwordStrength() {
            let score = 0;

            if (this.password.length >= 6) score++;
            if (/[A-Z]/.test(this.password)) score++;
            if (/[0-9]/.test(this.password)) score++;
            if (/[^A-Za-z0-9]/.test(this.password)) score++;

            if (score <= 1) return {label: "Weak", color: "#dc2626", width: "33%"};
            if (score === 2) return {label: "Medium", color: "#f59e0b", width: "66%"};
            return {label: "Strong", color: "#16a34a", width: "100%"};
        }
    },

    methods: {
        validateForm() {
            this.errors = {};
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

            if (!this.username) this.errors.username = "Username required.";
            if (!this.firstname) this.errors.firstname = "First name required.";
            if (!this.lastname) this.errors.lastname = "Last name required.";

            if (!this.email) this.errors.email = "Email required.";
            else if (!emailRegex.test(this.email)) this.errors.email = "Invalid email format.";

            if (!this.password) this.errors.password = "Password required.";
            else if (this.password.length < 6) this.errors.password = "Minimum 6 characters.";

            return Object.keys(this.errors).length === 0;
        },

        register() {
            if (!this.validateForm()) return;

            console.log("Registering:", this.username, this.firstname, this.lastname, this.email, this.password);
            alert("Account created!");
        }
    }
};
</script>

<template>
    <div class="pageWrapper">
        <div class="card">
            <h2>Create Account</h2>

            <form @submit.prevent="register">

                <!-- Username -->
                <div class="inputGroup">
                    <label>Username</label>
                    <input type="text" v-model="username" />
                    <small v-if="errors.username" class="error">{{ errors.username }}</small>
                </div>

                <!-- First Name -->
                <div class="inputGroup">
                    <label>First Name</label>
                    <input type="text" v-model="firstname" />
                    <small v-if="errors.firstname" class="error">{{ errors.firstname }}</small>
                </div>

                <!-- Last Name -->
                <div class="inputGroup">
                    <label>Last Name</label>
                    <input type="text" v-model="lastname" />
                    <small v-if="errors.lastname" class="error">{{ errors.lastname }}</small>
                </div>

                <!-- Email -->
                <div class="inputGroup">
                    <label>Email</label>
                    <input type="email" v-model="email" />
                    <small v-if="errors.email" class="error">{{ errors.email }}</small>
                </div>

                <!-- Password -->
                <div class="inputGroup">
                    <label>Password</label>
                    <input type="password" v-model="password" />
                    <small v-if="errors.password" class="error">{{ errors.password }}</small>

                    <!-- Strength meter -->
                    <div v-if="password" class="strengthBar">
                        <div :style="{
                            width: passwordStrength.width,
                            background: passwordStrength.color
                        }"></div>
                    </div>
                    <small v-if="password" class="strengthLabel" 
                           :style="{ color: passwordStrength.color }">
                        {{ passwordStrength.label }}
                    </small>
                </div>

                <button class="primaryBtn" type="submit">Register</button>
            </form>

            <p class="switchText">
                Already have an account?
                <router-link to="/login">Login</router-link>
            </p>
        </div>
    </div>
</template>

<style scoped>
/* Inherit SAME styling from Login.vue */
.pageWrapper {
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    background: #f4f6fb;
}

.card {
    width: 370px;
    padding: 30px;
    background: white;
    border-radius: 14px;
    box-shadow: 0 6px 20px rgba(0,0,0,0.15);
    text-align: center;
}

h2 {
    margin-bottom: 20px;
}

.inputGroup {
    text-align: left;
    margin-bottom: 18px;
}

.inputGroup label {
    font-size: 0.9rem;
    display: block;
    margin-bottom: 5px;
}

.inputGroup input {
    width: 100%;
    padding: 10px;
    border-radius: 8px;
    border: 1px solid #d0d5dd;
    font-size: 1rem;
}

.error {
    color: #dc2626;
    font-size: 0.8rem;
    margin-top: 4px;
    display: block;
}

.strengthBar {
    height: 8px;
    background: #e5e7eb;
    border-radius: 10px;
    margin-top: 6px;
}

.strengthBar div {
    height: 100%;
    border-radius: 10px;
}

.strengthLabel {
    display: block;
    margin-top: 6px;
    font-size: 0.8rem;
    font-weight: 600;
}

.primaryBtn {
    margin-top: 10px;
    width: 100%;
    padding: 12px;
    background: #4f46e5;
    color: white;
    border-radius: 8px;
    border: none;
    font-size: 1rem;
    cursor: pointer;
}

.primaryBtn:hover {
    background: #4338ca;
}

.switchText {
    margin-top: 15px;
    font-size: 0.9rem;
}
</style>
