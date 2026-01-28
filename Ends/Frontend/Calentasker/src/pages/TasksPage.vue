<script setup>
import { ref, onMounted, watch, computed } from 'vue';
import axios from 'axios';
import { useRoute, useRouter } from 'vue-router'; 
import ListTask from '../components/ListTask.vue';
import ListGroupIcon from '../components/ListGroupIcon.vue';
import TaskCalendar from '../components/TaskCalendar.vue';
import TaskDetailModal from '../components/TaskDetailModal.vue';
import CreateTaskModal from '../components/CreateTaskModal.vue';

// --- STATE ---
const route = useRoute();
const router = useRouter();

const groups = ref([]);
const tasks = ref([]);
const loading = ref(false);

const selectedGroupId = ref(null);
const hoveredTaskId = ref(null);
const selectedTaskId = ref(null);
const isCalendarModalOpen = ref(false);

// Task Detail Modal State
const isTaskDetailOpen = ref(false);
const detailTask = ref(null);

// Create Task Modal State
const isCreateTaskOpen = ref(false);

// New State for Date Filtering
const selectedDate = ref(null);

// --- COMPUTED ---
const selectedGroup = computed(() => {
    if (selectedGroupId.value === 'own') {
        return { groupname: 'Own Tasks', id: 'own' };
    }
    return groups.value.find(g => g.id == selectedGroupId.value);
});

// Filtered Tasks
const filteredTasks = computed(() => {
    if (!selectedDate.value) return tasks.value;
    
    return tasks.value.filter(task => {
        if (!task.created_at && !task.start_date) return false;
        
        const rawStart = task.start_date || task.created_at;
        const rawEnd = task.due_date || task.start_date || task.created_at;
        
        const start = rawStart.substring(0, 10);
        const end = rawEnd.substring(0, 10);
        
        return selectedDate.value >= start && selectedDate.value <= end;
    });
});

// --- API ACTIONS ---
const fetchGroups = async () => {
    try {
        const currentUserId = parseInt(localStorage.getItem('user_id'));
        const response = await axios.get(`http://127.0.0.1:8000/api/group-members/?user=${currentUserId}`);
        groups.value = response.data.map(item => item.group_detail);

        // Logic to default to something if needed, but 'own' might be default if route says so
        if (!route.query.group && groups.value.length > 0) {
             // Maybe default to Own tasks? Or first group. Keeping first group for now.
             handleGroupClick(groups.value[0].id);
        }
    } catch (error) {
        console.error("Failed to load groups", error);
    }
};

const fetchTasks = async (groupId = null) => {
    loading.value = true;
    tasks.value = []; // Clear current tasks to avoid confusion

    try {
        let url = 'http://127.0.0.1:8000/api/tasks/';
        const currentUserId = parseInt(localStorage.getItem('user_id'));

        if (groupId === 'own') {
             // Fetch tasks created by user with NO group (Personal Tasks)
             // Assuming backend supports simple filtering. 
             // If backend is standard DRF: ?created_by_userid=<id>&group__isnull=true
             // We'll try a custom filter approach or assume 'assigned_to'.
             // User request: "Own Tasks is a place where the user can create tasks for themselves."
             // This strongly implies personal tasks.
             
             // Strategy: Get all tasks and filter client side if backend is limited, 
             // BUT ideally backend filter. Let's try to pass a query.
             // Since I can't easily change backend right now without checking views, 
             // I will try to fetch specific user tasks.
             // Note: The previous code just fetched /tasks/?group=ID.
             
             // OPTION 1: Filter by creator and no group.
             url += `?created_by_userid=${currentUserId}`; 
             // We might need to handle the "no group" part in client if backend ignores it.
        } else if (groupId) {
            url += `?group=${groupId}`; 
        }

        const response = await axios.get(url);
        
        if (groupId === 'own') {
            // Client-side filter to ensure we show only personal tasks (no group)
            // or we could show ALL tasks assigned to user?
            // "Own Tasks is a place where the user can create tasks for themselves" -> Personal Tasks.
            tasks.value = response.data.filter(t => t.created_by_userid === currentUserId && !t.group);
        } else {
            tasks.value = response.data;
        }

    } catch (error) {
        console.error("Failed to load tasks", error);
    } finally {
        loading.value = false;
    }
};

// --- INTERACTION ---
const handleGroupClick = (groupId) => {
    // If clicking the same group/own, do nothing? Or refresh? 
    // Always push handling to watch
    router.push({ query: { ...route.query, group: groupId } });
};

watch(
    () => route.query.group,
    (newGroupId) => {
        if (newGroupId) {
            selectedGroupId.value = newGroupId;
            fetchTasks(newGroupId);
        } else {
            selectedGroupId.value = null;
        }
    },
    { immediate: true } 
);

const onTaskHover = (id) => { hoveredTaskId.value = id; };
const onTaskLeave = () => { hoveredTaskId.value = null; };

const onTaskSelect = (id) => {
    const width = window.innerWidth;
    if (width <= 530) return;
    if (width > 530 && width <= 1300) {
        selectedTaskId.value = id;
        isCalendarModalOpen.value = true;
    }
    if (width > 1300) {
        selectedTaskId.value = (selectedTaskId.value === id) ? null : id;
    }
};

const handleDateSelected = (dateStr) => {
    selectedDate.value = (selectedDate.value === dateStr) ? null : dateStr;
};

const toggleCalendarModal = () => {
    isCalendarModalOpen.value = !isCalendarModalOpen.value;
};

const goToDetails = (task) => { 
    console.log("Details clicked for task:", task); 
    detailTask.value = task;
    isTaskDetailOpen.value = true;
};

const closeTaskDetail = () => {
    isTaskDetailOpen.value = false;
    detailTask.value = null;
};

const openCreateTask = () => {
    if (!selectedGroupId.value) {
        alert("Please select a group or 'Own Tasks' first.");
        return;
    }
    isCreateTaskOpen.value = true;
};

const onTaskCreated = (newTask) => {
    fetchTasks(selectedGroupId.value);
};

// --- HELPERS ---
const getGroupUrl = (group) => {
    if (group.imageUrl) return group.imageUrl;
    if (group.image) return group.image;
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
});
</script>

<template>
    <div class="page-container">
        <!-- CUSTOM GRID LAYOUT -->
        <div class="layout-grid">
            
            <!-- COLUMN 1: SIDEBAR -->
            <div class="sidebar-area">
                <div class="sidebar-scroll">
                    <!-- Own Tasks Item -->
                    <list-group-icon
                        url="/src/assets/view-list.svg"
                        name="Own Tasks"
                        :isActive="selectedGroupId === 'own'"
                        :isSystemIcon="true"
                        @click="handleGroupClick('own')"
                        style="margin-bottom: 20px; border-bottom: 1px solid var(--border-color); padding-bottom: 10px;"
                    />

                    <list-group-icon
                        v-for="group in groups"
                        :key="group.id"
                        :url="getGroupUrl(group)"
                        :name="group.groupname"
                        :isActive="selectedGroupId == group.id"
                        @click="handleGroupClick(group.id)"
                    />
                </div>
            </div>

            <!-- COLUMN 2: TASKS -->
            <div class="tasks-area">    
                <div class="stickyHeader">
                    <div class="header-left">
                        <h1 class="group-title">{{ selectedGroup?.groupname || 'Select a Group' }}</h1>
                        <div class="tasks-subheading">
                            <h2 class="section-title">Tasks</h2>
                            <span v-if="selectedDate" class="date-badge">{{ selectedDate }}</span>
                        </div>
                    </div>

                    <div class="header-right">
                         <button class="btn-new-task" @click="openCreateTask">
                            <span class="plus-icon">+</span> New Task
                         </button>
                    </div>
                </div>

                <div class="task-scroll custom-scroll">
                    <div v-if="loading" style="padding: 20px;">
                        <div class="skeleton" style="height: 100px; width: 100%; margin-bottom: 15px;"></div>
                        <div class="skeleton" style="height: 100px; width: 100%; margin-bottom: 15px;"></div>
                        <div class="skeleton" style="height: 100px; width: 100%; margin-bottom: 15px;"></div>
                    </div>
                    <div v-else-if="filteredTasks.length === 0" style="padding: 20px; color:white;">
                        <span v-if="selectedDate">No tasks for this date.</span>
                        <span v-else>No tasks found.</span>
                    </div>

                    <list-task 
                        v-else
                        v-for="(task, index) in filteredTasks"
                        :key="task.id"
                        class="fade-in-item"
                        :style="{ animationDelay: `${index * 50}ms` }"
                        :id="task.id"
                        :url="getTaskUrl(task)"
                        :title="task.title"
                        :desc="task.description"
                        :isSelected="selectedTaskId === task.id"
                        :priority="task.priority"
                        :dueDate="task.due_date"
                        @hover="onTaskHover"
                        @leave="onTaskLeave"
                        @select="onTaskSelect"
                        @click="goToDetails(task)"
                    />
                </div>
            </div>

            <!-- COLUMN 3: CALENDAR (Desktop) -->
            <div class="calendar-area">
                <TaskCalendar 
                    :tasks="tasks"
                    :hoveredTaskId="hoveredTaskId"
                    :selectedDate="selectedDate"
                    @date-selected="handleDateSelected"
                />
            </div>
        </div>

    <TaskDetailModal 
        :isOpen="isTaskDetailOpen"
        :task="detailTask"
        @close="closeTaskDetail"
        @task-updated="fetchTasks(selectedGroupId)"
    />

    <CreateTaskModal 
        :isOpen="isCreateTaskOpen"
        :groupId="selectedGroupId === 'own' ? null : (selectedGroupId ? parseInt(selectedGroupId) : null)"
        @close="isCreateTaskOpen = false"
        @task-created="onTaskCreated"
    />

    <!-- MODAL OVERLAY (Calendar) -->
    <div v-if="isCalendarModalOpen" class="modal-overlay" @click.self="isCalendarModalOpen = false">
        <div class="modalContent">
            <TaskCalendar 
                :tasks="tasks"
                :hoveredTaskId="selectedTaskId"
                :selectedDate="selectedDate"
                @date-selected="handleDateSelected"
            />
        </div>
    </div>
    </div>
</template>

<style scoped>
* { box-sizing: border-box; }

.page-container {
    height: calc(100vh - 70px);
    width: 100%;
    overflow: hidden;
    background-color: var(--c-bg);
    position: relative;
}

/* GRID LAYOUT */
.layout-grid {
    display: grid;
    grid-template-columns: 80px 1fr 450px;
    height: 100%;
    width: 100%;
}

/* SIDEBAR AREA */
.sidebar-area {
    background-color: var(--c-surface);
    border-right: 1px solid var(--border-color);
    padding: 10px 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    z-index: 100;
}

.sidebar-scroll {
    width: 100%;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    align-items: center;
    scrollbar-width: none;
}
.sidebar-scroll::-webkit-scrollbar { display: none; }

/* TASKS AREA */
.tasks-area {
    background-color: var(--c-bg);
    padding: 0; 
    display: flex;
    flex-direction: column;
    overflow: hidden;
}

.task-scroll {
    flex-grow: 1;
    overflow-y: auto;
    padding: 20px; 
}

/* CALENDAR AREA (Right Column) */
.calendar-area {
    background-color: var(--c-surface);
    border-left: 1px solid var(--border-color);
    display: block; 
}

/* SCROLLBAR */
.custom-scroll::-webkit-scrollbar { width: 8px; }
.custom-scroll::-webkit-scrollbar-thumb { 
    background: var(--c-surface-hover); 
    border-radius: 4px; 
}
.custom-scroll::-webkit-scrollbar-thumb:hover { 
    background: var(--c-accent); 
}

/* MODAL */
.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background-color: rgba(0, 0, 0, 0.85);
    backdrop-filter: blur(5px);
    z-index: 1100;
    display: flex;
    align-items: center;
    justify-content: center;
    animation: fadeIn 0.2s ease;
}

.modalContent {
    width: 90%;
    max-width: 900px;
    height: auto;
    max-height: 90vh; /* Safety limit */
    
    background-color: var(--c-surface);
    border-radius: 15px;
    padding: 0; 
    box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    border: 1px solid var(--border-color);
    overflow: hidden;
}

/* HEADER REDESIGN */
.stickyHeader {
    position: sticky;
    top: 0;
    z-index: 50;
    background: var(--c-surface); /* Lighter background as requested */
    border-bottom: 1px solid var(--border-color);
    padding: 20px 30px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 4px 20px rgba(0,0,0,0.2); /* Added shadow for better separation */
}

/* Combined Left Section */
.header-left {
    display: flex;
    align-items: baseline; /* Align by text baseline */
    gap: 20px;
}

.group-title {
    margin: 0;
    font-size: 1.8rem;
    color: var(--c-text-primary);
    font-weight: 700;
}

.tasks-subheading {
    display: flex;
    align-items: center;
    gap: 10px;
}

.section-title {
    margin: 0;
    font-size: 1.1rem;
    color: var(--c-text-secondary);
    text-transform: uppercase;
    letter-spacing: 1px;
    font-weight: 600;
}

.date-badge {
    background: var(--c-bg); /* Use bg color for contrast against surface */
    color: var(--c-text-primary);
    padding: 4px 10px;
    border-radius: 12px;
    font-size: 0.85rem;
    border: 1px solid var(--border-color);
}

.btn-new-task {
    background: var(--c-accent);
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 8px;
    font-weight: 600;
    font-size: 0.95rem;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 8px;
    transition: all 0.2s ease;
    box-shadow: 0 2px 5px rgba(0,0,0,0.2);
}

.btn-new-task:hover {
    filter: brightness(1.1);
    transform: translateY(-1px);
    box-shadow: 0 4px 10px rgba(0,0,0,0.3);
}

.plus-icon {
    font-size: 1.2rem;
    line-height: 1;
    font-weight: bold;
}

@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

/* RESPONSIVE BREAKPOINTS */
@media (max-width: 1300px) {
    .layout-grid {
        grid-template-columns: 80px 1fr;
    }
    .calendar-area { display: none; }
}

@media (max-width: 768px) {
    /* Stack header on mobile/tablet */
    .stickyHeader {
        flex-direction: column;
        align-items: flex-start;
        gap: 15px;
    }
    .header-left {
        width: 100%;
        flex-wrap: wrap;
    }
    .btn-new-task {
        width: 100%;
        justify-content: center;
    }
}

@media (max-width: 530px) {
    .layout-grid {
        grid-template-columns: 70px 1fr;
    }
    .calendar-area { display: none; }
    .tasks-area { padding: 0 5px; }
    
    .modalContent {
        width: 100%;
        height: auto;
        max-height: 85vh;
        border-radius: 24px 24px 0 0; /* Round top only */
        position: fixed;
        bottom: 0;
        top: auto;
        border-bottom: none;
        animation: slideUp 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }
    
    .stickyHeader {
        padding: 15px;
    }
    .group-title { font-size: 1.4rem; }
}

@keyframes slideUp {
    from { transform: translateY(100%); }
    to { transform: translateY(0); }
}

/* FADE IN ANIMATION */
.fade-in-item {
    opacity: 0;
    animation: fadeInTask 0.4s ease forwards;
}

@keyframes fadeInTask {
    from { 
        opacity: 0; 
        transform: translateY(10px); 
    }
    to { 
        opacity: 1; 
        transform: translateY(0); 
    }
}
</style>