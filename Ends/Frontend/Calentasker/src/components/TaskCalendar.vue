<script setup>
import { computed } from 'vue';

const props = defineProps({
    tasks: {
        type: Array,
        default: () => []
    },
    hoveredTaskId: {
        type: [Number, String, null],
        default: null
    }
});

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

const getDayStatus = (dateStr) => {
    let dayHasTask = false;       
    let dayIsHovered = false;     
    const isHoveringAny = props.hoveredTaskId !== null;

    for (const task of props.tasks) {
        if (!task.created_at && !task.start_date) continue;

        const rawStart = task.start_date || task.created_at;
        const rawEnd = task.due_date || task.start_date || task.created_at;

        const start = rawStart.substring(0, 10);
        const end = rawEnd.substring(0, 10);

        if (dateStr >= start && dateStr <= end) {
            dayHasTask = true;
            if (props.hoveredTaskId === task.id) {
                dayIsHovered = true;
            }
        }
    }

    return {
        isHighlighted: dayIsHovered, 
        hasOrangeLine: dayHasTask && !isHoveringAny 
    };
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
                    'lineOrange': !day.isEmpty && getDayStatus(day.dateStr).hasOrangeLine,
                    'highlighted': !day.isEmpty && getDayStatus(day.dateStr).isHighlighted
                }"
            >
                <span v-if="!day.isEmpty">{{ day.dayNum }}</span>
            </div>
        </div>
    </div>
</template>

<style scoped>
.calendarContainer {
    background-color: var(--c-surface);
    padding: 20px;
    height: 100%;
    /* Flex to allow centering the grid vertically if needed */
    display: flex;
    flex-direction: column;
}

.calendarHeader h3 {
    text-align: center;
    margin-bottom: 20px;
    font-size: 1.5rem;
    color: var(--c-accent);
    font-weight: bold;
}

/* 
   GRID LAYOUT & BREAKPOINTS 
   This grid uses 'repeat(7, 1fr)' but the boxes won't grow infinitely 
   because we constrain the Width of the container in steps.
*/
.calendarGrid {
    display: grid;
    grid-template-columns: repeat(7, 1fr);
    gap: 8px;
    
    /* Center the grid horizontally */
    margin: 0 auto;
    width: 100%;
    
    /* 1. Base Size (Mobile/Small Tablets) */
    max-width: 300px; 
}

/* 2. Medium Screen Breakpoint */
@media (min-width: 1200px) {
    .calendarGrid {
        max-width: 380px; 
    }
}

/* 3. Large Screen Breakpoint */
@media (min-width: 1600px) {
    .calendarGrid {
        max-width: 450px; 
    }
}

.weekday {
    text-align: center;
    font-size: 0.85rem;
    color: var(--c-text-secondary);
    margin-bottom: 5px;
    text-transform: uppercase;
    font-weight: bold;
}

.daySquare {
    aspect-ratio: 1/1;
    background-color: #333; 
    border-radius: 6px;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 0.9rem;
    position: relative;
    color: var(--c-text-primary);
    
    border-bottom: 4px solid #222; 
    transition: background-color 0.2s, border-color 0.2s, box-shadow 0.2s;
    /* REMOVED: transform transition to stop expanding size */
}

.daySquare.empty {
    background-color: transparent;
    border-bottom: none;
    pointer-events: none;
}

/* --- STATE 1: TODAY (Standard) --- */
.daySquare.isToday {
    /* Thin white border */
    box-shadow: inset 0 0 0 2px white; 
    font-weight: bold;
    color: white;
}

/* --- STATE 2: TASK EXISTS (Not Hovered) --- */
.daySquare.lineOrange {
    border-bottom-color: var(--c-accent);
}

/* --- STATE 3: HOVERED TASK --- */
.daySquare.highlighted {
    background-color: var(--c-accent);      
    border-bottom-color: var(--c-primary); 
    color: white;
    font-weight: bold;
    /* REMOVED: transform: scale(1.1) */
}

/* --- STATE 4: HOVERED TASK + IS TODAY (The specific request) --- */
/* This specific combo needs to make the white border thicker */
.daySquare.highlighted.isToday {
    /* 
       1. Highlighted background (Orange)
       2. Thicker White Inset Border (4px)
    */
    background-color: var(--c-accent);
    box-shadow: inset 0 0 0 4px white; 
}
</style>