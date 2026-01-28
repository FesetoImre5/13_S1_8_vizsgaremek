<script setup>
import { useToast } from '../composables/useToast';

const { toasts, removeToast } = useToast();
</script>

<template>
    <div class="toast-container">
        <transition-group name="toast">
            <div 
                v-for="toast in toasts" 
                :key="toast.id" 
                class="toast" 
                :class="toast.type"
                @click="removeToast(toast.id)"
            >
                <div class="toast-content">
                    <span v-if="toast.type === 'success'">✅</span>
                    <span v-else-if="toast.type === 'error'">❌</span>
                    <span v-else-if="toast.type === 'warning'">⚠️</span>
                    <span v-else>ℹ️</span>
                    <p>{{ toast.message }}</p>
                </div>
                <button class="close-btn">&times;</button>
            </div>
        </transition-group>
    </div>
</template>

<style scoped>
.toast-container {
    position: fixed;
    top: 20px;
    right: 20px;
    z-index: 9999;
    display: flex;
    flex-direction: column;
    gap: 10px;
    pointer-events: none; /* Let clicks pass through container */
}

.toast {
    pointer-events: auto; /* Re-enable clicks for toasts */
    min-width: 300px;
    max-width: 400px;
    background: var(--c-surface, #1E1E1E);
    color: var(--c-text-primary, #E5E7EB);
    padding: 16px;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    display: flex;
    align-items: center;
    justify-content: space-between;
    cursor: pointer;
    border-left: 4px solid var(--c-primary, #DC2626);
}

.toast.success { border-left-color: #16a34a; }
.toast.error { border-left-color: #dc2626; }
.toast.warning { border-left-color: #f59e0b; }
.toast.info { border-left-color: #3b82f6; }

.toast-content {
    display: flex;
    align-items: center;
    gap: 12px;
}

.toast-content p {
    margin: 0;
    font-size: 0.95rem;
    font-weight: 500;
}

.close-btn {
    background: transparent;
    border: none;
    color: var(--c-text-secondary, #9CA3AF);
    font-size: 1.2rem;
    cursor: pointer;
    margin-left: 10px;
}

.close-btn:hover {
    color: var(--c-text-primary, #E5E7EB);
}

/* Transitions */
.toast-enter-active,
.toast-leave-active {
    transition: all 0.3s ease;
}

.toast-enter-from {
    opacity: 0;
    transform: translateX(30px);
}

.toast-leave-to {
    opacity: 0;
    transform: translateX(30px);
}
</style>
