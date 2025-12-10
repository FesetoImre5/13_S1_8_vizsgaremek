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

        <div class="calendarGrid headers">
            <div v-for="day in daysOfWeek" :key="day" class="weekday">{{ day }}</div>
        </div>

        <div class="calendarGrid body">
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
    background-color: #2a2a2a;
    padding: 20px;
    border-radius: 0 0 15px 15px;
    color: white;
    height: 100%;
}

.calendarHeader h3 {
    text-align: center;
    margin-bottom: 20px;
    font-size: 1.5rem;
    color: orangered;
    font-weight: bold;
}

.calendarGrid {
    display: grid;
    grid-template-columns: repeat(7, 1fr);
    gap: 8px;
}

.weekday {
    text-align: center;
    font-size: 0.8rem;
    color: #888;
    margin-bottom: 5px;
    text-transform: uppercase;
}

.daySquare {
    aspect-ratio: 1/1;
    background-color: #444; 
    border-radius: 6px;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 0.9rem;
    position: relative;
    
    border-bottom: 4px solid #333; 
    transition: all 0.2s ease;
}

.daySquare.empty {
    background-color: transparent;
    border-bottom: none;
}

/* 
   TODAY STATE
   Uses box-shadow instead of border so it doesn't conflict with the bottom orange line
*/
.daySquare.isToday {
    box-shadow: inset 0 0 0 2px white; /* Inner white border */
    font-weight: bold;
    color: white;
}

/* Task exists, not hovering specific one */
.daySquare.lineOrange {
    border-bottom-color: orange;
}

/* Hovering specific task */
.daySquare.highlighted {
    background-color: orange;      
    border-bottom-color: orangered; 
    color: white;
    font-weight: bold;
    transform: scale(1.1);
    box-shadow: 0 4px 10px rgba(0,0,0,0.3); /* Outer shadow for depth */
    z-index: 10;
}

/* If Today IS highlighted, combine shadows cleanly */
.daySquare.highlighted.isToday {
    box-shadow: inset 0 0 0 2px white, 0 4px 10px rgba(0,0,0,0.3);
}
</style>