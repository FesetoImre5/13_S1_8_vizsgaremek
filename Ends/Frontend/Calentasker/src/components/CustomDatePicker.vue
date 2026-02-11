<script setup>
import { ref, computed, watch, onMounted, onUnmounted, nextTick } from 'vue';
import { useI18n } from 'vue-i18n';

const props = defineProps({
    modelValue: {
        type: String,
        default: ''
    },
    placeholder: {
        type: String,
        default: ''
    },
    min: {
        type: String, // YYYY-MM-DD
        default: ''
    },
    disabled: {
        type: Boolean,
        default: false
    }
});

const emit = defineEmits(['update:modelValue']);
const { t, locale } = useI18n();

const isOpen = ref(false);
const pickerRef = ref(null);
const dropdownPosition = ref({ top: '0px', left: '0px', width: '280px' });

// Format date for display
// Format date for display
const displayValue = computed(() => {
    if (!props.modelValue) return '';
    
    // Parse YYYY-MM-DD manually to ensure local time is used
    // pulling "2024-02-15" -> new Date(2024, 1, 15)
    const parts = props.modelValue.split('-');
    if (parts.length !== 3) return props.modelValue;

    const year = parseInt(parts[0], 10);
    const month = parseInt(parts[1], 10) - 1;
    const day = parseInt(parts[2], 10);

    const date = new Date(year, month, day);
    if (isNaN(date.getTime())) return '';
    
    return date.toLocaleDateString(locale.value, {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
});

// Calendar State
const currentMonth = ref(new Date().getMonth());
const currentYear = ref(new Date().getFullYear());

// Initialize calendar to selected date or today
watch(() => props.modelValue, (newVal) => {
    if (newVal) {
        const parts = newVal.split('-');
        if (parts.length === 3) {
            const y = parseInt(parts[0], 10);
            const m = parseInt(parts[1], 10) - 1;
            // No need for day just to set month/year
            currentMonth.value = m;
            currentYear.value = y;
        }
    }
}, { immediate: true });

// Update position when opening
watch(isOpen, async (val) => {
    if (val && pickerRef.value) {
        await nextTick();
        updatePosition();
        window.addEventListener('resize', updatePosition);
        window.addEventListener('scroll', updatePosition, true); // true for capture to catch all scrolls
    } else {
        window.removeEventListener('resize', updatePosition);
        window.removeEventListener('scroll', updatePosition, true);
    }
});

const updatePosition = () => {
    if (!pickerRef.value) return;
    const rect = pickerRef.value.getBoundingClientRect();
    const dropdownHeight = 320; // Approx max height
    const spaceBelow = window.innerHeight - rect.bottom;
    
    let top = rect.bottom + 8;
    // If not enough space below, show above
    if (spaceBelow < dropdownHeight && rect.top > dropdownHeight) {
        top = rect.top - dropdownHeight - 8;
    }

    dropdownPosition.value = {
        top: `${top + window.scrollY}px`,
        left: `${rect.left + window.scrollX}px`,
        width: '280px' // Fixed width for calendar
    };
};

// Calendar Navigation
const monthName = computed(() => {
    return new Date(currentYear.value, currentMonth.value).toLocaleString(locale.value, { month: 'long' });
});

const weekDays = computed(() => {
    const days = [];
    // Start on Monday or Sunday depending on preference. 
    // This trick uses a known week (Jan 2024). Jan 1 2024 is Monday.
    // If we want Sunday start: Jan 7 2024
    const d = new Date(2024, 0, 7); 
    for (let i = 0; i < 7; i++) {
        days.push(d.toLocaleDateString(locale.value, { weekday: 'short' }));
        d.setDate(d.getDate() + 1);
    }
    return days;
});

const calendarDays = computed(() => {
    const days = [];
    const firstDay = new Date(currentYear.value, currentMonth.value, 1);
    const lastDay = new Date(currentYear.value, currentMonth.value + 1, 0);
    
    // Adjust start day (assuming Sunday start for visual grid 0-6)
    const startDayOfWeek = firstDay.getDay(); 
    const daysInMonth = lastDay.getDate();
    
    const prevMonthLastDay = new Date(currentYear.value, currentMonth.value, 0).getDate();
    for (let i = startDayOfWeek - 1; i >= 0; i--) {
        days.push({
            date: new Date(currentYear.value, currentMonth.value - 1, prevMonthLastDay - i),
            isCurrentMonth: false,
            isDisabled: true
        });
    }
    
    const today = new Date();
    today.setHours(0,0,0,0);
    
    for (let i = 1; i <= daysInMonth; i++) {
        const date = new Date(currentYear.value, currentMonth.value, i);
        
        // Use local time for YYYY-MM-DD construction to avoid UTC shifts
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');
        const dateString = `${year}-${month}-${day}`;
        
        let isDisabled = false;
        if (props.min) {
            isDisabled = dateString < props.min;
        }

        days.push({
            date: date,
            dayCheck: i,
            isCurrentMonth: true,
            isToday: date.getTime() === today.getTime(),
            isSelected: props.modelValue === dateString,
            isDisabled: isDisabled,
            value: dateString
        });
    }
    
    const remaining = 42 - days.length; 
    for (let i = 1; i <= remaining; i++) {
        days.push({
            date: new Date(currentYear.value, currentMonth.value + 1, i),
            isCurrentMonth: false,
            isDisabled: true
        });
    }
    
    return days;
});

const prevMonth = () => {
    if (currentMonth.value === 0) {
        currentMonth.value = 11;
        currentYear.value--;
    } else {
        currentMonth.value--;
    }
};

const nextMonth = () => {
    if (currentMonth.value === 11) {
        currentMonth.value = 0;
        currentYear.value++;
    } else {
        currentMonth.value++;
    }
};

const selectDate = (day) => {
    if (day.isDisabled || !day.isCurrentMonth) return;
    emit('update:modelValue', day.value);
    isOpen.value = false;
};

// Close on outside click
const handleClickOutside = (e) => {
    // Check if click is inside the picker input
    if (pickerRef.value && pickerRef.value.contains(e.target)) {
        return;
    }
    // Check if click is inside the dropdown (need a valid ref for dropdown content)
    const dropdown = document.getElementById('date-picker-dropdown-teleport');
    if (dropdown && dropdown.contains(e.target)) {
        return;
    }
    isOpen.value = false;
};

onMounted(() => {
    document.addEventListener('mousedown', handleClickOutside);
    document.addEventListener('touchstart', handleClickOutside);
});

onUnmounted(() => {
    document.removeEventListener('mousedown', handleClickOutside);
    document.removeEventListener('touchstart', handleClickOutside);
    window.removeEventListener('resize', updatePosition);
    window.removeEventListener('scroll', updatePosition, true);
});

</script>

<template>
    <div class="date-picker-container" ref="pickerRef">
        <!-- Input Field -->
        <div 
            class="date-input" 
            :class="{ 'focused': isOpen, 'disabled': disabled }"
            @click="!disabled && (isOpen = !isOpen)"
        >
            <span v-if="displayValue" class="display-text">{{ displayValue }}</span>
            <span v-else class="placeholder">{{ placeholder || 'Select date' }}</span>
            
            <span class="calendar-icon">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg>
            </span>
        </div>

        <!-- Dropdown (Teleported) -->
        <Teleport to="body">
            <Transition name="fade">
                <div 
                    v-if="isOpen" 
                    id="date-picker-dropdown-teleport"
                    class="calendar-dropdown"
                    :style="{ top: dropdownPosition.top, left: dropdownPosition.left }"
                >
                    <!-- Header -->
                    <div class="calendar-header">
                        <button @click.stop="prevMonth">&lt;</button>
                        <span class="month-year">{{ monthName }} {{ currentYear }}</span>
                        <button @click.stop="nextMonth">&gt;</button>
                    </div>

                    <!-- Days Header -->
                    <div class="weekdays-grid">
                        <span v-for="day in weekDays" :key="day">{{ day }}</span>
                    </div>

                    <!-- Days Grid -->
                    <div class="days-grid">
                        <div 
                            v-for="(day, index) in calendarDays" 
                            :key="index"
                            class="day-cell"
                            :class="{
                                'other-month': !day.isCurrentMonth,
                                'today': day.isToday,
                                'selected': day.isSelected,
                                'disabled': day.isDisabled
                            }"
                            @click.stop="selectDate(day)"
                        >
                            {{ day.date.getDate() }}
                        </div>
                    </div>
                </div>
            </Transition>
        </Teleport>
    </div>
</template>

<style scoped>
.date-picker-container {
    width: 100%;
}

.date-input {
    background: var(--c-bg);
    border: 1px solid var(--border-color);
    border-radius: 8px;
    padding: 10px 12px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    cursor: pointer;
    transition: all 0.2s;
    height: 42px; /* Match standard inputs like 'select' or 'input[type=text]' often used in your forms */
    box-sizing: border-box; /* Ensure padding doesn't affect height if width is set */
}

.date-input:hover {
    border-color: var(--c-text-secondary);
}

.date-input.focused {
    border-color: var(--c-accent);
    box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.1); 
}

.date-input.disabled {
    opacity: 0.6;
    cursor: not-allowed;
    background: rgba(255,255,255,0.02);
}

.display-text {
    color: var(--c-text-primary);
    font-size: 0.95rem;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    background: transparent;
    line-height: normal;
}

.placeholder {
    color: var(--c-text-secondary);
    font-size: 0.9rem;
    opacity: 0.7;
    background: transparent;
    line-height: normal;
}

.calendar-icon {
    color: var(--c-text-secondary);
    display: flex;
    margin-left: 8px;
}

/* Dropdown Teleported - Global Styles targeted via ID or class if global css allows, 
   but since this is scoped, Vue won't apply scoped styles to teleported content easily 
   unless we use :global or remove scoped. 
   HOWEVER, for single file components, Teleported content often loses scoped styles. 
   We will keep it scoped but use deep selectors or just inline/global logic?
   Actually, standard Vue scoped CSS DOES work with Teleport in mostly modern setups if structure is right,
   but often safest to rely on a specific class structure or global definitions.
   We will try standard structure first. If style is missing, we'll switch to :global equivalent.
*/

.calendar-dropdown {
    position: absolute; /* Relative to body */
    background: var(--c-surface);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.6);
    padding: 16px;
    z-index: 9999; /* Higher than everything */
    width: 280px;
}

.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.2s ease, transform 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
    opacity: 0;
    transform: translateY(-10px);
}

/* Header */
.calendar-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12px;
}

.calendar-header button {
    background: transparent;
    border: none;
    color: var(--c-text-secondary);
    cursor: pointer;
    font-weight: bold;
    padding: 4px 8px;
    border-radius: 4px;
    transition: background 0.2s;
}

.calendar-header button:hover {
    background: rgba(255,255,255,0.1);
    color: var(--c-text-primary);
}

.month-year {
    font-weight: 600;
    color: var(--c-text-primary);
    text-transform: capitalize;
}

/* Grid */
.weekdays-grid, .days-grid {
    display: grid;
    grid-template-columns: repeat(7, 1fr);
    text-align: center;
}

.weekdays-grid {
    margin-bottom: 8px;
}

.weekdays-grid span {
    font-size: 0.75rem;
    color: var(--c-text-secondary);
    font-weight: 600;
}

.day-cell {
    height: 32px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.9rem;
    cursor: pointer;
    border-radius: 6px;
    margin-bottom: 2px;
    color: var(--c-text-primary);
    transition: background 0.1s;
}

.day-cell:hover:not(.disabled):not(.other-month) {
    background: var(--c-surface-hover);
}

.day-cell.other-month {
    color: var(--c-text-secondary);
    opacity: 0.3;
    pointer-events: none; /* Can be removed if we want to allow selecting prev/next month days */
}

.day-cell.today {
    border: 1px solid var(--c-accent);
    color: var(--c-accent);
}

.day-cell.selected {
    background: var(--c-accent) !important;
    color: white !important;
}

.day-cell.disabled {
    opacity: 0.3;
    cursor: not-allowed;
    text-decoration: line-through;
}
</style>
