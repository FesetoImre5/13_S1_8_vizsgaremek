<script>
    export default {
        props: {
            id: { type: [Number, String], required: true },
            url: { type: String, default: "" },
            title: { type: String, default: "" },
            desc: { type: String, default: "" },
            isSelected: { type: Boolean, default: false }
        },
        emits: ['click', 'hover', 'leave', 'select']
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
                <!-- Mock Badge -->
                <span class="badge priorityHigh">High Priority</span>
            </div>
            
            <p class="cardDesc">{{ desc || "No description provided." }}</p>
            
            <!-- Optional: Date or Metadata -->
            <div class="cardMeta">
                <span class="date">Dec 16</span>
            </div>
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
.taskCard {
    display: flex;
    align-items: center;
    gap: 15px;
    
    background-color: var(--c-surface);
    border: 1px solid var(--border-color);
    border-radius: 16px; 
    
    padding: 15px;
    margin-bottom: 15px;
    
    width: 100%;
    position: relative;
    cursor: pointer;
    overflow: hidden;
    
    transition: all 0.25s cubic-bezier(0.25, 0.8, 0.25, 1);
}

/* --- HOVER & SELECTION STATES --- */
.taskCard:hover {
    transform: translateY(-4px); 
    background-color: #27272a; 
    border-color: var(--c-text-secondary);
    box-shadow: 0 10px 20px rgba(0,0,0,0.3);
}

.taskCard.isSelected {
    border-color: var(--c-accent);
    box-shadow: inset 0 0 0 1px var(--c-accent);
    background-color: rgba(249, 115, 22, 0.05); 
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

/* Badge Style */
.badge {
    font-size: 0.7rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    padding: 2px 8px;
    border-radius: 6px;
}
.badge.priorityHigh {
    background-color: rgba(220, 38, 38, 0.2); 
    color: #ef4444;
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
        justify-content: space-between;
    }

    .cardAction {
        display: none;
    }
    
    .cardDesc {
        -webkit-line-clamp: 3;
    }
}
</style>