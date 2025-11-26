<script setup>
import { ref } from 'vue';

// State for the mobile dropdown
const isMenuOpen = ref(false);

const navLinks = [
    { name: 'Tasks', path: '/' },
    { name: 'Login', path: '/auth' }
];
</script>

<template>
    <nav class="navbar">
        <div class="navbarContainer">
            <!-- LOGO -->
            <div class="logo">
                <router-link to="/">
                    <img src="../assets/logo-with-text.svg" alt="Logo">
                </router-link>
            </div>

            <!-- DESKTOP MENU -->
            <div class="desktopMenu">
                <ul class="navList">
                    <li v-for="link in navLinks" :key="link.name">
                        <router-link :to="link.path" class="navButton">
                            {{ link.name }}
                        </router-link>
                    </li>
                </ul>
            </div>
        </div>
        
        <div class="hamburgerMenu">
            <!-- HAMBURGER BUTTON -->
            <button 
                class="hamburgerBtn" 
                @click="isMenuOpen = !isMenuOpen"
                aria-label="Toggle menu"
            >
                <img src="../assets/list.svg" alt="Menu" class="hamburgerIcon">
            </button>
        </div>

        <!-- MOBILE DROPDOWN -->
        <div class="mobileDropdown" :class="{ 'isOpen': isMenuOpen }">
            <div class="mobileDropdownInner">
                <ul>
                    <li v-for="link in navLinks" :key="link.name">
                        <router-link 
                            :to="link.path" 
                            @click="isMenuOpen = false"
                            class="mobileButton"
                        >
                            {{ link.name }}
                        </router-link>
                    </li>
                </ul>
            </div>
        </div>
    </nav>
</template>

<style scoped>
/* --- CONFIGURATION --- */
.navbar {
    --nav-bg: #222;
    --nav-text: #fff;
    --accent: orangered; 
    --navbar-height: 70px;
    
    background-color: var(--nav-bg);
    color: var(--nav-text);
    height: var(--navbar-height);
    
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    z-index: 1000;
}

.navbarContainer {
    max-width: 1000px;
    height: 100%;
    margin: 0;
    padding: 0 1rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

/* --- LOGO --- */
.logo img {
    height: 40px;
    width: auto;
    display: block;
    margin-right: 20px;
}

/* --- BUTTON STYLES (DESKTOP) --- */
.navButton {
    text-decoration: none;
    color: var(--nav-text);
    font-size: 0.95rem;
    font-weight: 500;
    padding: 0.6rem 1.2rem;
    border-radius: 6px;
    background-color: transparent;
    border: 1px solid transparent;
    
    /* Important: Disable default browser focus outline to prevent "Double Shadow" */
    /*outline: none; */ 
    
    transition: all 0.2s ease;
}

/*  1. HOVER STATE (Only if not active) */
.navButton:hover:not(.router-link-exact-active) {
    background-color: rgba(255, 255, 255, 0.1);
}

/*  2. ACTIVE PAGE STATE (The "Lit Up" Look) */
.navButton.router-link-exact-active {
    background-color: var(--accent);
    color: #fff;
    font-weight: bold;
    /* Lift up and cast shadow */
    transform: translateY(-2px); 
    box-shadow: 0 4px 10px rgba(255, 69, 0, 0.4);
}

/*  3. CLICKING STATE (Mouse Held Down) 
    We explicitly target the active class too, so this overrides the shadow above.
*/
.navButton:active,
.navButton.router-link-exact-active:active {
    /* SNAP DOWN: Remove the lift */
    transform: translateY(0) !important; 
    /* REMOVE SHADOW: This prevents the "double density" look */
    /*box-shadow: none !important; */
    /* FEEDBACK: Make it slightly darker to look "pressed" */
    filter: brightness(0.85);
}

/*  4. FOCUS STATE (After click release) 
    Ensures the shadow doesn't come back weirdly if the button stays focused 
*/
.navButton:focus-visible {
    outline: none;
    box-shadow: 0 0 0 2px rgba(255, 255, 255, 0.5); /* Optional: A clean focus ring */
}


/* --- BUTTON STYLES (MOBILE) --- */
.mobileButton {
    text-decoration: none;
    color: var(--nav-text);
    font-size: 1.1rem;
    display: block;
    padding: 1.2rem;
    text-align: center;
    border-bottom: 1px solid #444;
    background-color: transparent;
    transition: background-color 0.2s ease;
}

.mobileButton:hover {
    background-color: #333;
}

.mobileButton.router-link-exact-active {
    background-color: var(--accent);
    color: #fff;
    font-weight: bold;
    border-bottom: 1px solid var(--accent);
}

/* =========================================
    MEDIA QUERIES
   ========================================= */

@media (max-width: 600px) {
    .desktopMenu { display: none; }
    
    .hamburgerMenu {
        float: right; 
        margin-right: 20px;
    }

    .hamburgerBtn {
        display: block;
        background: none;
        border: none;
        cursor: pointer;
        padding: 5px;
    }

    .hamburgerIcon {
        width: 30px;
        height: 30px;
        filter: invert(1);
        display: block;
    }
}

@media (min-width: 601px) {
    .hamburgerBtn, .mobileDropdown {
        display: none !important;
    }

    .desktopMenu { display: block; }

    .navList {
        display: flex;
        gap: 1rem;
        list-style: none;
        margin: 0;
        padding: 0;
    }
}

/* =========================================
    MOBILE DROPDOWN ANIMATION
   ========================================= */
.mobileDropdown {
    position: absolute;
    top: var(--navbar-height);
    left: 0;
    width: 100%;
    background-color: #2a2a2a;
    display: grid;
    grid-template-rows: 0fr;
    transition: grid-template-rows 0.3s ease-out;
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
}

.mobileDropdown.isOpen {
    grid-template-rows: 1fr;
}

.mobileDropdownInner {
    overflow: hidden;
}

.mobileDropdown ul {
    list-style: none;
    margin: 0;
    padding: 0;
    display: flex;
    flex-direction: column;
}
</style>