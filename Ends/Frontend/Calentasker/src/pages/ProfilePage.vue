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
                    
                    <!-- 6. Update buttons to use switchTab -->
                    <button 
                        class="sidebarBtn" 
                        :class="{ 'active': activeTab === 'details' }"
                        @click="switchTab('details')"
                    >
                        Profile Details
                    </button>

                    <button 
                        class="sidebarBtn" 
                        :class="{ 'active': activeTab === 'groups' }"
                        @click="switchTab('groups')"
                    >
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
                        <component 
                            :is="activeTab === 'details' ? ProfileDetails : ProfileGroups" 
                        />
                    </keep-alive>
                </transition>
            </div>
            
        </div>
    </div>
</template>

<style scoped>
/* (Keep your existing styles) */
.profileContainer {
    height: calc(100vh - 70px);
    background-color: #f3f4f6; 
    padding: 0;
    overflow: hidden;
}

.fullHeight { height: 100%; }

.sidebar {
    background-color: white;
    border-right: 1px solid #e5e7eb;
    padding: 20px;
    display: flex;
    flex-direction: column;
    z-index: 10;
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
    cursor: pointer;
}

.sidebarBtn:hover {
    background-color: #f3f4f6;
    color: orangered;
}

.sidebarBtn.active {
    background-color: #fff0eb; 
    color: orangered;
    font-weight: bold;
    border-left: 4px solid orangered;
}

.sidebarBtn.logout { color: #dc2626; }
.sidebarBtn.logout:hover { background-color: #fee2e2; }

.divider {
    height: 1px;
    background-color: #e5e7eb;
    margin: 10px 0;
}

.contentArea {
    padding: 30px;
    overflow: hidden; 
    height: 100%;
}

.fade-enter-active, .fade-leave-active { transition: opacity 0.2s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>