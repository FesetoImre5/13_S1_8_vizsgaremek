// src/composables/useAuth.js
import { ref } from 'vue';
import axios from 'axios';

// Global state (outside the function so it persists across components)
const user = ref(null);
const token = ref(localStorage.getItem('token') || null);

export function useAuth() {

    // 1. Check if user is already logged in on App load
    const checkAuth = () => {
        const storedToken = localStorage.getItem('token');
        const storedUser = localStorage.getItem('username');
        const storedDisplay = localStorage.getItem('display_username');

        if (storedToken) {
            token.value = storedToken;
            user.value = {
                username: storedUser,
                display_username: storedDisplay
            };
            // Set default header for future requests
            axios.defaults.headers.common['Authorization'] = `Token ${storedToken}`;
        }
    };

    // 2. Login Action (Updates state and LocalStorage)
    const loginUser = (data) => {
        token.value = data.token;
        user.value = {
            username: data.username,
            display_username: data.display_username
        };

        localStorage.setItem('token', data.token);
        localStorage.setItem('user_id', data.user_id);

        if (data.username) {
            localStorage.setItem('username', data.username);
        } else {
            localStorage.removeItem('username');
        }

        if (data.display_username) {
            localStorage.setItem('display_username', data.display_username);
        }

        axios.defaults.headers.common['Authorization'] = `Token ${data.token}`;
    };

    // 3. Logout Action
    const logout = () => {
        token.value = null;
        user.value = null;
        localStorage.clear();
        delete axios.defaults.headers.common['Authorization'];
    };

    return {
        user,
        token,
        checkAuth,
        loginUser,
        logout
    };
}