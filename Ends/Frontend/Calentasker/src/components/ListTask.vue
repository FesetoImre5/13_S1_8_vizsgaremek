<script>
    export default {
        props: {
            id: { type: [Number, String], required: true },
            url: { type: String, default: "" },
            title: { type: String, default: "" },
            desc: { type: String, default: "" },
            isSelected: { type: Boolean, default: false },
            priority: { type: String, default: "low" },
            dueDate: { type: String, default: null } 
        },
        emits: ['click', 'hover', 'leave', 'select'],
        computed: {
            formattedPriority() {
                if (!this.priority) return "Priority: Low";
                // Capitalize first letter
                const p = this.priority.charAt(0).toUpperCase() + this.priority.slice(1);
                return `Task Priority: ${p}`;
            },
            priorityColorClass() {
                const p = this.priority ? this.priority.toLowerCase() : 'low';
                return `priority-${p}`;
            },
            dueStatus() {
                if (!this.dueDate) return { text: "No Due Date", colorClass: "due-gray" };

                const now = new Date();
                const due = new Date(this.dueDate);
                
                // Reset times to compare dates only
                const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
                const dueDay = new Date(due.getFullYear(), due.getMonth(), due.getDate());

                const diffTime = dueDay - today; 
                const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

                if (diffDays < 0) {
                    return { text: "Overdue", colorClass: "due-red" };
                } else if (diffDays === 0) {
                    return { text: "Today", colorClass: "due-red" };
                } else if (diffDays === 1) {
                    return { text: "Tomorrow", colorClass: "due-orange" };
                } else if (diffDays < 7) {
                    return { text: `In ${diffDays} days`, colorClass: "due-yellow" };
                } else if (diffDays < 28) {
                    const weeks = Math.ceil(diffDays / 7);
                    return { text: `In ${weeks} week${weeks > 1 ? 's' : ''}`, colorClass: "due-blue" };
                } else {
                    return { text: "More than a month", colorClass: "due-green" };
                }
            }
        }
    }
</script>

<template>
    <div 
        class="taskCard"
        :class="{ 'isSelected': isSelected }"
        @mouseenter="$emit('hover', id)"
        @mouseleave="$emit('leave')"
        @click="$emit('select', id)"
    >
        <!-- Left: Image -->
        <div class="cardImageWrapper">
            <img :src="url" alt="Task Image">
        </div>

        <!-- Center: Content -->
        <div class="cardContent">
            <div class="cardHeader">
                <h3 class="cardTitle">{{ title }}</h3>
                
                <!-- Priority Badge -->
                <span class="statusPill" :class="priorityColorClass">
                    {{ formattedPriority }}
                </span>

                <!-- Due Date Badge -->
                <span class="statusPill" :class="dueStatus.colorClass">
                    {{ dueStatus.text }}
                </span>
            </div>
            
            <p class="cardDesc">{{ desc || "No description provided." }}</p>
            
            <!-- Optional: Date or Metadata (Hidden if using badge, or keep as extra info) -->
            <!-- <div class="cardMeta">
                <span class="date">Dec 16</span>
            </div> -->
        </div>

        <!-- Right: Action Area -->
        <div class="cardAction">
            <button class="viewBtn" @click.stop="$emit('click')">
                View
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
                    <polyline points="9 18 15 12 9 6"></polyline>
                </svg>
            </button>
        </div>
    </div>
</template>

<style scoped>
/* --- MAIN CARD CONTAINER --- */
/* --- MAIN CARD CONTAINER --- */
.taskCard {
    display: flex;
    align-items: center;
    gap: 15px;
    
    background-color: var(--c-surface);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-lg); 
    
    padding: 16px;
    margin-bottom: 12px;
    
    width: 100%;
    position: relative;
    cursor: pointer;
    overflow: hidden;
    
    box-shadow: var(--shadow-sm);
    transition: all 0.2s cubic-bezier(0.25, 0.8, 0.25, 1);
}

/* --- HOVER & SELECTION STATES --- */
.taskCard:hover {
    transform: translateY(-2px); 
    background-color: var(--c-surface-hover); 
    border-color: rgba(255,255,255,0.1);
    box-shadow: var(--shadow-md);
}

.taskCard.isSelected {
    border-color: var(--c-accent);
    box-shadow: var(--shadow-glow);
}

/* --- IMAGE --- */
.cardImageWrapper {
    flex-shrink: 0;
}

.cardImageWrapper img {
    width: 80px;
    height: 80px;
    object-fit: cover;
    border-radius: 12px;
    background-color: var(--c-bg);
    border: 1px solid var(--border-color);
}

/* --- CONTENT AREA --- */
.cardContent {
    flex-grow: 1;
    min-width: 0; 
    display: flex;
    flex-direction: column;
    gap: 6px;
}

.cardHeader {
    display: flex;
    align-items: center;
    gap: 10px;
    flex-wrap: wrap;
}

.cardTitle {
    margin: 0;
    font-size: 1.1rem;
    font-weight: 700;
    color: var(--c-text-primary);
    line-height: 1.2;
}

/* Status Pill Base */
.statusPill {
    display: inline-flex;
    padding: 4px 10px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    border: 1px solid transparent;
}

/* Priority Colors */
.priority-urgent {
    background: rgba(220, 38, 38, 0.15);
    color: #ef4444; 
    border-color: rgba(220, 38, 38, 0.3);
}
.priority-high {
    background: rgba(249, 115, 22, 0.15);
    color: #f97316; 
    border-color: rgba(249, 115, 22, 0.3);
}
.priority-medium {
    background: rgba(234, 179, 8, 0.15);
    color: #eab308; 
    border-color: rgba(234, 179, 8, 0.3);
}
.priority-low {
    background: rgba(34, 197, 94, 0.15);
    color: #22c55e;
    border-color: rgba(34, 197, 94, 0.3);
}

/* Due Date Colors */
.due-red {
    background: rgba(220, 38, 38, 0.15);
    color: #ef4444; 
    border-color: rgba(220, 38, 38, 0.3);
}
.due-orange {
    background: rgba(249, 115, 22, 0.15);
    color: #f97316; 
    border-color: rgba(249, 115, 22, 0.3);
}
.due-yellow {
    background: rgba(234, 179, 8, 0.15);
    color: #eab308; 
    border-color: rgba(234, 179, 8, 0.3);
}
.due-blue {
    background: rgba(59, 130, 246, 0.15);
    color: #3b82f6; 
    border-color: rgba(59, 130, 246, 0.3);
}
.due-green {
    background: rgba(34, 197, 94, 0.15);
    color: #22c55e; 
    border-color: rgba(34, 197, 94, 0.3);
}
.due-gray {
    background: rgba(113, 113, 122, 0.15);
    color: #a1a1aa; 
    border-color: rgba(113, 113, 122, 0.3);
}

.cardDesc {
    margin: 0;
    font-size: 0.9rem;
    color: var(--c-text-secondary);
    
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
    line-height: 1.4;
}

.cardMeta {
    font-size: 0.8rem;
    color: var(--c-text-secondary);
    opacity: 0.7;
}

/* --- ACTION BUTTON --- */
.cardAction {
    flex-shrink: 0;
    display: flex;
    align-items: center;
}

.viewBtn {
    background-color: transparent;
    color: var(--c-text-secondary);
    border: 1px solid var(--border-color);
    padding: 8px 14px;
    border-radius: 30px; 
    font-size: 0.85rem;
    font-weight: 600;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 5px;
    transition: all 0.2s ease;
}

.taskCard:hover .viewBtn {
    background-color: var(--c-accent);
    color: white;
    border-color: var(--c-accent);
}

/* --- MOBILE TILE LAYOUT (< 530px) --- */
@media (max-width: 530px) {
    .taskCard {
        flex-direction: column;
        align-items: flex-start;
        padding: 0;
        gap: 0;
        border-radius: 12px;
    }

    .cardImageWrapper {
        width: 100%;
        height: 140px;
    }

    .cardImageWrapper img {
        width: 100%;
        height: 100%;
        border-radius: 12px 12px 0 0;
        border: none;
    }

    .cardContent {
        padding: 15px;
        width: 100%;
    }

    .cardHeader {
        justify-content: flex-start; /* flow normally on mobile, or keep space-between if desired */
    }

    .cardAction {
        display: none;
    }
    
    .cardDesc {
        -webkit-line-clamp: 3;
    }
}
</style>