<script>
    export default {
        props: {
            id: { type: [Number, String], required: true },
            url: { type: String, default: "" },
            title: { type: String, default: "" },
            desc: { type: String, default: "" },
            // Prop to show visual selection state
            isSelected: { type: Boolean, default: false }
        },
        // Added 'select' emitter
        emits: ['click', 'hover', 'leave', 'select'] 
    }
</script>

<template>
    <div 
        class="task"
        :class="{ 'selected-task': isSelected }"
        @mouseenter="$emit('hover', id)"
        @mouseleave="$emit('leave')"
        @click="$emit('select', id)"
    >
        <img :src="url" alt="" class="taskImage">
        
        <div class="taskText">
            <h2 class="taskTitle">{{title}}</h2>
            <p class="taskDesc">{{ desc }}</p>
            <!-- .stop prevents the selection click from firing when clicking Details -->
            <button class="detailsBtn" @click.stop="$emit('click')">Details</button>
        </div>
    </div>
</template>

<style scoped>
    /* --- DESKTOP STYLES --- */
    .task {
        display: flex;
        flex-direction: row;
        background-color: var(--c-surface);
        border: 1px solid var(--border-color);
        color: var(--c-text-primary);
        border-radius: var(--radius-md);
        
        font-family: Arial, Helvetica, sans-serif;
        width: 100%;
        margin: 10px 0;
        max-height: 145px;
        align-items: stretch; 
        position: relative; 
        overflow: hidden; 
        transition: all 0.2s ease;
        cursor: pointer; /* Clickable for selection */
    }

    /* Selected State (Visual feedback) */
    .selected-task {
        border-color: var(--c-accent);
        box-shadow: 0 0 0 1px var(--c-accent);
    }

    .task:hover {
        transform: translateY(-2px);
        box-shadow: inset 0 0 0 2px var(--c-accent); 
        z-index: 5;
    }

    .taskImage{
        width: 125px;
        height: 125px;
        aspect-ratio: 1/1;
        object-fit: cover;
        margin: 10px;
        flex-shrink: 0;
        border-radius: 8px;
        align-self: center;
        background-color: var(--c-bg);
    }

    .taskText {
        flex-grow: 1; 
        padding: 15px;
        min-width: 0; 
        padding-right: 100px; 
    }

    .taskTitle{
        font-size: 24px;
        font-weight: bold;
        margin: 0 0 5px 0;
        padding: 0;
        line-height: 1.2;
        color: var(--c-text-primary);
    }

    .taskDesc{
        margin: 0;
        font-size: 16px;
        color: var(--c-text-secondary);
        display: -webkit-box;
        text-overflow: ellipsis;
        overflow: hidden;
        -webkit-box-orient: vertical;
        -webkit-line-clamp: 3;
        word-break: keep-all;
    }

    .detailsBtn {
        font-size: 14px;
        font-weight: bold;
        padding: 0 20px;
        border: none;
        cursor: pointer;
        background-color: var(--c-surface-hover); 
        color: var(--c-text-primary);
        border-left: 1px solid var(--border-color);
        white-space: nowrap;
        position: absolute;
        right: 0;      
        top: 0;        
        height: 100%;  
        border-radius: 0; 
        transition: background 0.2s;
    }
    
    .task:hover .detailsBtn {
        background-color: var(--c-accent);
        color: white;
    }

    /* --- MOBILE TILE LAYOUT (< 530px) --- */
    @media (max-width: 530px) {
        .task {
            flex-direction: column;
            margin: 10px 0;
            padding: 0;
            aspect-ratio: 2 / 1; 
            height: auto; 
            max-height: none; 
            width: 100%; 
            min-width: 0; 
            border: 1px solid var(--border-color);
            background-color: var(--c-surface); 
            box-shadow: none !important;
            cursor: pointer; 
            transform: translateZ(0); 
        }
        
        .task:hover {
            box-shadow: none !important;
            z-index: auto;
            transform: none;
        }

        .taskImage {
            width: 100%;
            height: 100%;
            margin: 0;
            border-radius: 0; 
            background-color: transparent;
            aspect-ratio: auto;
            object-fit: cover; 
            object-position: center; 
        }

        .taskText {
            padding: 10px;
            position: absolute;
            bottom: 0;
            left: 0;
            width: 100%;
            background-color: rgba(18, 18, 18, 0.85); 
            backdrop-filter: blur(4px); 
            border-radius: 0; 
            display: block;
            text-align: center;
        }

        .taskTitle {
            font-size: 18px;
            color: var(--c-text-primary);
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        .taskDesc {
            display: none;
        }

        .detailsBtn {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            opacity: 0; 
            z-index: 10;
            margin: 0;
            background-color: transparent;
            border-radius: 0; 
        }
    }
</style>