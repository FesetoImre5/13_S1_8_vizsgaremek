<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
import { useAuth } from '../composables/UseAuth';

const { logout } = useAuth();
const router = useRouter();

// State
const userData = ref(null);
const loading = ref(true);
const error = ref('');

// Fetch Data
const fetchUserProfile = async () => {
    try {
        const userId = localStorage.getItem('user_id');
        if (!userId) {
            throw new Error("User ID not found locally.");
        }

        const response = await axios.get(`http://127.0.0.1:8000/api/users/${userId}/`);
        userData.value = response.data;
        console.log("User Data Loaded:", userData.value);

    } catch (err) {
        console.error(err);
        error.value = "Failed to load user data.";
    } finally {
        loading.value = false;
    }
};

const handleLogout = () => {
    logout();
    router.push('/auth');
};

onMounted(() => {
    fetchUserProfile();
});
</script>

<template>
    <div class="profileContainer container-fluid">
        <div class="row fullHeight">
            
            <!-- LEFT SIDEBAR -->
            <!-- Bootstrap cols kept as kebab-case -->
            <div class="col-md-3 col-lg-2 sidebar">
                <div class="sidebarMenu">
                    <!-- Profile Button (Active) -->
                    <button class="sidebarBtn active">
                        Profile Details
                    </button>

                    <!-- Groups Button -->
                    <button class="sidebarBtn">
                        Groups
                    </button>

                    <div class="divider"></div>

                    <!-- Log Out Button -->
                    <button class="sidebarBtn logout" @click="handleLogout">
                        Log out
                    </button>
                </div>
            </div>

            <!-- RIGHT CONTENT AREA (Empty for now) -->
            <div class="col-md-9 col-lg-10 contentArea">
                <div class="emptyWorkspace">
                    <!-- Data is loaded in 'userData' variable -->
                    <p v-if="loading">Loading user data...</p>
                    <p v-if="error" class="text-danger">{{ error }}</p>
                </div>
            </div>
            
        </div>
    </div>
</template>

<style scoped>
.profileContainer {
    /* Accounts for the 70px Fixed Navbar */
    height: calc(100vh - 70px);
    background-color: #f8f9fa; 
    padding: 0;
    overflow: hidden;
}

.fullHeight {
    height: 100%;
}

/* --- SIDEBAR STYLES --- */
.sidebar {
    background-color: white;
    border-right: 1px solid #e5e7eb;
    padding: 20px;
    display: flex;
    flex-direction: column;
}

.sidebarMenu {
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.sidebarBtn {
    text-align: left;
    background: transparent;
    border: none;
    padding: 12px 20px;
    border-radius: 8px;
    color: #4b5563;
    font-weight: 500;
    font-size: 1rem;
    transition: all 0.2s ease;
    width: 100%;
}

.sidebarBtn:hover {
    background-color: #f3f4f6;
    color: orangered; /* Accent color */
}

.sidebarBtn.active {
    background-color: #fff0eb; 
    color: orangered;
    font-weight: bold;
    border-left: 4px solid orangered;
}

.sidebarBtn.logout {
    color: #dc2626; 
}

.sidebarBtn.logout:hover {
    background-color: #fee2e2;
}

.divider {
    height: 1px;
    background-color: #e5e7eb;
    margin: 10px 0;
}

/* --- CONTENT AREA --- */
.contentArea {
    padding: 40px;
    overflow-y: auto; 
}

.emptyWorkspace {
    width: 100%;
    height: 100%;
    /* Visual guide for the empty div */
    border: 2px dashed #e5e7eb; 
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #9ca3af;
}
</style>