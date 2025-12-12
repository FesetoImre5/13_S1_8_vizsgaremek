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
    <div class="detailsPageContainer">
        <div class="detailsCard fullHeight">
            <div class="header">
                <h2 class="sectionTitle">Profile Details</h2>
                <p class="sectionSubtitle">Manage your personal account information</p>
            </div>
            
            <div class="divider"></div>
            
            <div v-if="loading" class="statusMsg">Loading user data...</div>
            <div v-else-if="error" class="statusMsg error">{{ error }}</div>
            
            <div v-else class="formContainer">
                <div class="infoGroup">
                    <label>Username</label>
                    <div class="valueField">{{ userData.username }}</div>
                </div>
                
                <div class="infoGroup">
                    <label>Email</label>
                    <div class="valueField">{{ userData.email }}</div>
                </div>
                
                <div class="row">
                    <div class="col-md-6 infoGroup">
                        <label>First Name</label>
                        <div class="valueField">{{ userData.first_name }}</div>
                    </div>
                    <div class="col-md-6 infoGroup">
                        <label>Last Name</label>
                        <div class="valueField">{{ userData.last_name }}</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
/* Main Wrapper: Fills the available space from the parent */
.detailsPageContainer {
    height: 100%;
    width: 100%;
    padding: 0;
    /* Use app background color */
    background-color: var(--c-bg); 
}

/* The Card/Surface: Fills the container, similar to the Groups layout */
.detailsCard {
    background: var(--c-surface);
    height: 100%;
    width: 100%;
    padding: 40px;
    overflow-y: auto; /* Scroll inside if content gets too long */
    
    /* Remove border radius if you want it to look like a full panel, 
       or keep it if there is padding around it in ProfilePage. 
       Based on "fill out", usually implies 0 margin. */
    border-radius: 0; 
}

/* Header Styling */
.header {
    margin-bottom: 20px;
}
.sectionTitle {
    color: var(--c-text-primary);
    font-size: 1.75rem;
    margin: 0 0 5px 0;
    font-weight: bold;
}
.sectionSubtitle {
    color: var(--c-text-secondary);
    margin: 0;
    font-size: 0.95rem;
}

.divider {
    height: 1px;
    background-color: var(--border-color);
    margin: 25px 0;
}

/* Loading / Error */
.statusMsg {
    color: var(--c-text-secondary);
    font-style: italic;
    font-size: 1.1rem;
}
.statusMsg.error {
    color: var(--c-primary);
}

/* Form Container: Restricts width of inputs for readability 
   while the background (.detailsCard) still fills the screen. */
.formContainer {
    max-width: 800px; 
}

/* Form Groups */
.infoGroup {
    margin-bottom: 30px;
}

.infoGroup label {
    font-size: 0.9rem;
    color: var(--c-accent); 
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 10px;
    display: block;
}

/* Value Fields (Read-only inputs) */
.valueField {
    font-size: 1rem;
    color: var(--c-text-primary);
    background-color: var(--c-bg); /* Inset look */
    border: 1px solid var(--border-color);
    border-radius: 8px;
    padding: 15px;
    width: 100%;
    transition: border-color 0.2s;
}

.valueField:hover {
    border-color: var(--c-text-secondary);
}
</style>