<script setup>
import { computed, ref } from 'vue';

const props = defineProps({
    tasks: {
        type: Array,
        default: () => []
    },
    hoveredTaskId: {
        type: [Number, String, null],
        default: null
    },
    selectedDate: {
        type: String,
        default: null
    }
});

const emit = defineEmits(['date-selected']);

const currentDate = new Date();
const currentYear = currentDate.getFullYear();
const currentMonth = currentDate.getMonth();

const monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
const daysOfWeek = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];

// Helper: Format to "YYYY-MM-DD"
const formatDate = (date) => {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
};

const todayStr = formatDate(new Date());

const calendarDays = computed(() => {
    const days = [];
    const firstDay = new Date(currentYear, currentMonth, 1).getDay();
    const daysInMonth = new Date(currentYear, currentMonth + 1, 0).getDate();

    for (let i = 0; i < firstDay; i++) {
        days.push({ id: `pad-${i}`, isEmpty: true });
    }

    for (let i = 1; i <= daysInMonth; i++) {
        const dateObj = new Date(currentYear, currentMonth, i);
        const dateString = formatDate(dateObj);
        
        days.push({
            id: i,
            dayNum: i,
            isEmpty: false,
            dateStr: dateString,
            isToday: dateString === todayStr 
        });
    }
    return days;
});

const getDayTasks = (dateStr) => {
    return props.tasks.filter(task => {
        if (!task.created_at && !task.start_date) return false;
        const rawStart = task.start_date || task.created_at;
        const rawEnd = task.due_date || task.start_date || task.created_at;
        const start = rawStart.substring(0, 10);
        const end = rawEnd.substring(0, 10);
        return dateStr >= start && dateStr <= end;
    });
};

const handleDayClick = (day) => {
    if (day.isEmpty) return;
    emit('date-selected', day.dateStr);
};
</script>

<template>
    <div class="calendarContainer">
        <div class="calendarHeader">
            <h3>{{ monthNames[currentMonth] }} {{ currentYear }}</h3>
        </div>

        <div class="calendarGrid">
            <!-- Headers -->
            <div v-for="day in daysOfWeek" :key="day" class="weekday">{{ day }}</div>
            
            <!-- Days -->
            <div 
                v-for="day in calendarDays" 
                :key="day.id"
                class="daySquare"
                :class="{ 
                    'empty': day.isEmpty,
                    'isToday': day.isToday,
                    'hasTasks': !day.isEmpty && getDayTasks(day.dateStr).length > 0,
                    'isSelected': day.dateStr === selectedDate
                }"
                @click="handleDayClick(day)"
            >
                <span v-if="!day.isEmpty" class="dayNum">{{ day.dayNum }}</span>
                
                <!-- Tooltip -->
                <div v-if="!day.isEmpty && getDayTasks(day.dateStr).length > 0" class="taskTooltip">
                    {{ getDayTasks(day.dateStr).length }} Tasks
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
* {
    box-sizing: border-box;
}

.calendarContainer {
    background-color: var(--c-surface);
    padding: 20px;
    height: fit-content;
    width: 100%;
    display: flex;
    flex-direction: column;
}

.calendarHeader {
    margin-bottom: 20px;
    display: flex;
    justify-content: center;
}

.calendarHeader h3 {
    text-align: center;
    font-size: 1.8rem;
    color: var(--c-accent);
    font-weight: 800;
    margin: 0;
    letter-spacing: 1px;
}

/* GRID LAYOUT */
.calendarGrid {
    display: grid;
    grid-template-columns: repeat(7, 1fr);
    gap: 8px; 
    width: 100%;
    max-width: 600px; 
    margin: 0 auto;
}

.weekday {
    text-align: center;
    font-size: 1rem;
    color: var(--c-text-secondary);
    margin-bottom: 8px;
    text-transform: uppercase;
    font-weight: bold;
    letter-spacing: 1px;
}

.daySquare {
    aspect-ratio: 1/1;
    background-color: #333; 
    border-radius: 8px; 
    
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    
    font-size: 1.2rem;
    font-weight: 600;
    
    position: relative;
    color: var(--c-text-primary);
    border: 1px solid transparent;
    
    transition: all 0.2s;
    user-select: none;
    cursor: pointer;
}

.daySquare.empty {
    background-color: transparent;
    border: none;
    pointer-events: none;
    cursor: default;
}

.daySquare:hover:not(.empty) {
    background-color: var(--c-surface-hover);
}

.daySquare.isToday {
    box-shadow: inset 0 0 0 2px white; 
    font-weight: 800;
    color: white;
}

.daySquare.isSelected {
    background-color: rgba(249, 115, 22, 0.2);
    border: 1px solid var(--c-accent);
}

/* Orange Underline (Inset Shadow) for tasks */
.daySquare.hasTasks {
    box-shadow: inset 0 -4px 0 0 var(--c-accent);
}
.daySquare.hasTasks.isToday {
    /* Combine both shadows if today has tasks */
    box-shadow: inset 0 0 0 2px white, inset 0 -4px 0 0 var(--c-accent);
}

/* Tooltip */
.taskTooltip {
    position: absolute;
    bottom: 110%;
    left: 50%;
    transform: translateX(-50%);
    background-color: #000;
    color: #fff;
    padding: 5px 10px;
    border-radius: 4px;
    font-size: 0.8rem;
    white-space: nowrap;
    opacity: 0;
    pointer-events: none;
    transition: opacity 0.2s;
    z-index: 10;
    box-shadow: 0 2px 5px rgba(0,0,0,0.3);
}

.taskTooltip::after {
    content: '';
    position: absolute;
    top: 100%;
    left: 50%;
    margin-left: -5px;
    border-width: 5px;
    border-style: solid;
    border-color: #000 transparent transparent transparent;
}

.daySquare:hover .taskTooltip {
    opacity: 1;
}
</style>