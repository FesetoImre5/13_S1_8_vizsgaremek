<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import ListTask from '../components/ListTask.vue';
import ListGroup from '../components/ListGroup.vue';
import TaskCalendar from '../components/TaskCalendar.vue'; // 1. Import

// State
const isSidebarExpanded = ref(false);
const groups = ref([]);
const tasks = ref([]);
const loading = ref(false);
const selectedGroupId = ref(null);

// 2. State for Hover Logic
const hoveredTaskId = ref(null);

// --- API ACTIONS ---

const fetchGroups = async () => {
    try {
        const currentUserId = parseInt(localStorage.getItem('user_id'));
        const response = await axios.get('http://127.0.0.1:8000/api/group-members/');
        const myMemberships = response.data.filter(item => item.user_detail.id === currentUserId);
        groups.value = myMemberships.map(item => item.group_detail);
    } catch (error) {
        console.error("Failed to load groups", error);
    }
};

const fetchTasks = async (groupId = null) => {
    loading.value = true;
    try {
        let url = 'http://127.0.0.1:8000/api/tasks/';
        if (groupId) {
            url += `?group=${groupId}`; 
        }
        const response = await axios.get(url);
        tasks.value = response.data;
    } catch (error) {
        console.error("Failed to load tasks", error);
    } finally {
        loading.value = false;
    }
};

// --- INTERACTION ---

const toggleSidebar = () => { isSidebarExpanded.value = !isSidebarExpanded.value; };

const handleGroupClick = (groupId) => {
    if (selectedGroupId.value === groupId) {
        selectedGroupId.value = null;
        fetchTasks();
    } else {
        selectedGroupId.value = groupId;
        fetchTasks(groupId);
    }
};

// 3. Hover Handlers
const onTaskHover = (id) => { hoveredTaskId.value = id; };
const onTaskLeave = () => { hoveredTaskId.value = null; };

// --- HELPERS ---

const getGroupUrl = (group) => {
    if (group.imageUrl) return group.imageUrl;
    return `https://ui-avatars.com/api/?name=${encodeURIComponent(group.groupname)}&background=random&color=fff&size=128`;
};

const getTaskUrl = (task) => {
    if (task.imageUrl) return task.imageUrl;
    const p = task.priority ? task.priority.toLowerCase() : 'low';
    if (p === 'urgent') return 'https://placehold.co/150/dc2626/white?text=Urgent';
    return 'https://placehold.co/150/gray/white?text=Task';
};

// --- INIT ---
onMounted(() => {
    fetchGroups();
    fetchTasks(); 
});
</script>

<template>
    <div>
        <div class="container-fluid pageWrapper">
            <div class="row">
                <!-- SIDEBAR COLUMN -->
                <div 
                    class="col-auto sidebarCol" 
                    :style="{ width: isSidebarExpanded ? '250px' : '80px' }"
                >
                    <button class="toggleBtn" @click="toggleSidebar">#</button>

                    <list-group
                        v-for="group in groups"
                        :key="group.id"
                        :url="getGroupUrl(group)"
                        :name="group.groupname"
                        :isActive="selectedGroupId === group.id"
                        @click="handleGroupClick(group.id)"
                    />
                </div>

                <!-- MAIN CONTENT -->
                <div class="col" style="background-color: blue;">    
                    <div class="taskList">
                        <div v-if="loading" class="text-white p-3">Loading tasks...</div>
                        <div v-else-if="tasks.length === 0" class="text-white p-3">No tasks found.</div>

                        <!-- 
                            4. Pass ID and Listen for Hover events 
                        -->
                        <list-task 
                            v-else
                            v-for="task in tasks"
                            :key="task.id"
                            :id="task.id"
                            :url="getTaskUrl(task)"
                            :title="task.title"
                            :desc="task.description"
                            @hover="onTaskHover"
                            @leave="onTaskLeave"
                        />
                    </div>
                </div>

                <!-- 
                    5. RIGHT COLUMN (Calendar) 
                    Replaced the green div with TaskCalendar
                -->
                <div class="col-sm-4 p-0" style="background-color: #2a2a2a;">
                    <TaskCalendar 
                        :tasks="tasks"
                        :hoveredTaskId="hoveredTaskId"
                    />
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.sidebarCol {
    background-color: red;
    transition: width 0.3s ease;
    padding: 10px;
    display: flex;
    flex-direction: column;
    align-items: center;
    overflow: hidden; 
}

.toggleBtn {
    width: 40px;
    height: 40px;
    margin-bottom: 10px;
    border-radius: 50%;
    border: none;
    background-color: #333;
    color: white;
    font-weight: bold;
    cursor: pointer;
    font-size: 1.2rem;
    flex-shrink: 0;
}
.toggleBtn:hover {
    background-color: #444;
}

.taskList {
    height: calc(100vh - 70px);
    overflow-y: auto;
    padding-bottom: 20px;
}

@media (max-width: 700px) {
    .toggleBtn { display: none; }
    .sidebarCol { width: 80px !important; }
}
</style>