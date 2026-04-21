<script setup>
import { ref } from 'vue';
import { useRouter, useRoute } from 'vue-router'; 
import { useAuth } from '../composables/UseAuth';

const { user, logout } = useAuth();
const router = useRouter();
const route = useRoute(); 
const isOpen = ref(false);

// --- 2. LOCAL DIRECTIVE DEFINITION (Fixes the error without touching main.js) ---
const vClickOutside = {
    mounted(el, binding) {
        el.clickOutsideEvent = function(event) {
            // Check if the click was outside the element and its children
            if (!(el === event.target || el.contains(event.target))) {
                binding.value(event);
            }
        };
        document.body.addEventListener('click', el.clickOutsideEvent);
    },
    unmounted(el) {
        document.body.removeEventListener('click', el.clickOutsideEvent);
    }
};

const toggleMenu = () => {
    isOpen.value = !isOpen.value;
};

const handleLogout = () => {
    logout();
    isOpen.value = false;
    router.push('/auth');
};

const closeMenu = () => {
    // Only close if it's currently open
    if (isOpen.value) {
        isOpen.value = false;
    }
};

const isAuthActive = (mode) => {
    if (route.path !== '/auth') return false;
    if (!route.query.mode && mode === 'login') return true;
    return route.query.mode === mode;
};
</script>

<template>
    <div class="userMenuContainer">
        
        <!-- STATE 1: NOT LOGGED IN (Guest Group) -->
        <div v-if="!user" class="guestActions">
            <router-link 
                :to="{ path: '/auth', query: { mode: 'login' } }" 
                class="navButton"
                :class="{ 'custom-active': isAuthActive('login') }"
            >
                Login
            </router-link>
            
            <router-link 
                :to="{ path: '/auth', query: { mode: 'register' } }" 
                class="navButton"
                :class="{ 'custom-active': isAuthActive('register') }"
            >
                Register
            </router-link>
        </div>

        <!-- STATE 2: LOGGED IN (User Dropdown) -->
        <!-- The v-click-outside directive now uses the local definition above -->
        <div v-else class="loggedInWrapper" v-click-outside="closeMenu">
            
            <!-- Trigger Button -->
            <button 
                class="userTrigger" 
                @click="toggleMenu"
                :class="{ 'active': isOpen }"
            >
                <span class="username">{{ user.display_username || user.username }}</span>
                <span class="arrow" :class="{ 'flipped': isOpen }">▼</span>
            </button>

            <!-- Dropdown Menu -->
            <div class="dropdownMenu" :class="{ 'is-open': isOpen }">
                <div class="dropdownInner">
                    
                    <!-- 1. LINK TO PROFILE (Default Tab) -->
                    <router-link :to="{ path: '/profile', query: { tab: 'details' } }" class="dropdownItem" @click="closeMenu">
                        Profile
                    </router-link>

                    <!-- 2. LINK TO GROUPS (Switch Tab via Query) -->
                    <router-link :to="{ path: '/profile', query: { tab: 'groups' } }" class="dropdownItem" @click="closeMenu">
                        Groups
                    </router-link>

                    <div class="divider"></div>
                    <button class="dropdownItem logout" @click="handleLogout">
                        Log Out
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.userMenuContainer {
    --nav-text: #fff;
    --accent: orangered;
    position: relative;
    display: flex;
    align-items: center;
}

.guestActions { 
    display: flex; 
    gap: 10px; 
    align-items: center; 
}

/* SHARED BUTTON STYLES */
.navButton {
    text-decoration: none; 
    color: var(--nav-text); 
    font-size: 0.95rem; 
    font-weight: 500;
    padding: 0.6rem 1.2rem; 
    border-radius: 6px; 
    background-color: transparent; 
    border: 1px solid transparent; 
    transition: all 0.2s ease; 
    white-space: nowrap;
}

.navButton:hover:not(.custom-active) { 
    background-color: rgba(255, 255, 255, 0.1); 
}

.navButton.custom-active { 
    background-color: var(--accent); 
    color: #fff; 
    font-weight: bold; 
    transform: translateY(-2px); 
    box-shadow: 0 4px 10px rgba(255, 69, 0, 0.4); 
}

.navButton:active, .navButton.custom-active:active { 
    transform: translateY(0) !important; 
    filter: brightness(0.85); 
}

/* TRIGGER BUTTON */
.userTrigger {
    background: transparent; 
    border: none; 
    color: var(--nav-text); 
    font-size: 1rem; 
    cursor: pointer; 
    display: flex; 
    align-items: center; 
    gap: 8px; 
    padding: 0.6rem 1rem; 
    border-radius: 6px; 
    transition: background 0.2s;
}

.userTrigger:hover, .userTrigger.active { 
    background-color: rgba(255, 255, 255, 0.1); 
}

.arrow { 
    font-size: 0.7rem; 
    transition: transform 0.3s; 
}

.arrow.flipped { 
    transform: rotate(180deg); 
}

/* --- DESKTOP DROPDOWN (Popup Style) --- */
.dropdownMenu {
    position: absolute; 
    top: 130%; 
    right: 0; 
    width: 180px;
    background-color: #333;
    border-radius: 8px; 
    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    z-index: 1100;

    /* Hidden State (Desktop) */
    opacity: 0;
    transform: translateY(-10px);
    pointer-events: none; /* Prevents clicking when hidden */
    transition: opacity 0.2s ease, transform 0.2s ease;
}

/* Open State (Desktop) */
.dropdownMenu.is-open {
    opacity: 1;
    transform: translateY(0);
    pointer-events: auto;
}

.dropdownInner {
    display: flex; 
    flex-direction: column; 
    padding: 5px 0;
}

.dropdownItem {
    text-decoration: none; 
    color: #ddd;  
    padding: 10px 20px; 
    font-size: 0.95rem; 
    text-align: left; 
    background: none; 
    border: none; 
    cursor: pointer; 
    width: 100%; 
    transition: background 0.2s;
}

.dropdownItem:hover { 
    background-color: #2a2a2a;  
    color: #fff;
}

.dropdownItem.logout { 
    color: #dc2626; 
}

.dropdownItem.logout:hover { 
    background-color: #2a2a2a;  
}

.divider { 
    height: 1px; 
    background-color: #444; 
    margin: 4px 0; 
}

/* --- MOBILE OVERRIDES (Accordion Style) --- */
@media (max-width: 600px) {
    .userMenuContainer { 
        width: 100%; 
        flex-direction: column; 
    }
    .guestActions { 
        flex-direction: column; 
        width: 100%; 
        gap: 0; 
    }
    
    /* Mobile Nav Buttons */
    .navButton {
        width: 100%; 
        border-radius: 0; 
        border: none; 
        border-bottom: 1px solid #444; 
        padding: 1.2rem; 
        text-align: center; 
        font-size: 1.1rem; 
        display: block; 
        transform: none !important; 
        box-shadow: none !important; 
        color: #fff; 
        background-color: transparent;
    }

    .navButton:hover { 
        background-color: #333; 
    }

    .navButton.custom-active { 
        background-color: var(--accent); 
        color: #fff; 
        font-weight: bold; 
        border-bottom: 1px solid var(--accent); 
        transform: none; 
        box-shadow: none; 
    }

    .loggedInWrapper { 
        width: 100%; 
    }

    /* Mobile User Trigger */
    .userTrigger {
        display: flex; 
        justify-content: center; 
        width: 100%; 
        padding: 1.2rem; 
        border-radius: 0; 
        border-bottom: 1px solid #444; 
        font-size: 1.1rem; 
        color: #fff; 
        background-color: transparent;
    }

    .userTrigger:hover, .userTrigger.active { 
        background-color: #333; 
    }

    .arrow { 
        margin-left: 8px; 
    }

    /* --- MOBILE DROPDOWN ANIMATION (Grid Trick) ---*/
    .dropdownMenu {
        position: static; 
        width: 100%;
        box-shadow: none; 
        background-color: #1a1a1a; /* Darker bg */
        border-radius: 0; 
        
        /* Reset Desktop Transitions */
        opacity: 1; 
        transform: none;
        pointer-events: auto;

        /* THE ANIMATION MAGIC */
        display: grid;
        grid-template-rows: 0fr; /* Start collapsed */
        transition: grid-template-rows 0.3s ease-out; /* Smooth slide */
    }

    /* Open State (Mobile) */
    .dropdownMenu.is-open {
        grid-template-rows: 1fr; /* Expand to fit content */
    }

    /* Inner wrapper handles overflow */
    .dropdownInner {
        overflow: hidden;
        padding: 0; /* Reset padding to be handled by items */
    }

    .dropdownItem {
        color: #ddd; 
        padding: 1.2rem; 
        text-align: center; 
        border-bottom: 1px solid #333; 
        font-size: 1rem;
    }

    .dropdownItem:hover { 
        background-color: #2a2a2a; 
        color: #fff; 
    }

    .dropdownItem.logout { 
        color: #ff6b6b; 
    }

    .dropdownItem.logout:hover { 
        background-color: #2a2a2a; 
    }

    .divider { 
        display: none; 
    }
}
</style>