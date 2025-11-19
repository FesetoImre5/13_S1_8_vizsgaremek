<script>
export default {
    name: "Login",
    data() {
        return {
            email: "",
            password: "",
            errors: {}
        };
    },

    methods: {
        validateForm() {
            this.errors = {};

            // Email validation
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!this.email) this.errors.email = "Email is required.";
            else if (!emailRegex.test(this.email)) this.errors.email = "Invalid email format.";

            // Password validation
            if (!this.password) this.errors.password = "Password is required.";
            else if (this.password.length < 6) this.errors.password = "Password must be at least 6 characters.";

            return Object.keys(this.errors).length === 0;
        },

        login() {
            if (!this.validateForm()) return;

            console.log("Logging in with:", this.email, this.password);
            alert("Login successful!");
        }
    }
};
</script>

<template>
    <div class="pageWrapper">
        <div class="card">
            <h2>Login</h2>

            <form @submit.prevent="login">

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
                </div>

                <button class="primaryBtn" type="submit">Login</button>
            </form>

            <p class="switchText">
                Don't have an account?
                <router-link to="/register">Sign up</router-link>
            </p>
        </div>
    </div>
</template>

<style scoped>
/* SHARED STYLE BASE */
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
