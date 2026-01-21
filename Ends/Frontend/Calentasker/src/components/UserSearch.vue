<script setup>
import { ref, watch } from 'vue';
import axios from 'axios';

const props = defineProps({
    placeholder: {
        type: String,
        default: 'Search by email or name...'
    },
    exclude: { // Array of user IDs to exclude from results
        type: Array,
        default: () => []
    }
});

const emit = defineEmits(['select']);

const searchQuery = ref('');
const results = ref([]);
const isLoading = ref(false);
const showDropdown = ref(false);
const searchInput = ref(null);

let debounceTimeout = null;

const performSearch = async () => {
    console.log('UserSearch: performing search for', searchQuery.value);
    if (!searchQuery.value.trim()) {
        results.value = [];
        showDropdown.value = false;
        return;
    }

    isLoading.value = true;
    try {
        const response = await axios.get(`http://127.0.0.1:8000/api/users/search/?q=${encodeURIComponent(searchQuery.value)}`);
        console.log('UserSearch: API response', response.data);
        // Filter out excluded users
        results.value = response.data.filter(user => !props.exclude.includes(user.id));
        console.log('UserSearch: Filtered results', results.value);
        showDropdown.value = true;
    } catch (error) {
        console.error('Search failed:', error);
    } finally {
        isLoading.value = false;
    }
};

const handleInput = () => {
    if (debounceTimeout) clearTimeout(debounceTimeout);
    debounceTimeout = setTimeout(performSearch, 300);
};

const selectUser = (user) => {
    emit('select', user);
    searchQuery.value = '';
    results.value = [];
    showDropdown.value = false;
    // Keep focus (optional)
    // searchInput.value.focus();
};

const closeDropdown = () => {
    // Delay to allow click to register
    setTimeout(() => {
        showDropdown.value = false;
    }, 200);
};

</script>

<template>
    <div class="user-search-container">
        <div class="input-wrapper">
            <input 
                ref="searchInput"
                type="text" 
                v-model="searchQuery" 
                :placeholder="placeholder"
                @input="handleInput"
                @focus="performSearch"
                @blur="closeDropdown"
                class="search-input"
            >
            <div v-if="isLoading" class="spinner"></div>
        </div>

        <ul v-if="showDropdown && results.length > 0" class="results-dropdown">
            <li v-for="user in results" :key="user.id" @mousedown.prevent="selectUser(user)" class="result-item">
                <div class="user-avatar">
                   <img v-if="user.profile_picture" :src="user.profile_picture" alt="Avatar">
                   <div v-else class="avatar-placeholder">{{ (user.first_name?.[0] || user.display_username?.[0] || user.email?.[0] || '?').toUpperCase() }}</div>
                </div>
                <div class="user-info">
                    <span class="user-name">{{ user.display_username || user.first_name + ' ' + user.last_name }}</span>
                    <span class="user-email">{{ user.email }}</span>
                </div>
            </li>
        </ul>
        <div v-if="showDropdown && searchQuery && !isLoading && results.length === 0" class="no-results">
            No users found.
        </div>
    </div>
</template>

<style scoped>
.user-search-container {
    position: relative;
    width: 100%;
}

.input-wrapper {
    position: relative;
}

.search-input {
    width: 100%;
    padding: 10px 12px;
    padding-right: 30px;
    border: 1px solid var(--border-color, #ccc);
    border-radius: 8px;
    background: var(--c-bg, #fff);
    color: var(--c-text-primary, #000);
    font-size: 0.95rem;
    outline: none;
}

.search-input:focus {
    border-color: var(--c-accent, #ff4400);
    box-shadow: 0 0 0 1px var(--c-accent, #ff4400);
}

.spinner {
    position: absolute;
    right: 10px;
    top: 50%;
    transform: translateY(-50%);
    width: 16px;
    height: 16px;
    border: 2px solid rgba(0,0,0,0.1);
    border-left-color: var(--c-accent, #ff4400);
    border-radius: 50%;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    to { transform: translateY(-50%) rotate(360deg); }
}

.results-dropdown {
    position: absolute;
    top: 100%;
    left: 0;
    right: 0;
    margin: 4px 0 0;
    padding: 0;
    list-style: none;
    background: var(--c-surface, #fff);
    border: 1px solid var(--border-color, #ccc);
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    z-index: 1000;
    max-height: 250px;
    overflow-y: auto;
}

.result-item {
    display: flex;
    align-items: center;
    padding: 10px 12px;
    cursor: pointer;
    transition: background-color 0.1s;
    border-bottom: 1px solid var(--border-color-light, rgba(0,0,0,0.05));
}

.result-item:last-child {
    border-bottom: none;
}

.result-item:hover {
    background-color: var(--c-bg-hover, rgba(0,0,0,0.05));
}

.user-avatar {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    overflow: hidden;
    margin-right: 12px;
    background: #eee;
    flex-shrink: 0;
    display: flex;
    align-items: center;
    justify-content: center;
}

.user-avatar img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.avatar-placeholder {
    color: #666;
    font-weight: bold;
    font-size: 14px;
}

.user-info {
    display: flex;
    flex-direction: column;
    overflow: hidden;
}

.user-name {
    font-weight: 600;
    color: var(--c-text-primary, #000);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.user-email {
    font-size: 0.8rem;
    color: var(--c-text-secondary, #666);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.no-results {
    position: absolute;
    top: 100%;
    left: 0;
    right: 0;
    padding: 12px;
    background: var(--c-surface, #fff);
    border: 1px solid var(--border-color, #ccc);
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    z-index: 1000;
    color: var(--c-text-secondary, #666);
    text-align: center;
    margin-top: 4px;
}
</style>
