<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const userData = ref(null);
const loading = ref(true);
const error = ref('');

const fetchUserProfile = async () => {
    try {
        const userId = localStorage.getItem('user_id');
        if (!userId) throw new Error("User ID not found locally.");

        const response = await axios.get(`http://127.0.0.1:8000/api/users/${userId}/`);
        userData.value = response.data;
    } catch (err) {
        console.error(err);
        error.value = "Failed to load user data.";
    } finally {
        loading.value = false;
    }
};

onMounted(() => {
    fetchUserProfile();
});
</script>

<template>
    <div class="detailsWrapper">
        <h2>Profile Details</h2>
        <hr />
        
        <div v-if="loading">Loading user data...</div>
        <div v-else-if="error" class="text-danger">{{ error }}</div>
        
        <div v-else class="userInfo">
            <div class="infoGroup">
                <label>Username</label>
                <p>{{ userData.username }}</p>
            </div>
            <div class="infoGroup">
                <label>Email</label>
                <p>{{ userData.email }}</p>
            </div>
            <div class="row">
                <div class="col-6 infoGroup">
                    <label>First Name</label>
                    <p>{{ userData.first_name }}</p>
                </div>
                <div class="col-6 infoGroup">
                    <label>Last Name</label>
                    <p>{{ userData.last_name }}</p>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.detailsWrapper {
    background: white;
    padding: 30px;
    border-radius: 12px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    max-width: 600px;
}

.infoGroup {
    margin-bottom: 20px;
}

.infoGroup label {
    font-size: 0.85rem;
    color: #6b7280;
    font-weight: bold;
    text-transform: uppercase;
    margin-bottom: 5px;
    display: block;
}

.infoGroup p {
    font-size: 1.1rem;
    color: #111;
    margin: 0;
    padding: 10px;
    background-color: #f9fafb;
    border-radius: 6px;
    border: 1px solid #e5e7eb;
}
</style>