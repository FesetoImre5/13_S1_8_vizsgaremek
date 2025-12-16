<script setup>
import { ref, onMounted, watch } from 'vue';
import axios from 'axios';
import { useRoute, useRouter } from 'vue-router'; 
import ListTask from '../components/ListTask.vue';
import ListGroup from '../components/ListGroup.vue';
import TaskCalendar from '../components/TaskCalendar.vue';

// --- STATE ---
const route = useRoute();
const router = useRouter();

const groups = ref([]);
const tasks = ref([]);
const loading = ref(false);
const selectedGroupId = ref(null);
const hoveredTaskId = ref(null);

// --- API ACTIONS ---

const fetchGroups = async () => {
    try {
        const currentUserId = parseInt(localStorage.getItem('user_id'));
        const response = await axios.get('http://127.0.0.1:8000/api/group-members/');
        const myMemberships = response.data.filter(item => item.user_detail.id === currentUserId);
        groups.value = myMemberships.map(item => item.group_detail);

        // --- FIX 1: AUTO-SELECT FIRST GROUP ---
        // If there are groups, and NO group is currently selected in the URL...
        if (groups.value.length > 0 && !route.query.group) {
            // ...select the first one automatically.
            handleGroupClick(groups.value[0].id);
        }

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
    // Note: We intentionally allow clicking the same group again to keep it selected
    // or switch to a new one. We only clear if you want a specific "deselect" feature,
    // but usually, in this layout, one group is always active.
    
    router.push({ query: { ...route.query, group: groupId } });
};

// Watch URL changes
watch(
    () => route.query.group,
    (newGroupId) => {
        // If URL has an ID, use it.
        if (newGroupId) {
            selectedGroupId.value = newGroupId;
            fetchTasks(newGroupId);
        } 
        // If URL is empty, we handle that in fetchGroups (initial load) 
        // or let it sit empty if you prefer.
        else {
            selectedGroupId.value = null;
            // Optional: If you want to show ALL tasks when nothing is selected:
            // fetchTasks(null); 
        }
    },
    { immediate: true } 
);

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
});
</script>

<template>
    <div>
        <div class="container-fluid pageWrapper">
            <!-- 
                FIX 2: Added 'full-height-row' class to ensure 
                the columns stretch to the bottom 
            -->
            <div class="row full-height-row">
                
                <!-- SIDEBAR COLUMN -->
                <div class="col-auto sidebarCol">
                    <div class="sidebarScroll">
                        <list-group
                            v-for="group in groups"
                            :key="group.id"
                            :url="getGroupUrl(group)"
                            :name="group.groupname"
                            :isActive="selectedGroupId == group.id"
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
                <!-- Added specific background class here to ensure full height color -->
                <div class="col-sm-4 p-0 d-none d-md-block calendarCol">
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
/* FIX 2: Layout Structure */

/* 1. Define the viewport height minus navbar */
.pageWrapper {
    height: calc(100vh - 70px);
    overflow: hidden;
    padding: 0;
    margin: 0;
    background-color: var(--c-bg);
}

/* 2. Force the Bootstrap row to take full height */
.full-height-row {
    height: 100%;
    margin: 0; /* remove default negative margins */
}

/* --- SIDEBAR --- */
.sidebarCol {
    width: 80px !important;
    background-color: var(--c-surface); /* Background applied to column */
    border-right: 1px solid var(--border-color);
    padding: 10px 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    height: 100%; /* Fill the row */
    z-index: 100;
}

.sidebarScroll {
    width: 100%;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    align-items: center;
    scrollbar-width: none; 
}
.sidebarScroll::-webkit-scrollbar { display: none; }

/* --- MAIN CONTENT --- */
.mainContentCol {
    background-color: var(--c-bg); /* Background applied to column */
    padding: 0 20px;
    height: 100%; /* Fill the row */
    display: flex;
    flex-direction: column;
}

.taskList {
    flex-grow: 1; /* Take available space */
    overflow-y: auto;
    padding-bottom: 20px;
    padding-top: 20px;
    height: 100%;
}

/* --- CALENDAR COLUMN --- */
.calendarCol {
    background-color: var(--c-surface); /* Background applied to column */
    height: 100%; /* Fill the row */
    border-left: 1px solid var(--border-color);
    overflow: hidden; /* Calendar component handles its own scrolling if needed */
}

/* Custom Scrollbar */
.customScroll::-webkit-scrollbar { width: 8px; }
.customScroll::-webkit-scrollbar-thumb { 
    background: var(--c-surface-hover); 
    border-radius: 4px; 
}
.customScroll::-webkit-scrollbar-thumb:hover { 
    background: var(--c-accent); 
}

/* --- RESPONSIVE --- */
@media (max-width: 768px) {
    .sidebarCol { width: 70px !important; }
    .mainContentCol { padding: 0 10px; }
}
</style>