<script setup>
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';
import ListGroup from '../components/ListGroup.vue';
import CreateGroupModal from '../components/CreateGroupModal.vue';

// --- STATE ---
const groups = ref([]);
const selectedGroup = ref(null);
const groupMembers = ref([]);
const loading = ref(false);
const memberLoading = ref(false);

const leaders = computed(() => groupMembers.value.filter(m => m.role === 'leader'));
const regularMembers = computed(() => groupMembers.value.filter(m => m.role !== 'leader'));

const newMemberUsername = ref('');
const addMemberError = ref('');
const addMemberSuccess = ref('');

const showCreateModal = ref(false);

// --- API ACTIONS ---
const fetchMyGroups = async () => {
    loading.value = true;
    try {
        const currentUserId = parseInt(localStorage.getItem('user_id'));
        const response = await axios.get('http://127.0.0.1:8000/api/group-members/');
        const myMemberships = response.data.filter(item => item.user_detail.id === currentUserId);
        groups.value = myMemberships.map(item => item.group_detail);
    } catch (error) {
        console.error("Failed to load groups", error);
    } finally {
        loading.value = false;
    }
};

const selectGroup = async (group) => {
    selectedGroup.value = group;
    groupMembers.value = [];
    newMemberUsername.value = '';
    addMemberError.value = ''; 
    addMemberSuccess.value = '';
    
    memberLoading.value = true;
    try {
        const response = await axios.get(`http://127.0.0.1:8000/api/group-members/?group=${group.id}`);
        groupMembers.value = response.data;
    } catch (error) {
        console.error("Failed to load members", error);
    } finally {
        memberLoading.value = false;
    }
};

const addMember = async () => {
    if (!newMemberUsername.value.trim()) return;
    addMemberError.value = '';
    addMemberSuccess.value = '';

    try {
        const payload = { group: selectedGroup.value.id, username: newMemberUsername.value };
        const response = await axios.post('http://127.0.0.1:8000/api/group-members/', payload);
        groupMembers.value.push(response.data);
        addMemberSuccess.value = `User added!`;
        newMemberUsername.value = '';
    } catch (error) {
        if (error.response && error.response.data) {
             const data = error.response.data;
             addMemberError.value = data.detail || (data.username ? data.username[0] : "Failed to add.");
        } else {
            addMemberError.value = "Network error.";
        }
    }
};

const removeMember = async (membershipId) => {
    if(!confirm("Remove this member?")) return;
    try {
        await axios.delete(`http://127.0.0.1:8000/api/group-members/${membershipId}/`);
        groupMembers.value = groupMembers.value.filter(m => m.id !== membershipId);
        fetchMyGroups(); // Refresh list in case I removed myself
    } catch (e) { alert("Failed to remove."); }
};

const getGroupUrl = (group) => {
    if (group.imageUrl) return group.imageUrl;
    return `https://ui-avatars.com/api/?name=${encodeURIComponent(group.groupname)}&background=random&color=fff&size=128`;
};

const openCreateModal = () => {
    showCreateModal.value = true;
};

const closeCreateModal = () => {
    showCreateModal.value = false;
};

const handleGroupCreated = async (newGroup) => {
    await fetchMyGroups();
    // Fallback: If the new group is not in the list (e.g. race condition/cache), add it manually
    if (!groups.value.some(g => g.id === newGroup.id)) {
        groups.value.push(newGroup);
    }
    selectGroup(newGroup);
};

onMounted(() => {
    fetchMyGroups();
});
</script>

<template>
    <div class="groupsWrapper container-fluid">
        <div class="row h-100 g-0"> <!-- g-0 removes bootstrap gutters -->
            
            <!-- Inner Sidebar: Group List -->
            <div class="col-md-4 groupListCol">
                <h5 class="sectionTitle">My Groups</h5>
                <div v-if="loading" class="p-3 text-muted">Loading...</div>
                
                <div class="listContainer customScroll">
                    <list-group
                        v-for="group in groups"
                        :key="group.id"
                        :url="getGroupUrl(group)"
                        :name="group.groupname"
                        :isActive="selectedGroup && selectedGroup.id === group.id"
                        @click="selectGroup(group)"
                    />
                </div>
                
                <!-- Create New Group Button -->
                <button class="createGroupBtn" @click="openCreateModal">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <line x1="12" y1="5" x2="12" y2="19"></line>
                        <line x1="5" y1="12" x2="19" y2="12"></line>
                    </svg>
                    Create New Group
                </button>
            </div>

            <!-- Inner Content: Group Details -->
            <div class="col-md-8 detailsCol">
                <div v-if="!selectedGroup" class="emptyState">
                    <p>Select a group to manage details</p>
                </div>
                <div v-else class="detailsInner">
                    <div class="header">
                        <img :src="getGroupUrl(selectedGroup)" class="gImg">
                        <h3>{{ selectedGroup.groupname }}</h3>
                    </div>
                    
                    <div class="divider"></div>
                    
                    <!-- Add Member -->
                    <div class="actionBox">
                        <label>Add New Member</label>
                        <div class="inputGroup">
                            <input v-model="newMemberUsername" type="text" placeholder="Enter username..." @keyup.enter="addMember">
                            <button @click="addMember">Add</button>
                        </div>
                        <small v-if="addMemberError" class="text-danger">{{ addMemberError }}</small>
                        <small v-if="addMemberSuccess" class="text-success">{{ addMemberSuccess }}</small>
                    </div>

                    <!-- Leaders List -->
                    <div v-if="leaders.length > 0" class="mb-4">
                        <h6 class="listHeader">Leaders ({{ leaders.length }})</h6>
                        <ul class="memberList">
                            <li v-for="m in leaders" :key="m.id" class="memberItem">
                                <div class="memberInfo">
                                    <div class="avatar">{{ m.user_detail.username.charAt(0).toUpperCase() }}</div>
                                    <span>
                                        <strong>{{ m.user_detail.username }}</strong>
                                        <span class="roleBadge leader">LEADER</span>
                                    </span>
                                </div>
                                <button class="removeBtn" @click="removeMember(m.id)">Remove</button>
                            </li>
                        </ul>
                    </div>

                    <!-- Member List -->
                    <div v-if="regularMembers.length > 0">
                        <h6 class="listHeader">Members ({{ regularMembers.length }})</h6>
                        <ul class="memberList">
                            <li v-for="m in regularMembers" :key="m.id" class="memberItem">
                                <div class="memberInfo">
                                    <div class="avatar">{{ m.user_detail.username.charAt(0).toUpperCase() }}</div>
                                    <span>
                                        <strong>{{ m.user_detail.username }}</strong>
                                        <span v-if="m.role === 'moderator'" class="roleBadge moderator">MOD</span>
                                        <span v-else-if="m.role === 'operator'" class="roleBadge operator">OP</span>
                                    </span>
                                </div>
                                <button class="removeBtn" @click="removeMember(m.id)">Remove</button>
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Create Group Modal -->
        <create-group-modal 
            v-if="showCreateModal" 
            @close="closeCreateModal"
            @groupCreated="handleGroupCreated"
        />
    </div>
</template>

<style scoped>
.groupsWrapper {
    height: calc(100vh - 70px); /* Adjust for navbar height */
    /* No background here, letting it blend or using surface */
    background: var(--c-bg);
}

.groupListCol {
    background: var(--c-bg);
    border-right: 1px solid var(--border-color);
    padding: 20px 10px 20px 20px;
    display: flex;
    flex-direction: column;
    height: 100%;
}

.sectionTitle { color: var(--c-accent); font-weight: bold; margin-bottom: 20px; }

.listContainer {
    flex-grow: 1;
    overflow-y: auto;
    padding-right: 10px;
}

.detailsCol {
    padding: 0;
    background: var(--c-bg);
    height: 100%;
    overflow-y: auto;
}

.detailsInner { padding: 30px; }

.emptyState {
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--c-text-secondary);
    border: 2px dashed var(--border-color);
    margin: 20px;
    border-radius: var(--radius-md);
}

/* Header & Images */
.header { display: flex; align-items: center; margin-bottom: 20px; }
.gImg { width: 64px; height: 64px; border-radius: var(--radius-md); margin-right: 20px; object-fit: cover; }
.header h3 { color: var(--c-text-primary); margin: 0; }
.divider { height: 1px; background: var(--border-color); margin: 20px 0; }

/* Inputs & Actions */
.actionBox {
    background: var(--c-surface);
    padding: 20px;
    border-radius: var(--radius-md);
    margin-bottom: 30px;
    border: 1px solid var(--border-color);
}
.actionBox label { display: block; color: var(--c-text-primary); margin-bottom: 10px; font-size: 0.9rem; font-weight: 600; }
.inputGroup { display: flex; gap: 10px; }
.inputGroup input {
    flex: 1;
    background: var(--c-bg);
    border: 1px solid var(--border-color);
    color: var(--c-text-primary);
    padding: 10px 15px;
    border-radius: 8px;
    outline: none;
}
.inputGroup input:focus { border-color: var(--c-accent); }
.inputGroup button {
    background: var(--c-accent);
    color: white;
    border: none;
    padding: 0 20px;
    border-radius: 8px;
    cursor: pointer;
    font-weight: bold;
}
.inputGroup button:hover { opacity: 0.9; }

/* Member List */
.listHeader { color: var(--c-accent); text-transform: uppercase; font-size: 0.85rem; letter-spacing: 1.5px; margin-bottom: 15px; font-weight: 700; }
.memberList { list-style: none; padding: 0; }
.memberItem {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 14px 16px;
    background: var(--c-surface);
    border: 1px solid var(--border-color);
    margin-bottom: 10px;
    border-radius: 10px;
    transition: all 0.2s ease;
}
.memberItem:hover { transform: translateX(5px); border-color: var(--c-accent); background: rgba(249, 115, 22, 0.05); }

.memberInfo { display: flex; align-items: center; gap: 12px; }
.memberInfo span {
    color: var(--c-text-primary);
    font-size: 0.95rem;
}
.memberInfo strong {
    color: var(--c-text-primary);
    font-weight: 600;
}
.avatar {
    width: 36px; height: 36px; background: var(--c-accent); color: white;
    border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1rem; font-weight: 600;
}
.roleBadge { font-size: 0.7rem; color: white; padding: 3px 8px; border-radius: 4px; margin-left: 8px; font-weight: bold; text-transform: uppercase; }
.roleBadge.leader { background: #EAB308; } /* Yellow/Gold */
.roleBadge.moderator { background: #3B82F6; } /* Blue */
.roleBadge.operator { background: #10B981; } /* Green */

.removeBtn { background: transparent; color: var(--c-text-primary); border: 1px solid var(--border-color); padding: 6px 12px; border-radius: 6px; cursor: pointer; font-size: 0.85rem; transition: all 0.2s; }
.removeBtn:hover { color: white; background: #ef4444; border-color: #ef4444; }

/* Scrollbar fix for the list */
.customScroll::-webkit-scrollbar { width: 5px; }
.customScroll::-webkit-scrollbar-thumb { background: var(--border-color); border-radius: 10px; }

/* Create Group Button */
.createGroupBtn {
    width: 100%;
    padding: 12px 16px;
    margin-top: 12px;
    background: var(--c-accent);
    color: white;
    border: none;
    border-radius: 10px;
    font-weight: 600;
    font-size: 0.95rem;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    transition: all 0.2s ease;
}

.createGroupBtn:hover {
    opacity: 0.9;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(249, 115, 22, 0.3);
}

.createGroupBtn svg {
    flex-shrink: 0;
}
</style>
