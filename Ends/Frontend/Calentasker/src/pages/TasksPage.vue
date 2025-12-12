<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import ListTask from '../components/ListTask.vue';
import ListGroup from '../components/ListGroup.vue';
import TaskCalendar from '../components/TaskCalendar.vue';

// --- STATE ---
// Removed "isSidebarExpanded" as we are now using a fixed "Discord-style" sidebar
const groups = ref([]);
const tasks = ref([]);
const loading = ref(false);
const selectedGroupId = ref(null);
const hoveredTaskId = ref(null);

// --- API ACTIONS (Unchanged) ---
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
        if (groupId) url += `?group=${groupId}`; 
        const response = await axios.get(url);
        tasks.value = response.data;
    } catch (error) {
        console.error("Failed to load tasks", error);
    } finally {
        loading.value = false;
    }
};

// --- INTERACTION ---
const handleGroupClick = (groupId) => {
    if (selectedGroupId.value === groupId) {
        selectedGroupId.value = null;
        fetchTasks();
    } else {
        selectedGroupId.value = groupId;
        fetchTasks(groupId);
    }
};

const onTaskHover = (id) => { hoveredTaskId.value = id; };
const onTaskLeave = () => { hoveredTaskId.value = null; };

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

onMounted(() => {
    fetchGroups();
    fetchTasks(); 
});
</script>

<template>
    <div>
        <div class="container-fluid pageWrapper">
            <div class="row">
                <!-- SIDEBAR COLUMN: Fixed narrow width -->
                <div class="col-auto sidebarCol">
                    <div class="sidebarScroll">
                        <list-group
                            v-for="group in groups"
                            :key="group.id"
                            :url="getGroupUrl(group)"
                            :name="group.groupname"
                            :isActive="selectedGroupId === group.id"
                            @click="handleGroupClick(group.id)"
                        />
                    </div>
                </div>

                <!-- MAIN CONTENT -->
                <div class="col mainContentCol">    
                    <div class="taskList customScroll">
                        <div v-if="loading" class="p-3 text-white">Loading tasks...</div>
                        <div v-else-if="tasks.length === 0" class="p-3 text-white">No tasks found.</div>

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

                <!-- RIGHT COLUMN (Calendar) -->
                <div class="col-sm-4 p-0 d-none d-md-block" style="background-color: var(--c-surface);">
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
    width: 80px !important; /* Fixed width like Discord */
    background-color: var(--c-surface);
    border-right: 1px solid var(--border-color);
    padding: 10px 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    height: calc(100vh - 70px);
    z-index: 100; /* Ensure tooltip goes over content */
}

.sidebarScroll {
    width: 100%;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    align-items: center;
    /* Hide scrollbar */
    scrollbar-width: none; 
}
.sidebarScroll::-webkit-scrollbar { display: none; }

.mainContentCol {
    background-color: var(--c-bg);
    padding: 0 20px;
}

.taskList {
    height: calc(100vh - 70px);
    overflow-y: auto;
    padding-bottom: 20px;
    padding-top: 20px;
}

/* Custom Scrollbar for task list */
.customScroll::-webkit-scrollbar { width: 8px; }
.customScroll::-webkit-scrollbar-thumb { background: var(--c-surface-hover); border-radius: 4px; }

@media (max-width: 768px) {
    /* On mobile, keep sidebar small or hide/show via other means. 
       For now, 80px fits icons comfortably. */
    .sidebarCol { width: 70px !important; }
}
</style>