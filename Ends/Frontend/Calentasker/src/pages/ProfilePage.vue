<script setup>
import { useRouter } from 'vue-router'; 
import { useAuth } from '../composables/UseAuth';
import ProfileDetails from '../components/ProfileDetails.vue';

const { logout } = useAuth();
const router = useRouter();

const handleLogout = () => {
    logout();
    router.push('/auth');
};
</script>

<template>
    <div class="profileContainer container-fluid">
        <div class="row fullHeight justify-content-center">
            <!-- RIGHT CONTENT AREA (Now Full Width/Centered) -->
            <div class="col-md-10 col-lg-8 contentArea">
                <ProfileDetails />
            </div>
        </div>
    </div>
</template>

<style scoped>
.profileContainer {
    height: calc(100vh - 70px);
    background-color: var(--c-bg); /* Dark background */
    padding: 20px;
    overflow-y: auto;
}

.fullHeight { height: 100%; }

.contentArea {
    padding: 0; /* Let children handle padding */
    height: auto;
    background-color: transparent; 
}
</style>