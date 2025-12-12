<script>
    export default {
        props: {
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
            }
        }
    }
</script>

<template>
    <div class="listGroupWrapper">
        <!-- The Icon Box -->
        <div class="listGroup" :class="{ 'active-group': isActive }">
            <img :src="url" alt="">
        </div>

        <!-- The Tooltip Bubble (Discord Style) -->
        <div class="groupNameTooltip">
            {{ name }}
        </div>
    </div>
</template>

<style scoped>
/* Wrapper to handle positioning */
.listGroupWrapper {
    position: relative;
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
    transition: all 0.2s cubic-bezier(0.175, 0.885, 0.32, 1.275); /* Bouncy transition */
    position: relative;
    z-index: 2;
}

/* Hover Effect: Turns into a rounded square (Discord style) */
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
    border-radius: inherit; /* Follows parent border-radius */
    transition: border-radius 0.2s;
}

/* Selected State */
.listGroup.active-group {
    box-shadow: 0 0 10px rgba(249, 115, 22, 0.4);
}

/* --- TOOLTIP BUBBLE --- */
.groupNameTooltip {
    position: absolute;
    left: 70px; /* Push it to the right of the sidebar */
    top: 50%;
    transform: translateY(-50%) scale(0.9);
    
    background-color: black;
    color: white;
    padding: 8px 12px;
    border-radius: 8px;
    font-size: 14px;
    font-weight: bold;
    white-space: nowrap;
    
    opacity: 0;
    visibility: hidden;
    pointer-events: none; /* Mouse passes through */
    z-index: 100;
    
    box-shadow: 0 4px 10px rgba(0,0,0,0.3);
    transition: all 0.15s ease;
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

/* Show Tooltip on Wrapper Hover */
.listGroupWrapper:hover .groupNameTooltip {
    opacity: 1;
    visibility: visible;
    transform: translateY(-50%) scale(1);
}

/* --- MOBILE & TOUCH: Disable Tooltip --- */
@media (max-width: 768px), (hover: none) {
    .groupNameTooltip {
        display: none !important;
    }
    
    .listGroupWrapper {
        justify-content: center; /* Ensure centered */
    }
}
</style>