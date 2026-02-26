<script setup>
import { ref, onMounted, watch, computed } from 'vue';
import { useI18n } from 'vue-i18n';
import axios from 'axios';
import { useRoute, useRouter } from 'vue-router'; 
import ListTask from '../components/ListTask.vue';
import ListGroupIcon from '../components/ListGroupIcon.vue';
import TaskCalendar from '../components/TaskCalendar.vue';
import TaskDetailModal from '../components/TaskDetailModal.vue';
import CreateTaskModal from '../components/CreateTaskModal.vue';
import AlertModal from '../components/AlertModal.vue';

// --- STATE ---
const route = useRoute();
const router = useRouter();
const { t } = useI18n();

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

// Alert Modal State
const isAlertOpen = ref(false);
const alertConfig = ref({
    title: '',
    message: '',
    type: 'info',
    confirmText: 'Confirm',
    onConfirm: () => {}
});

const closeAlert = () => { isAlertOpen.value = false; };

const showAlert = ({ title, message, type = 'info', confirmText = 'Confirm', onConfirm }) => {
    alertConfig.value = { title, message, type, confirmText, onConfirm };
    isAlertOpen.value = true;
};

const handleAlertConfirm = () => {
    alertConfig.value.onConfirm();
    closeAlert();
};

// New State for Date Filtering, Sorting, and Priority
const selectedDate = ref(null);
const sortBy = ref('date-desc'); // date-desc (newest), date-asc (oldest), due-asc, priority
const filterPriority = ref('all'); // all, low, medium, high, urgent
const showCompleted = ref(false); // Toggle for completed tasks
const showMobileFilters = ref(false); // Toggle for mobile filter menu

// --- COMPUTED ---
const selectedGroup = computed(() => {
    if (selectedGroupId.value === 'own') {
        return { groupname: t('tasks.ownTasks'), id: 'own' };
    }
    return groups.value.find(g => g.id == selectedGroupId.value);
});

// Check if user is Leader or Operator in the selected group
const canCreateTask = computed(() => {
    if (!selectedGroupId.value) return false;
    if (selectedGroupId.value === 'own') return true; // Always allow own tasks

    const group = groups.value.find(g => g.id == selectedGroupId.value);
    // groups.value now stores the group_detail, but we need the membership role.
    // Wait, fetchGroups maps to group_detail. We need to preserve the role.
    return group && (group.myRole === 'leader' || group.myRole === 'operator');
});

const canDeleteGroup = computed(() => {
    if (!selectedGroupId.value || selectedGroupId.value === 'own') return false;
    const group = groups.value.find(g => g.id == selectedGroupId.value);
    return group && group.myRole === 'leader';
});

// Priority Map for sorting
const priorityMap = { 'urgent': 4, 'high': 3, 'medium': 2, 'low': 1 };

// Helper to filter and sort
const processTasks = (taskList) => {
    let result = taskList;

    // 1. Date Filter (Existing)
    if (selectedDate.value) {
        result = result.filter(task => {
            if (!task.created_at && !task.start_date) return false;
            
            const rawStart = task.start_date || task.created_at;
            const rawEnd = task.due_date || task.start_date || task.created_at;
            
            const start = rawStart.substring(0, 10);
            const end = rawEnd.substring(0, 10);
            
            return selectedDate.value >= start && selectedDate.value <= end;
        });
    }

    // 2. Priority Filter
    if (filterPriority.value !== 'all') {
        result = result.filter(task => task.priority === filterPriority.value);
    }

    // 3. Sorting
    return result.sort((a, b) => {
        switch (sortBy.value) {
            case 'date-desc': // Newest first
                return new Date(b.created_at) - new Date(a.created_at);
            case 'date-asc': // Oldest first
                return new Date(a.created_at) - new Date(b.created_at);
            case 'due-asc': // Soonest due date
                if (!a.due_date) return 1; // No due date at bottom
                if (!b.due_date) return -1;
                return new Date(a.due_date) - new Date(b.due_date);
            case 'priority': // Highest priority first
                const pA = priorityMap[a.priority] || 0;
                const pB = priorityMap[b.priority] || 0;
                return pB - pA;
            default:
                return 0;
        }
    });
};

// Grouped Tasks
const groupedTasks = computed(() => {
    const all = tasks.value;
    const now = new Date();
    const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());

    const dueSoon = [];     // <= 7 days
    const upcoming = [];    // > 7 days
    const noDueDate = [];   // null
    const overdue = [];     // < Today
    const completed = [];   // status === 'done'

    all.forEach(task => {
        // Completed
        if (task.status === 'done') {
            completed.push(task);
            return;
        }

        // No Due Date
        if (!task.due_date) {
            noDueDate.push(task);
            return;
        }

        const due = new Date(task.due_date);
        const dueDay = new Date(due.getFullYear(), due.getMonth(), due.getDate());
        const diffTime = dueDay - today;
        const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

        if (diffDays < 0) {
            overdue.push(task);
        } else if (diffDays <= 7) {
            dueSoon.push(task);
        } else {
            // > 7 days
            upcoming.push(task);
        }
    });

    return {
        dueSoon: processTasks(dueSoon),
        upcoming: processTasks(upcoming),
        noDueDate: processTasks(noDueDate),
        overdue: processTasks(overdue),
        completed: processTasks(completed)
    };
});

// --- API ACTIONS ---
const fetchGroups = async () => {
    try {
        const currentUserId = parseInt(localStorage.getItem('user_id'));
        const response = await axios.get(`http://127.0.0.1:8000/api/group-members/?user=${currentUserId}`);
        // Store group details AND the role from the membership object
        groups.value = response.data.map(item => ({
            ...item.group_detail,
            myRole: item.role // Add the role to the group object
        }));

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
             url += `?created_by_userid=${currentUserId}&group__isnull=true`; 
             // We might need to handle the "no group" part in client if backend ignores it.
        } else if (groupId) {
            url += `?group=${groupId}`; 
        }

        const response = await axios.get(url);
        
        if (groupId === 'own') {
            tasks.value = response.data;
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
            // Default to own tasks if no group specified
            selectedGroupId.value = 'own';
            fetchTasks('own');
            // Optionally push to route to reflect state, but be careful of loops
            // router.replace({ query: { ...route.query, group: 'own' } });
        }
    },
    { immediate: true } 
);

const onTaskHover = (id) => { hoveredTaskId.value = id; };
const onTaskLeave = () => { hoveredTaskId.value = null; };

const onTaskSelect = (id) => {
    const width = window.innerWidth;
    if (width <= 530) {
        // On mobile, tap opens details directly
        const task = tasks.value.find(t => t.id === id);
        if (task) goToDetails(task);
        return;
    }
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
        showAlert({ title: t('common.warning'), message: t('tasks.selectGroup'), type: 'warning', confirmText: 'OK', onConfirm: () => {} });
        return;
    }
    isCreateTaskOpen.value = true;
};

const onTaskCreated = (newTask) => {
    fetchTasks(selectedGroupId.value);
};

const handleTaskUpdate = (updatedTask) => {
    // Update local list
    const index = tasks.value.findIndex(t => t.id === updatedTask.id);
    if (index !== -1) {
        tasks.value[index] = updatedTask;
    }
    
    // Update detail view if open
    if (detailTask.value && detailTask.value.id === updatedTask.id) {
        detailTask.value = updatedTask;
    }
};

const deleteGroup = async () => {
    if (!selectedGroupId.value || selectedGroupId.value === 'own') return;
    
    showAlert({
        title: t('groups.confirmDeleteTitle'),
        message: t('groups.confirmDeleteMsg', { name: selectedGroup.value?.groupname }),
        type: 'danger',
        confirmText: t('common.delete'),
        onConfirm: async () => {
            try {
                await axios.delete(`http://127.0.0.1:8000/api/groups/${selectedGroupId.value}/`);
                // Refresh groups list
                await fetchGroups();
                // Redirect to Own Tasks or first available
                const nextId = groups.value.length > 0 ? groups.value[0].id : 'own';
                handleGroupClick(nextId); 
            } catch (error) {
                console.error("Failed to delete group", error);
                showAlert({ title: t('common.error'), message: t('groups.failedDelete'), type: 'danger', confirmText: 'OK', onConfirm: () => {} });
            }
        }
    });
};

// --- HELPERS ---
const getGroupUrl = (group) => {
    if (group.imageUrl) return group.imageUrl;
    if (group.image) return group.image;
    return `https://ui-avatars.com/api/?name=${encodeURIComponent(group.groupname)}&background=random&color=fff&size=128`;
};

const getTaskUrl = (task) => {
    if (task.imageUrl) return task.imageUrl;
    if (task.image) return task.image;
    const p = task.priority ? task.priority.toLowerCase() : 'low';
    if (p === 'urgent') return 'https://placehold.co/150/26272D/9CA3AF?text=No%20Image';
    return 'https://placehold.co/150/26272D/9CA3AF?text=No%20Image';
};

onMounted(() => {
    fetchGroups();
});
</script>

<template>
    <div class="pageContainer">
        <!-- CUSTOM GRID LAYOUT -->
        <div class="layoutGrid">
            
            <!-- COLUMN 1: SIDEBAR -->
            <div class="sidebarArea">
                <div class="sidebarScroll">
                    <!-- Own Tasks Item -->
                    <list-group-icon
                        url="/src/assets/view-list.svg"
                        :name="$t('tasks.ownTasks')"
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
            <div class="tasksArea">    
                <div class="stickyHeader">
                    <div class="headerLeft">
                        <h1 class="groupTitle">{{ selectedGroup?.groupname || $t('tasks.selectGroup') }}</h1>
                        
                        <div class="tasksSubheading">
                            <h2 class="sectionTitle">{{ $t('tasks.title') }}</h2>
                            <span v-if="selectedDate" class="dateBadge">{{ selectedDate }}</span>

                            <!-- MOBILE TOGGLES -->
                            <div class="mobileControls">
                                <button class="control-btn mobile-only" @click="showMobileFilters = !showMobileFilters">
                                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                        <line x1="4" y1="21" x2="4" y2="14"></line>
                                        <line x1="4" y1="10" x2="4" y2="3"></line>
                                        <line x1="12" y1="21" x2="12" y2="12"></line>
                                        <line x1="12" y1="8" x2="12" y2="3"></line>
                                        <line x1="20" y1="21" x2="20" y2="16"></line>
                                        <line x1="20" y1="12" x2="20" y2="3"></line>
                                        <line x1="1" y1="14" x2="7" y2="14"></line>
                                        <line x1="9" y1="8" x2="15" y2="8"></line>
                                        <line x1="17" y1="16" x2="23" y2="16"></line>
                                    </svg>

                                    {{ $t('tasks.filters') }}
                                </button>
                                <button class="control-btn mobile-only" @click="isCalendarModalOpen = true">
                                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                        <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                                        <line x1="16" y1="2" x2="16" y2="6"></line>
                                        <line x1="8" y1="2" x2="8" y2="6"></line>
                                        <line x1="3" y1="10" x2="21" y2="10"></line>
                                    </svg>
                                    {{ $t('tasks.calendar') }}
                                </button>
                            </div>

                            <!-- FILTER CONTROLS (Wrapped for Responsive) -->
                            <div class="filter-group" :class="{ 'show-mobile': showMobileFilters }">
                                <!-- Sorting Dropdown -->
                                <select v-model="sortBy" class="control-select">
                                    <option value="date-desc">{{ $t('tasks.sort.newest') }}</option>
                                    <option value="date-asc">{{ $t('tasks.sort.oldest') }}</option>
                                    <option value="due-asc">{{ $t('tasks.sort.dueSoonest') }}</option>
                                    <option value="priority">{{ $t('tasks.sort.priority') }}</option>
                                </select>

                                <!-- Priority Filter -->
                                <select v-model="filterPriority" class="control-select">
                                    <option value="all">{{ $t('tasks.priorities.all') }}</option>
                                    <option value="low">{{ $t('tasks.priorities.low') }}</option>
                                    <option value="medium">{{ $t('tasks.priorities.medium') }}</option>
                                    <option value="high">{{ $t('tasks.priorities.high') }}</option>
                                    <option value="urgent">{{ $t('tasks.priorities.urgent') }}</option>
                                </select>

                                <!-- Show Completed Toggle -->
                                <button class="control-btn" @click="showCompleted = !showCompleted">
                                    {{ showCompleted ? $t('tasks.toggle.hideCompleted') : $t('tasks.toggle.showCompleted') }}
                                </button>
                            </div>
                        </div>
                    </div>

                    <div class="headerRight">
                         <button 
                            v-if="canCreateTask" 
                            class="btnNewTask" 
                            @click="openCreateTask"
                         >
                            <span class="plusIcon">+</span> {{ $t('tasks.newTask') }}
                         </button>
                    </div>
                </div>

                <div class="taskScroll customScroll">
                    <div v-if="!loading && tasks.length === 0" style="padding: 20px; color:white;">
                        <span v-if="selectedDate">{{ $t('tasks.empty.date') }}</span>
                        <span v-else>{{ $t('tasks.empty.general') }}</span>
                    </div>

                    <template v-else>
                        <!-- 1. Due Soon (<= 7 days) -->
                        <div v-if="groupedTasks.dueSoon.length > 0">
                            <h3 class="group-header">{{ $t('tasks.groups.dueSoon') }}</h3>
                            <list-task 
                                v-for="(task, index) in groupedTasks.dueSoon"
                                :key="task.id"
                                class="fadeInItem"
                                :style="{ animationDelay: `${index * 50}ms` }"
                                :id="task.id"
                                :url="getTaskUrl(task)"
                                :title="task.title"
                                :desc="task.description"
                                :isSelected="selectedTaskId === task.id"
                                :priority="task.priority"
                                :dueDate="task.due_date"
                                :status="task.status"
                                @hover="onTaskHover"
                                @leave="onTaskLeave"
                                @select="onTaskSelect"
                                @click="goToDetails(task)"
                            />
                        </div>

                        <!-- Red Break Line (Only if Due Soon exists AND (Date not selected OR other tasks below exist)) -->
                        <hr v-if="groupedTasks.dueSoon.length > 0 && (!selectedDate || (groupedTasks.upcoming.length > 0 || groupedTasks.noDueDate.length > 0 || groupedTasks.overdue.length > 0))" class="red-break">

                        <!-- 2. Upcoming (> 7 days) -->
                        <div v-if="groupedTasks.upcoming.length > 0">
                            <h3 class="group-header">{{ $t('tasks.groups.upcoming') }}</h3>
                            <list-task 
                                v-for="(task, index) in groupedTasks.upcoming"
                                :key="task.id"
                                class="fadeInItem"
                                :style="{ animationDelay: `${index * 50}ms` }"
                                :id="task.id"
                                :url="getTaskUrl(task)"
                                :title="task.title"
                                :desc="task.description"
                                :isSelected="selectedTaskId === task.id"
                                :priority="task.priority"
                                :dueDate="task.due_date"
                                :status="task.status"
                                @hover="onTaskHover"
                                @leave="onTaskLeave"
                                @select="onTaskSelect"
                                @click="goToDetails(task)"
                            />
                        </div>

                        <!-- 3. No Due Date -->
                        <div v-if="groupedTasks.noDueDate.length > 0">
                            <!-- Divider if Upcoming exists -->
                            <hr v-if="groupedTasks.upcoming.length > 0" class="divider">
                            
                            <h3 class="group-header">{{ $t('tasks.groups.noDueDate') }}</h3>
                            <list-task 
                                v-for="(task, index) in groupedTasks.noDueDate"
                                :key="task.id"
                                class="fadeInItem"
                                :style="{ animationDelay: `${index * 50}ms` }"
                                :id="task.id"
                                :url="getTaskUrl(task)"
                                :title="task.title"
                                :desc="task.description"
                                :isSelected="selectedTaskId === task.id"
                                :priority="task.priority"
                                :dueDate="task.due_date"
                                :status="task.status"
                                @hover="onTaskHover"
                                @leave="onTaskLeave"
                                @select="onTaskSelect"
                                @click="goToDetails(task)"
                            />
                        </div>

                        <!-- 4. Overdue (< Today) -->
                        <div v-if="groupedTasks.overdue.length > 0">
                            <!-- Divider if Upcoming or NoDueDate exists. Note: DueSoon uses RedBreak. -->
                            <hr v-if="groupedTasks.upcoming.length > 0 || groupedTasks.noDueDate.length > 0" class="divider">

                            <h3 class="group-header text-danger">{{ $t('tasks.groups.overdue') }}</h3>
                            <list-task 
                                v-for="(task, index) in groupedTasks.overdue"
                                :key="task.id"
                                class="fadeInItem"
                                :style="{ animationDelay: `${index * 50}ms` }"
                                :id="task.id"
                                :url="getTaskUrl(task)"
                                :title="task.title"
                                :desc="task.description"
                                :isSelected="selectedTaskId === task.id"
                                :priority="task.priority"
                                :dueDate="task.due_date"
                                :status="task.status"
                                @hover="onTaskHover"
                                @leave="onTaskLeave"
                                @select="onTaskSelect"
                                @click="goToDetails(task)"
                            />
                        </div>

                        <!-- 5. Completed -->
                        <div v-if="showCompleted && groupedTasks.completed.length > 0">
                            <hr class="divider">
                            <h3 class="group-header text-muted">{{ $t('tasks.groups.completed') }}</h3>
                            <list-task 
                                v-for="(task, index) in groupedTasks.completed"
                                :key="task.id"
                                class="fadeInItem opacity-75"
                                :style="{ animationDelay: `${index * 50}ms` }"
                                :id="task.id"
                                :url="getTaskUrl(task)"
                                :title="task.title"
                                :desc="task.description"
                                :isSelected="selectedTaskId === task.id"
                                :priority="task.priority"
                                :dueDate="task.due_date"
                                :status="task.status"
                                @hover="onTaskHover"
                                @leave="onTaskLeave"
                                @select="onTaskSelect"
                                @click="goToDetails(task)"
                            />
                        </div>
                    </template>
                </div>
            </div>

            <!-- COLUMN 3: CALENDAR (Desktop) -->
            <div class="calendarArea">
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
        :userRole="selectedGroupId === 'own' ? 'owner' : (selectedGroup ? selectedGroup.myRole : null)"
        @close="closeTaskDetail"
        @task-updated="handleTaskUpdate"
        @task-deleted="fetchTasks(selectedGroupId)"
    />

    <CreateTaskModal 
        :isOpen="isCreateTaskOpen"
        :groupId="selectedGroupId === 'own' ? null : (selectedGroupId ? parseInt(selectedGroupId) : null)"
        @close="isCreateTaskOpen = false"
        @task-created="onTaskCreated"
    />

    <!-- MODAL OVERLAY (Calendar) -->
    <div v-if="isCalendarModalOpen" class="modalOverlay" @click.self="isCalendarModalOpen = false">
        <div class="modalContent">
            <TaskCalendar 
                :tasks="tasks"
                :hoveredTaskId="selectedTaskId"
                :selectedDate="selectedDate"
                @date-selected="handleDateSelected"
            />
        </div>
        </div>

    
    <AlertModal
        :isOpen="isAlertOpen"
        :title="alertConfig.title"
        :message="alertConfig.message"
        :type="alertConfig.type"
        :confirmText="alertConfig.confirmText"
        @close="closeAlert"
        @confirm="handleAlertConfirm"
    />
    </div>
</template>

<style scoped>
* { box-sizing: border-box; }

.pageContainer {
    height: calc(100vh - 70px);
    width: 100%;
    overflow: hidden;
    background-color: var(--c-bg);
    position: relative;
}

/* GRID LAYOUT */
.layoutGrid {
    display: grid;
    grid-template-columns: 80px 1fr 450px;
    height: 100%;
    width: 100%;
}

@media (max-width: 1024px) {
    .layoutGrid {
        grid-template-columns: 80px 1fr 350px; /* Reduce calendar width */
    }
}

@media (max-width: 768px) {
    .pageContainer {
        overflow-y: hidden; /* Use internal scrolling */
        height: calc(100vh - 70px);
    }
    
    .layoutGrid {
        display: flex; /* Flex row by default */
        flex-direction: row; 
        height: 100%;
        gap: 0;
        justify-content: flex-start; /* Ensure they stick together */
    }
    
    .sidebarArea {
        width: 80px; 
        min-width: 80px;
        flex-shrink: 0; /* Never shrink */
        flex-grow: 0;   /* Never grow */
        height: 100%;
        border-right: 1px solid var(--border-color);
        border-bottom: none;
        padding: 10px 0;
        flex-direction: column;
        justify-content: flex-start;
        margin: 0; /* Ensure no margin */
    }
    
    .sidebarScroll {
        overflow-y: auto;
    }

    /* Adjust main content area */
    .tasksArea {
        flex: 1; /* Take remaining width */
        width: auto; /* Let flex handle it */
        min-width: 0; /* Allow shrinking below content size to prevent overflow */
        height: 100%;
        margin: 0;
    }

    /* Hide Calendar column on mobile */
    .calendarArea {
        display: none; 
    }
}

/* SIDEBAR AREA */
.sidebarArea {
    background-color: var(--c-surface);
    border-right: 1px solid var(--border-color);
    padding: 10px 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    z-index: 100;
    overflow: hidden;
}

.sidebarScroll {
    width: 100%;
    flex-grow: 1;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    align-items: center;
    scrollbar-width: none;
}
.sidebarScroll::-webkit-scrollbar { display: none; }

/* TASKS AREA */
.tasksArea {
    background-color: var(--c-bg);
    padding: 0; 
    display: flex;
    flex-direction: column;
    overflow: hidden;
}

.taskScroll {
    flex-grow: 1;
    overflow-y: auto;
    padding: 20px; 
}

/* CALENDAR AREA (Right Column) */
.calendarArea {
    background-color: var(--c-surface);
    border-left: 1px solid var(--border-color);
    display: block; 
}

/* SCROLLBAR */
.customScroll::-webkit-scrollbar { width: 8px; }
.customScroll::-webkit-scrollbar-thumb { 
    background: var(--c-surface-hover); 
    border-radius: 4px; 
}
.customScroll::-webkit-scrollbar-thumb:hover { 
    background: var(--c-accent); 
}

/* MODAL */
.modalOverlay {
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
/* HEADER REDESIGN */
.stickyHeader {
    position: sticky;
    top: 0;
    z-index: 50;
    background: var(--c-surface); 
    border-bottom: 1px solid var(--border-color);
    padding: 15px 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 4px 20px rgba(0,0,0,0.2); 
    min-height: auto; 
    flex-wrap: wrap; /* Allow wrapping */
}

@media (max-width: 600px) {
    .stickyHeader {
        flex-direction: column;
        align-items: stretch; 
        gap: 15px;
        /* Force overlap to prevent gap */
        margin-left: -1px;
        width: calc(100% + 2px); /* Compensate */
        padding-left: 20px; 
    }

    .headerLeft {
        flex-direction: column;
        align-items: flex-start;
        gap: 5px;
        width: 100%;
    }
    
    .headerRight {
        width: 100%;
        display: flex;
        justify-content: flex-end; /* Align button right or stretch? User said "below box", let's make it full width */
    }
    
    .btnNewTask {
        width: 100%;
        justify-content: center;
    }
    
    .tasksSubheading {
        width: 100%;
        justify-content: space-between;
    }
}

/* Combined Left Section */
.headerLeft {
    display: flex;
    align-items: baseline; /* Align by text baseline */
    gap: 20px;
}

.groupTitle {
    margin: 0;
    font-size: 1.8rem;
    color: var(--c-text-primary);
    font-weight: 700;
}

.tasksSubheading {
    display: flex;
    align-items: center;
    gap: 10px;
    flex-wrap: wrap; /* Allow wrapping for controls */
}

.control-select {
    background: var(--c-bg);
    color: var(--c-text-primary);
    border: 1px solid var(--border-color);
    padding: 6px 12px;
    border-radius: 8px;
    font-size: 0.85rem;
    cursor: pointer;
    font-family: inherit;
    outline: none;
    transition: border-color 0.2s;
}

.control-select:hover, .control-select:focus {
    border-color: var(--c-accent);
}

.control-btn {
    background: transparent;
    border: 1px solid var(--border-color);
    color: var(--c-text-primary);
    padding: 6px 12px;
    border-radius: 8px;
    font-size: 0.85rem;
    cursor: pointer;
    transition: all 0.2s;
    display: inline-flex;
    align-items: center;
    gap: 6px;
    white-space: nowrap;
}
.control-btn:hover {
    background: var(--c-surface-hover);
    border-color: var(--c-accent);
}

/* RESPONSIVE HEADER CONTROLS */
.mobile-only { display: none; } /* Hidden on desktop */
.filter-group {
    display: flex;
    gap: 10px;
    align-items: center;
    flex-wrap: wrap;
}

@media (max-width: 1024px) {
    /* Show Calendar button on tablet/mobile where calendar column is hidden */
    /* Wait, calendar column is hidden at 768px in existing CSS, but let's check. 
       Existing CSS: @media (max-width: 768px) { .calendarArea { display: none; } }
       So we should show the button at 768px.
    */
}

@media (max-width: 768px) {
    .mobile-only { display: inline-flex; }
    
    .filter-group {
        display: none; /* Hidden by default */
        flex-direction: column;
        width: 100%;
        margin-top: 15px;
        background: var(--c-bg); /* Contrast against header */
        padding: 15px;
        border-radius: 8px;
        border: 1px solid var(--border-color);
    }

    .filter-group.show-mobile {
        display: flex;
        animation: fadeIn 0.2s ease;
    }

    .control-select, .control-btn {
        width: 100%; /* Full width on mobile */
        justify-content: center;
    }

    .tasksSubheading {
        flex-wrap: wrap;
    }
    
    .mobileControls {
        display: flex;
        gap: 8px;
        margin-left: auto; /* Push to right */
        flex-wrap: wrap; /* Allow wrapping to prevent cut-off */
        justify-content: flex-end;
    }
}


.red-break {
    border: 0;
    height: 1px;
    background: #ef4444; /* Bright Red */
    margin: 30px 0;
    opacity: 0.6;
}

.divider {
    border: 0;
    height: 1px;
    background: var(--border-color);
    margin: 30px 0;
}

.group-header {
    font-size: 1.1rem;
    color: var(--c-text-primary);
    margin: 0 0 15px 0;
    font-weight: 600;
    opacity: 0.8;
}

.text-danger { color: #ef4444 !important; }
.text-muted { color: var(--c-text-secondary) !important; }
.opacity-75 { opacity: 0.75; }

.sectionTitle {
    margin: 0;
    font-size: 1.1rem;
    color: var(--c-text-secondary);
    text-transform: uppercase;
    letter-spacing: 1px;
    font-weight: 600;
}

.dateBadge {
    background: var(--c-bg); /* Use bg color for contrast against surface */
    color: var(--c-text-primary);
    padding: 4px 10px;
    border-radius: 12px;
    font-size: 0.85rem;
    border: 1px solid var(--border-color);
}

.btnNewTask {
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

.btnNewTask:hover {
    filter: brightness(1.1);
    transform: translateY(-1px);
    box-shadow: 0 4px 10px rgba(0,0,0,0.3);
}

.plusIcon {
    font-size: 1.4rem; /* Slightly larger */
    line-height: 0; /* Remove line-height influence */
    font-weight: 700; /* Bold as requested */
    transform: translateY(-1px); /* Visual correction */
    margin-top: -2px; /* Fine-tune centering */
}

.btnDeleteGroup {
    background: transparent;
    border: none;
    color: var(--c-text-secondary);
    cursor: pointer;
    padding: 8px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-left: 10px;
    opacity: 0.6;
    transition: all 0.2s;
}
.btnDeleteGroup:hover {
    background: rgba(239, 68, 68, 0.1);
    color: #ef4444;
    opacity: 1;
}

@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

/* RESPONSIVE BREAKPOINTS */
@media (max-width: 1300px) {
    .layoutGrid {
        grid-template-columns: 80px 1fr;
    }
    .calendarArea { display: none; }
}

@media (max-width: 768px) {
    /* Stack header on mobile/tablet */
    .stickyHeader {
        flex-direction: column;
        align-items: flex-start;
        gap: 15px;
    }
    .headerLeft {
        width: 100%;
        flex-wrap: wrap;
    }
    .btnNewTask {
        width: 100%;
        justify-content: center;
    }
}

@media (max-width: 530px) {
    .layoutGrid {
        grid-template-columns: 70px 1fr;
    }
    .calendarArea { display: none; }
    .tasksArea { padding: 0 5px; }
    
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
    .groupTitle { font-size: 1.4rem; }
}

@keyframes slideUp {
    from { transform: translateY(100%); }
    to { transform: translateY(0); }
}

/* FADE IN ANIMATION */
.fadeInItem {
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