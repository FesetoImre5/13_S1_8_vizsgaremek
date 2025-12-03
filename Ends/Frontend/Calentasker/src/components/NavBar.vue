<script setup>
import { ref } from 'vue';
import UserMenu from './UserMenu.vue';

const isMenuOpen = ref(false);

const navLinks = [
    { name: 'Tasks', path: '/' }
];
</script>

<template>
    <nav class="navbar">
        <div class="navbarContainer">
            
            <!-- LEFT: Logo + Links -->
            <div class="navLeft">
                <div class="logo">
                    <router-link to="/">
                        <img src="../assets/logo-with-text.svg" alt="Logo">
                    </router-link>
                </div>
                <ul class="desktopLinks">
                    <li v-for="link in navLinks" :key="link.name">
                        <router-link :to="link.path" class="navButton">
                            {{ link.name }}
                        </router-link>
                    </li>
                </ul>
            </div>

            <!-- RIGHT: UserMenu -->
            <div class="navRight">
                <UserMenu />
            </div>

            <!-- HAMBURGER -->
            <div class="hamburgerMenu">
                <button class="hamburgerBtn" @click="isMenuOpen = !isMenuOpen">
                    <img src="../assets/list.svg" alt="Menu" class="hamburgerIcon">
                </button>
            </div>
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
                    <li class="mobileUserMenuWrapper">
                        <UserMenu />
                    </li>
                </ul>
            </div>
        </div>
    </nav>
</template>

<style scoped>
.navbar {
    --nav-bg: #222;
    --nav-text: #fff;
    --accent: orangered; 
    --navbar-height: 70px;
    background-color: var(--nav-bg);
    color: var(--nav-text);
    height: var(--navbar-height);
    position: fixed;
    top: 0; left: 0; width: 100%; z-index: 1000;
}

.navbarContainer {
    width: 100%;
    height: 100%; 
    padding: 0 1rem;
    display: flex;
    align-items: center; 
    justify-content: space-between; 
}

.navLeft { 
    display: flex; 
    align-items: center; 
    gap: 30px; 
}

.logo img { 
    height: 40px; 
    width: auto; 
    display: block; 
}

.desktopLinks { 
    display: flex; 
    align-items: center; 
    gap: 1rem; 
    list-style: none; 
    margin: 0; 
    padding: 0; 
}

.navRight { 
    display: block; 
}

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
}

.navButton:hover:not(.router-link-exact-active) { 
    background-color: rgba(255, 255, 255, 0.1); 
}

.navButton.router-link-exact-active { 
    background-color: var(--accent); 
    color: #fff; font-weight: bold; 
    transform: translateY(-2px); 
    box-shadow: 0 4px 10px rgba(255, 69, 0, 0.4); 
}

.navButton:active, .navButton.router-link-exact-active:active { 
    transform: translateY(0) !important; 
    filter: brightness(0.85); 
}

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

/* Ensure UserMenu takes full width in mobile */
.mobileUserMenuWrapper { 
    display: block; 
    width: 100%; 
    padding: 0; 
    border: none; 
}

@media (max-width: 600px) {
    .desktopLinks, .navRight { 
        display: none; 
    }

    .hamburgerMenu { 
        display: block; 
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

    .navbarContainer { 
        padding: 0 1rem; 
    }
}

@media (min-width: 601px) {
    .hamburgerMenu, .mobileDropdown { 
        display: none !important; 
    }

    .desktopLinks, .navRight { 
        display: flex; 
    }
}

.mobileDropdown {
    position: absolute; 
    top: var(--navbar-height); 
    left: 0; width: 100%; 
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