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
                    'isToday': day.isToday
                }"
            >
                <span v-if="!day.isEmpty">{{ day.dayNum }}</span>
                <!-- Dots Heatmap -->
                <div v-if="!day.isEmpty" class="dotContainer">
                    <div 
                        v-for="task in getDayTasks(day.dateStr).slice(0, 4)" 
                        :key="task.id" 
                        class="dot"
                    ></div>
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
    /* UPDATED: Fit content height instead of forcing 100% */
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

/* 
   GRID LAYOUT 
*/
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
    flex-direction: column; /* Allow stacking number and dots */
    
    font-size: 1.2rem;
    font-weight: 600;
    
    position: relative;
    color: var(--c-text-primary);
    border: 1px solid transparent;
    
    transition: background-color 0.2s, border-color 0.2s, box-shadow 0.2s;
    user-select: none;
}

.daySquare.empty {
    background-color: transparent;
    border: none;
    pointer-events: none;
}

.daySquare.isToday {
    box-shadow: inset 0 0 0 2px white; 
    font-weight: 800;
    color: white;
}

/* Heatmap Dots */
.dotContainer {
    position: absolute;
    bottom: 6px;
    display: flex;
    gap: 3px;
}

.dot {
    width: 4px;
    height: 4px;
    border-radius: 50%;
    background-color: var(--c-accent);
    opacity: 0.8;
}
</style>