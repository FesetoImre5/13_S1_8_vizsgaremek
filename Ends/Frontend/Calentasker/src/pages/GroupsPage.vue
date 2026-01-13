<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import ListGroup from '../components/ListGroup.vue';

// --- STATE ---
const groups = ref([]);
const selectedGroup = ref(null);
const groupMembers = ref([]);
const loading = ref(false);
const memberLoading = ref(false);

const newMemberUsername = ref('');
const addMemberError = ref('');
const addMemberSuccess = ref('');

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
                    <!-- Note: ListGroup component needs styling update too -->
                    <list-group
                        v-for="group in groups"
                        :key="group.id"
                        :url="getGroupUrl(group)"
                        :name="group.groupname"
                        :isActive="selectedGroup && selectedGroup.id === group.id"
                        @click="selectGroup(group)"
                    />
                </div>
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

                    <!-- Member List -->
                    <h6 class="listHeader">Members ({{ groupMembers.length }})</h6>
                    <ul class="memberList">
                        <li v-for="m in groupMembers" :key="m.id" class="memberItem">
                            <div class="memberInfo">
                                <div class="avatar">{{ m.user_detail.username.charAt(0) }}</div>
                                <span>
                                    <strong>{{ m.user_detail.username }}</strong>
                                    <span v-if="m.isAdmin" class="adminBadge">ADMIN</span>
                                </span>
                            </div>
                            <button class="removeBtn" @click="removeMember(m.id)">Remove</button>
                        </li>
                    </ul>
                </div>
            </div>
        </div>
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
.actionBox label { display: block; color: var(--c-text-secondary); margin-bottom: 10px; font-size: 0.9rem; }
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
.listHeader { color: var(--c-text-secondary); text-transform: uppercase; font-size: 0.8rem; letter-spacing: 1px; margin-bottom: 15px; }
.memberList { list-style: none; padding: 0; }
.memberItem {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px;
    background: var(--c-surface);
    border: 1px solid var(--border-color);
    margin-bottom: 10px;
    border-radius: 10px;
    transition: transform 0.1s;
}
.memberItem:hover { transform: translateX(5px); border-color: var(--c-text-secondary); }

.memberInfo { display: flex; align-items: center; gap: 12px; }
.avatar {
    width: 32px; height: 32px; background: var(--c-primary); color: white;
    border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 0.9rem;
}
.adminBadge { font-size: 0.7rem; background: var(--c-accent); color: black; padding: 2px 6px; border-radius: 4px; margin-left: 8px; font-weight: bold; }
.removeBtn { background: transparent; color: var(--c-text-secondary); border: none; cursor: pointer; font-size: 0.9rem; }
.removeBtn:hover { color: var(--c-primary); text-decoration: underline; }

/* Scrollbar fix for the list */
.customScroll::-webkit-scrollbar { width: 5px; }
.customScroll::-webkit-scrollbar-thumb { background: var(--border-color); border-radius: 10px; }
</style>
