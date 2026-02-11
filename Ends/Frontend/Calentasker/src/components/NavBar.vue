<script setup>
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router'; // Import useRouter
import { useI18n } from 'vue-i18n';
import { useAuth } from '../composables/UseAuth';  

const { user, logout } = useAuth(); // Destructure logout
const router = useRouter(); // Use router
const { t, locale } = useI18n();
const isMenuOpen = ref(false);

const toggleLanguage = () => {
    locale.value = locale.value === 'en' ? 'hu' : 'en';
};

const navLinks = computed(() => {
    if (user.value) {
        return [
            { key: 'nav.tasks', path: '/tasks' },
            { key: 'nav.groups', path: '/groups' } // Add Groups link
        ];
    }
    return []; 
});

const handleLogout = () => {
    logout();
    router.push('/auth');
};
</script>

<template>
    <nav class="navbar">
        <div class="navbarContainer">
            <!-- GROUP 1 (LEFT): Logo + Tasks Button -->
            <div class="navLeft">
                <div class="logo">
                    <router-link to="/tasks">
                        <img src="../assets/logo-with-text.svg" alt="Calentasker" class="logo-full">
                        <img src="../assets/logo.svg" alt="Calentasker" class="logo-icon">
                    </router-link>
                </div>
                <ul class="desktopLinks">
                    <li v-for="link in navLinks" :key="link.path">
                        <router-link :to="link.path" class="navButton">
                            {{ $t(link.key) }}
                        </router-link>
                    </li>
                </ul>
            </div>

            <!-- GROUP 2 (RIGHT): User Controls -->
            <div class="navRight">
                <!-- Lang Button Always Visible -->
                <button class="langBtn" @click="toggleLanguage">
                    <img 
                        :src="locale === 'en' 
                            ? 'https://hatscripts.github.io/circle-flags/flags/hu.svg' 
                            : 'https://hatscripts.github.io/circle-flags/flags/gb.svg'" 
                        alt="Switch Language"
                        class="flag-icon"
                    >
                </button>

                <template v-if="user">
                    <router-link to="/profile" class="usernameLink">
                        {{ user.display_username || user.username }}
                    </router-link>
                    <button class="logoutBtn" @click="handleLogout">
                        {{ $t('nav.logout') }}
                    </button>
                </template>
                <template v-else>
                     <router-link to="/auth" class="navButton">{{ $t('nav.login') }}</router-link>
                </template>
            </div>

            <!-- MOBILE RIGHT BUNDLE -->
            <div class="navMobileRight">
                <button class="mobileLangBtn" @click="toggleLanguage">
                    <img 
                        :src="locale === 'en' 
                            ? 'https://hatscripts.github.io/circle-flags/flags/hu.svg' 
                            : 'https://hatscripts.github.io/circle-flags/flags/gb.svg'" 
                        alt="Switch Language"
                        class="flag-icon"
                    >
                </button>
                
                <div class="hamburgerMenu">
                    <button 
                        class="hamburgerBtn" 
                        @click="isMenuOpen = !isMenuOpen"
                        aria-label="Toggle menu"
                    >
                        <img src="../assets/list.svg" alt="Menu" class="hamburgerIcon">
                    </button>
                </div>
            </div>
        </div>

        <!-- MOBILE DROPDOWN -->
        <div class="mobileDropdown" :class="{ 'isOpen': isMenuOpen }">
            <div class="mobileDropdownInner">
                <ul>
                    <li v-for="link in navLinks" :key="link.path">
                        <router-link 
                            :to="link.path" 
                            @click="isMenuOpen = false"
                            class="mobileButton"
                        >
                            {{ $t(link.key) }}
                        </router-link>
                    </li>
                    <!-- Mobile User Controls -->
                     <li v-if="user" class="mobileUserControls">
                        <router-link to="/profile" class="mobileButton" @click="isMenuOpen = false">
                            {{ $t('nav.profile') }} ({{ user.display_username || user.username }})
                        </router-link>
                        <button class="mobileButton logout" @click="handleLogout(); isMenuOpen = false">
                            {{ $t('nav.logout') }}
                        </button>
                    </li>
                    <li v-else>
                         <router-link to="/auth" class="mobileButton" @click="isMenuOpen=false">{{ $t('nav.login') }}</router-link>
                    </li>
                </ul>
            </div>
        </div>
    </nav>
</template>

<style scoped>
/* --- CONFIGURATION --- */
.navbar {
    /* Mapping to Global Variables defined in App.vue */
    --nav-bg: var(--c-surface);      /* Dark Gray */
    --nav-text: var(--c-text-primary);
    --accent: var(--c-accent);       /* Orange */
    --navbar-height: 70px;
    
    background-color: var(--nav-bg);
    color: var(--nav-text);
    height: var(--navbar-height);
    border-bottom: 1px solid var(--border-color);
    
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    z-index: 2000;
}

.navbarContainer {
    width: 100%; 
    height: 100%;
    padding: 0 2rem; 
    display: flex;
    align-items: center;
    justify-content: space-between; 
}

/* --- GROUP 1 (LEFT) --- */
.navLeft {
    display: flex;
    align-items: center;
    gap: 30px; 
}

.logo a {
    display: flex;
    align-items: center;
}

.logo-full { display: block; height: 35px; width: auto; }
.logo-icon { display: none; }

@media (max-width: 480px) {
    .logo-full { display: none; }
    .logo-icon { display: block; height: 32px; width: auto; }
}

.desktopLinks {
    display: flex;
    align-items: center;
    gap: 1rem;
    list-style: none;
    margin: 0;
    padding: 0;
}

/* --- GROUP 2 (RIGHT) --- */
.navRight {
    display: flex;
    align-items: center;
    gap: 15px;
}

.usernameLink {
    text-decoration: none;
    color: var(--nav-text);
    font-weight: 500;
    font-size: 1rem;
    transition: color 0.2s;
}

.usernameLink:hover {
    color: var(--accent);
}

.logoutBtn {
    background-color: transparent;
    border: 1px solid var(--c-primary); /* Red/Orange border */
    color: var(--c-primary);
    padding: 0.5rem 1rem;
    border-radius: 6px;
    cursor: pointer;
    font-weight: 500;
    transition: all 0.2s;
}

.logoutBtn:hover {
    background-color: var(--c-primary);
    color: white;
}

/* --- BUTTON STYLES --- */
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
    background-color: var(--c-surface-hover);
}

.navButton.router-link-exact-active {
    background-color: var(--accent);
    color: #fff;
    font-weight: bold;
    transform: translateY(-2px); 
    box-shadow: 0 4px 10px rgba(249, 115, 22, 0.4);
}

.navButton:active,
.navButton.router-link-exact-active:active {
    transform: translateY(0) !important; 
    filter: brightness(0.85);
}

/* --- MOBILE STYLES --- */
.mobileButton {
    text-decoration: none;
    color: var(--nav-text);
    font-size: 1.1rem;
    display: block;
    padding: 1.2rem;
    text-align: center;
    border-bottom: 1px solid var(--border-color);
    background-color: transparent;
    border-left: none;
    border-right: none;
    border-top: none;
    width: 100%;
    transition: background-color 0.2s ease;
    cursor: pointer;
}

.mobileButton:hover {
    background-color: var(--c-surface-hover);
}

.mobileButton.router-link-exact-active {
    background-color: var(--accent);
    color: #fff;
    font-weight: bold;
    border-bottom: 1px solid var(--accent);
}

.mobileButton.logout {
    color: var(--c-primary);
}

.mobileUserControls {
    display: flex;
    flex-direction: column;
}

/* --- LANGUAGE SWITCHER --- */
.langBtn {
    background: transparent;
    border: 2px solid #ffffff; /* White outline */
    padding: 0;
    border-radius: 50%;
    cursor: pointer;
    transition: all 0.2s;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 34px;
    height: 34px;
    overflow: hidden;
}
.langBtn:hover {
    border-color: var(--accent);
    transform: scale(1.05);
}

.mobileLangBtn {
    display: none; 
    background: transparent;
    border: 2px solid #ffffff; /* White outline */
    padding: 0;
    border-radius: 50%;
    margin-right: 15px; 
    cursor: pointer;
    display: flex; /* alignment */
    align-items: center;
    justify-content: center;
    width: 32px;
    height: 32px;
    overflow: hidden;
}

.flag-icon {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
}

.navMobileRight {
    display: none; /* Hidden by default on desktop */
    align-items: center;
    gap: 10px; /* Space between lang button and hamburger */
}

/* =========================================
    MEDIA QUERIES
   ========================================= */

@media (max-width: 600px) {
    .desktopLinks, 
    .navRight { 
        display: none; 
    }
    
    .navMobileRight {
        display: flex;
    }

    .hamburgerMenu, .mobileLangBtn {
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
        filter: invert(1); /* Invert to make white on dark bg */
        display: block;
    }
    
    .navbarContainer {
        padding: 0 1rem;
    }
}

@media (min-width: 601px) {
    .hamburgerMenu, .mobileDropdown, .mobileLangBtn, .navMobileRight {
        display: none !important;
    }

    .desktopLinks, 
    .navRight { 
        display: flex; 
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
    
    /* Dark Surface */
    background-color: var(--nav-bg); 
    border-bottom: 1px solid var(--border-color);
    
    display: grid;
    grid-template-rows: 0fr;
    transition: grid-template-rows 0.3s ease-out;
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.5);
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