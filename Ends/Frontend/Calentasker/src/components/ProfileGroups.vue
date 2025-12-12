<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import ListGroup from './ListGroup.vue';

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
    <div class="groupsWrapper">
        <div class="row h-100">
            <!-- Inner Sidebar: Group List -->
            <div class="col-md-4 groupListCol">
                <h5>My Groups</h5>
                <div v-if="loading">Loading...</div>
                <div class="listContainer">
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
                    Select a group to manage.
                </div>
                <div v-else>
                    <div class="header">
                        <img :src="getGroupUrl(selectedGroup)" class="gImg">
                        <h3>{{ selectedGroup.groupname }}</h3>
                    </div>
                    <hr>
                    
                    <!-- Add Member -->
                    <div class="addArea">
                        <h6>Add Member</h6>
                        <div class="d-flex gap-2">
                            <input v-model="newMemberUsername" class="form-control" placeholder="Username" @keyup.enter="addMember">
                            <button class="btn btn-dark" @click="addMember">Add</button>
                        </div>
                        <small v-if="addMemberError" class="text-danger d-block mt-1">{{ addMemberError }}</small>
                        <small v-if="addMemberSuccess" class="text-success d-block mt-1">{{ addMemberSuccess }}</small>
                    </div>

                    <!-- Member List -->
                    <h6 class="mt-4">Members ({{ groupMembers.length }})</h6>
                    <ul class="list-group list-group-flush">
                        <li v-for="m in groupMembers" :key="m.id" class="list-group-item d-flex justify-content-between align-items-center">
                            <span>
                                <strong>{{ m.user_detail.username }}</strong>
                                <span v-if="m.isAdmin" class="badge bg-secondary ms-2">Admin</span>
                            </span>
                            <button class="btn btn-sm text-danger" @click="removeMember(m.id)">&times;</button>
                        </li>
                    </ul>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.groupsWrapper {
    height: 100%;
    background: white;
    border-radius: 12px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    overflow: hidden;
}

.groupListCol {
    background: #f8f9fa;
    border-right: 1px solid #e5e7eb;
    padding: 20px;
    display: flex;
    flex-direction: column;
    max-height: 100%;
}

.listContainer {
    flex-grow: 1;
    overflow-y: auto;
}

.detailsCol {
    padding: 30px;
    overflow-y: auto;
    max-height: 100%;
}

.emptyState {
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #aaa;
}

.gImg { width: 50px; height: 50px; border-radius: 8px; margin-right: 15px; }
.header { display: flex; align-items: center; }
</style>