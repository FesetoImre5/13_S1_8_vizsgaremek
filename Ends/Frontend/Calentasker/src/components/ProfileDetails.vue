<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const userData = ref({});
const editableUsername = ref('');
const loading = ref(true);
const error = ref('');
const isEditing = ref(false);
const saveError = ref('');
const saveSuccess = ref('');

const newPassword = ref('');
const confirmPassword = ref('');
const pwError = ref('');
const pwSuccess = ref('');
const fileInput = ref(null);


const fetchUserProfile = async () => {
    try {
        const userId = localStorage.getItem('user_id');
        if (!userId) throw new Error("User ID not found locally.");

        const response = await axios.get(`http://127.0.0.1:8000/api/users/${userId}/`);
        userData.value = response.data;
        editableUsername.value = userData.value.username || '';
    } catch (err) {
        console.error(err);
        error.value = "Failed to load user data.";
    } finally {
        loading.value = false;
    }
};

const saveUsername = async () => {
    saveError.value = '';
    saveSuccess.value = '';
    
    try {
        const userId = localStorage.getItem('user_id');
        // If empty, send null to backend (assuming backend handles it) or empty string
        const payload = {
            username: editableUsername.value.trim() ? editableUsername.value.trim() : null
        };

        const response = await axios.patch(`http://127.0.0.1:8000/api/users/${userId}/`, payload);
        
        userData.value = response.data;
        editableUsername.value = userData.value.username || '';
        saveSuccess.value = 'Username updated successfully!';
        isEditing.value = false;
        
        // Hide success message after 3 seconds
        setTimeout(() => {
            saveSuccess.value = '';
        }, 3000);
        
    } catch (err) {
        console.error(err);
        if (err.response && err.response.data && err.response.data.username) {
            saveError.value = err.response.data.username[0];
        } else {
            saveError.value = "Failed to update username.";
        }
    }
};

const cancelEdit = () => {
    editableUsername.value = userData.value.username || '';
    isEditing.value = false;
    saveError.value = '';
};

const triggerFileInput = () => {
    fileInput.value.click();
};

const handleFileChange = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('profile_picture', file);

    try {
        const userId = localStorage.getItem('user_id');
        const response = await axios.patch(`http://127.0.0.1:8000/api/users/${userId}/`, formData, {
            headers: { 'Content-Type': 'multipart/form-data' }
        });
        userData.value = response.data;
    } catch (e) {
        console.error("Failed to upload image", e);
        alert("Failed to upload profile picture.");
    }
};



const updatePassword = async () => {
    if (newPassword.value !== confirmPassword.value) {
        pwError.value = "Passwords do not match.";
        return;
    }
    if (!newPassword.value) return;

    pwError.value = '';
    pwSuccess.value = '';

    try {
        const userId = localStorage.getItem('user_id');
        await axios.patch(`http://127.0.0.1:8000/api/users/${userId}/`, {
            password: newPassword.value
        });
        pwSuccess.value = "Password changed successfully!";
        newPassword.value = '';
        confirmPassword.value = '';
        setTimeout(() => pwSuccess.value = '', 3000);
    } catch (e) {
        console.error(e);
        pwError.value = "Failed to update password.";
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
                <div class="profileInfo">
                    <div class="profilePicWrapper" @click="triggerFileInput">
                        <img v-if="userData.profile_picture" :src="userData.profile_picture" class="profilePic">
                        <div v-else class="profilePic placeholder">{{ userData.username ? userData.username.charAt(0).toUpperCase() : '?' }}</div>
                        <div class="editOverlay">
                            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"></path><circle cx="12" cy="13" r="4"></circle></svg>
                        </div>
                        <input type="file" ref="fileInput" @change="handleFileChange" accept="image/*" style="display: none;">
                    </div>
                    <div>
                        <h2 class="sectionTitle">Profile Details</h2>
                        <p class="sectionSubtitle">Manage your personal account information</p>
                    </div>
                </div>
            </div>
            
            <div class="divider"></div>
            
            <div v-if="loading" class="statusMsg">Loading user data...</div>
            <div v-else-if="error" class="statusMsg error">{{ error }}</div>
            
            <div v-else class="formContainer">
                <!-- Username Field (Editable) -->
                <div class="infoGroup">
                    <label>Username (Optional)</label>
                    <div v-if="!isEditing" class="valueFieldWrapper">
                        <div class="valueField">{{ userData.username || 'Not set (using fallback name)' }}</div>
                        <button class="editBtn" @click="isEditing = true">
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path></svg>
                        </button>
                    </div>
                    <div v-else class="editFieldWrapper">
                        <input 
                            v-model="editableUsername" 
                            type="text" 
                            placeholder="Enter username" 
                            class="editInput"
                        >
                        <div class="editActions">
                            <button class="saveBtn" @click="saveUsername">Save</button>
                            <button class="cancelBtn" @click="cancelEdit">Cancel</button>
                        </div>
                    </div>
                    <p v-if="saveError" class="errorMessage">{{ saveError }}</p>
                    <p v-if="saveSuccess" class="successMessage">{{ saveSuccess }}</p>
                    <small class="helpText" v-if="isEditing">Leave empty to use First Name + Last Name as your display name.</small>
                </div>
                
                <div class="infoGroup">
                    <label>Display Name Preview</label>
                    <div class="valueField dim">{{ userData.display_username }}</div>
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

                <div class="divider"></div>

                <!-- Password Section -->
                <div class="infoGroup">
                    <label>Change Password</label>
                    <div class="row g-2">
                        <div class="col-md-6">
                            <input type="password" v-model="newPassword" placeholder="New Password" class="valueField">
                        </div>
                        <div class="col-md-6">
                            <input type="password" v-model="confirmPassword" placeholder="Confirm Password" class="valueField">
                        </div>
                    </div>
                    <div class="mt-3">
                         <button class="saveBtn" @click="updatePassword" :disabled="!newPassword">Update Password</button>
                    </div>
                    <p v-if="pwError" class="errorMessage">{{ pwError }}</p>
                    <p v-if="pwSuccess" class="successMessage">{{ pwSuccess }}</p>
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
    max-width: 850px; /* Constrain width to avoid dead space */
    margin: 0 auto;   /* Center */
    padding: 40px;
    overflow-y: auto; /* Scroll inside if content gets too long */
    
    /* Remove border radius if you want it to look like a full panel, 
       or keep it if there is padding around it in ProfilePage. 
       Based on "fill out", usually implies 0 margin. */
    border-radius: 12px;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06); 
}

/* Header Styling */
.header {
    margin-bottom: 20px;
}
.profileInfo {
    display: flex;
    align-items: center;
    gap: 20px;
}
.profilePicWrapper {
    position: relative;
    width: 80px;
    height: 80px;
    cursor: pointer;
}
.profilePic {
    width: 100%;
    height: 100%;
    border-radius: 50%;
    object-fit: cover;
    border: 3px solid var(--c-surface);
    box-shadow: 0 0 0 2px var(--c-accent);
}
.profilePic.placeholder {
    background: var(--c-accent);
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2rem;
    font-weight: bold;
}
.editOverlay {
    position: absolute;
    inset: 0;
    background: rgba(0,0,0,0.5);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    opacity: 0;
    transition: opacity 0.2s;
}
.profilePicWrapper:hover .editOverlay {
    opacity: 1;
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

.valueField.dim {
    color: var(--c-text-secondary);
    background-color: transparent;
    border: 1px dashed var(--border-color);
}

.valueField:hover {
    border-color: var(--c-text-secondary);
}

/* Edit Mode Styles */
.valueFieldWrapper {
    position: relative;
    display: flex;
    align-items: center;
}

.editBtn {
    position: absolute;
    right: 10px;
    background: none;
    border: none;
    color: var(--c-text-secondary);
    cursor: pointer;
    padding: 5px;
    border-radius: 4px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.editBtn:hover {
    background: var(--c-bg);
    color: var(--c-accent);
}

.editFieldWrapper {
    display: flex;
    gap: 10px;
}

.editInput {
    flex: 1;
    padding: 15px;
    border: 1px solid var(--c-accent);
    border-radius: 8px;
    background: var(--c-bg);
    color: var(--c-text-primary);
    font-size: 1rem;
    outline: none;
}

.editActions {
    display: flex;
    gap: 8px;
}

.saveBtn, .cancelBtn {
    padding: 12px 24px;
    border-radius: 8px;
    font-weight: 600;
    cursor: pointer;
    border: none;
}

.saveBtn {
    background: var(--c-accent);
    color: white;
}

.saveBtn:hover {
    opacity: 0.9;
}

.cancelBtn {
    background: var(--c-bg);
    border: 1px solid var(--border-color);
    color: var(--c-text-secondary);
}

.cancelBtn:hover {
    background: var(--border-color);
}

.errorMessage {
    color: #ef4444;
    font-size: 0.9rem;
    margin-top: 5px;
}

.successMessage {
    color: #22c55e;
    font-size: 0.9rem;
    margin-top: 5px;
}

.helpText {
    display: block;
    margin-top: 5px;
    font-size: 0.85rem;
    color: var(--c-text-secondary);
}
</style>