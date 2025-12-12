<script setup>
import { ref, watch } from 'vue';
import { useRouter, useRoute } from 'vue-router'; // 1. Import useRoute
import { useAuth } from '../composables/UseAuth';
import ProfileDetails from '../components/ProfileDetails.vue';
import ProfileGroups from '../components/ProfileGroups.vue';

const { logout } = useAuth();
const router = useRouter();
const route = useRoute(); // 2. Get current route

// 3. State defaults to 'details'
const activeTab = ref('details'); 

// 4. Watch for URL changes (handles initial load AND navigation from UserMenu)
watch(
    () => route.query.tab, 
    (newTab) => {
        // If query is 'groups', switch to groups. Otherwise default to details.
        activeTab.value = newTab === 'groups' ? 'groups' : 'details';
    },
    { immediate: true } // Run immediately when page loads
);

// 5. Helper to switch tabs by updating the URL
const switchTab = (tabName) => {
    router.push({ query: { tab: tabName } });
};

const handleLogout = () => {
    logout();
    router.push('/auth');
};
</script>

<template>
    <div class="profileContainer container-fluid">
        <div class="row fullHeight">
            <!-- LEFT SIDEBAR -->
            <div class="col-md-3 col-lg-2 sidebar">
                <div class="sidebarMenu">
                    <button class="sidebarBtn" :class="{ 'active': activeTab === 'details' }" @click="switchTab('details')">
                        Profile Details
                    </button>
                    <button class="sidebarBtn" :class="{ 'active': activeTab === 'groups' }" @click="switchTab('groups')">
                        Groups
                    </button>
                    <div class="divider"></div>
                    <button class="sidebarBtn logout" @click="handleLogout">
                        Log out
                    </button>
                </div>
            </div>

            <!-- RIGHT CONTENT AREA -->
            <div class="col-md-9 col-lg-10 contentArea">
                <transition name="fade" mode="out-in">
                    <keep-alive>
                        <component :is="activeTab === 'details' ? ProfileDetails : ProfileGroups" />
                    </keep-alive>
                </transition>
            </div>
        </div>
    </div>
</template>

<style scoped>
.profileContainer {
    height: calc(100vh - 70px);
    background-color: var(--c-bg); /* Dark background */
    padding: 0;
    overflow: hidden;
}

.fullHeight { height: 100%; }

.sidebar {
    background-color: var(--c-surface); /* Dark Gray Surface */
    border-right: 1px solid var(--border-color);
    padding: 20px;
    display: flex;
    flex-direction: column;
}

.sidebarMenu {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.sidebarBtn {
    text-align: left;
    background: transparent;
    border: 1px solid transparent;
    padding: 12px 20px;
    border-radius: var(--radius-md);
    color: var(--c-text-secondary);
    font-weight: 500;
    font-size: 0.95rem;
    transition: all 0.2s ease;
    cursor: pointer;
}

.sidebarBtn:hover {
    background-color: var(--c-surface-hover);
    color: var(--c-text-primary);
}

.sidebarBtn.active {
    background-color: rgba(249, 115, 22, 0.1); /* Low opacity orange */
    color: var(--c-accent);
    border: 1px solid var(--c-accent);
    font-weight: bold;
}

.sidebarBtn.logout { color: var(--c-primary); } /* Red-Orange */
.sidebarBtn.logout:hover { 
    background-color: rgba(220, 38, 38, 0.1);
    border-color: var(--c-primary); 
}

.divider {
    height: 1px;
    background-color: var(--border-color);
    margin: 15px 0;
}

.contentArea {
    padding: 0; /* Let children handle padding */
    height: 100%;
    background-color: var(--c-bg);
}

/* Animations */
.fade-enter-active, .fade-leave-active { transition: opacity 0.2s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>