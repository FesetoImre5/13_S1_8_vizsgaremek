<script setup>
import { ref } from 'vue';

const props = defineProps({
    url: {
        type: String,
        default: "https://www.mariposakids.co.nz/wp-content/uploads/2014/08/image-placeholder2.jpg"
    },
    name: {
        type: String,
        default: "Group Name"
    },
    isActive: {
        type: Boolean,
        default: false
    },
    isSystemIcon: {
        type: Boolean,
        default: false
    }
});

// State to handle hover and positioning
const isHovered = ref(false);
const iconRef = ref(null);
const tooltipPos = ref({ top: 0, left: 0 });

const handleMouseEnter = () => {
    if (iconRef.value) {
        // Get the position of the icon on the screen
        const rect = iconRef.value.getBoundingClientRect();
        
        // Calculate position: 
        // Top: Center of icon
        // Left: Right side of icon + 15px gap
        tooltipPos.value = {
            top: rect.top + (rect.height / 2),
            left: rect.right + 15
        };
        isHovered.value = true;
    }
};

const handleMouseLeave = () => {
    isHovered.value = false;
};
</script>

<template>
    <div 
        class="listGroupWrapper"
        ref="iconRef"
        @mouseenter="handleMouseEnter"
        @mouseleave="handleMouseLeave"
    >
        <!-- The Icon Box -->
        <div class="listGroup" :class="{ 'active-group': isActive, 'system-icon-container': isSystemIcon }">
            <img :src="url" alt="">
        </div>

        <!-- 
            TELEPORT: This moves the tooltip div to the <body> tag 
            so it is never clipped by the sidebar's scrollbar or z-index.
        -->
        <Teleport to="body">
            <Transition name="fade">
                <div 
                    v-if="isHovered" 
                    class="groupNameTooltip"
                    :style="{ top: `${tooltipPos.top}px`, left: `${tooltipPos.left}px` }"
                >
                    {{ name }}
                </div>
            </Transition>
        </Teleport>
    </div>
</template>

<style scoped>
/* Wrapper to handle positioning references */
.listGroupWrapper {
    width: 100%;
    display: flex;
    justify-content: center;
    margin: 8px 0;
}

/* The Icon Container */
.listGroup {
    width: 50px; 
    height: 50px;
    
    display: flex;
    align-items: center;
    justify-content: center;
    
    background-color: var(--c-surface);
    border: 1px solid var(--border-color);
    border-radius: 50%; /* Circle by default */
    
    cursor: pointer;
    transition: all 0.2s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    position: relative;
    z-index: 2;
}

/* Hover Effect */
.listGroupWrapper:hover .listGroup,
.listGroup.active-group {
    border-radius: 15px; /* Squircle */
    background-color: var(--c-accent);
    border-color: var(--c-accent);
}

.listGroup img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: inherit;
    transition: border-radius 0.2s;
}

/* System Icon Styles */
.listGroup.system-icon-container img {
    width: 60%; /* Shrink the icon */
    height: 60%;
    object-fit: contain; /* Ensure standard icon aspect ratio */
    filter: brightness(0) invert(1); /* Make it white */
    border-radius: 0; /* Don't round the icon itself if it's a shape */
}

/* Selected State */
.listGroup.active-group {
    box-shadow: 0 0 10px rgba(249, 115, 22, 0.4);
}

/* --- TOOLTIP BUBBLE (Fixed Position via Teleport) --- */
.groupNameTooltip {
    position: fixed; /* Fixed relative to viewport */
    transform: translateY(-50%); /* Center vertically on the coordinates */
    
    background-color: black;
    color: white;
    padding: 8px 12px;
    border-radius: 8px;
    font-size: 14px;
    font-weight: bold;
    white-space: nowrap;
    
    pointer-events: none; /* Mouse passes through */
    z-index: 9999; /* Higher than everything else */
    
    box-shadow: 0 4px 10px rgba(0,0,0,0.3);
}

/* Little triangle pointing to the left */
.groupNameTooltip::before {
    content: "";
    position: absolute;
    top: 50%;
    left: -6px;
    margin-top: -6px;
    border-width: 6px 6px 6px 0;
    border-style: solid;
    border-color: transparent black transparent transparent;
}

/* --- TRANSITION ANIMATION --- */
.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.15s ease, transform 0.15s ease;
}

.fade-enter-from,
.fade-leave-to {
    opacity: 0;
    transform: translateY(-50%) scale(0.9); /* Start slightly smaller */
}

/* --- MOBILE & TOUCH --- */
@media (max-width: 768px), (hover: none) {
    .groupNameTooltip {
        display: none !important;
    }
}
</style>
