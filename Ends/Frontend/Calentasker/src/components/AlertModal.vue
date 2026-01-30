<script setup>
defineProps({
    isOpen: Boolean,
    title: {
        type: String,
        default: 'Are you sure?'
    },
    message: String,
    confirmText: {
        type: String,
        default: 'Confirm'
    },
    cancelText: {
        type: String,
        default: 'Cancel'
    },
    type: {
        type: String,
        default: 'danger', // danger, info, success
        validator: (value) => ['danger', 'info', 'success', 'warning'].includes(value)
    }
});

const emit = defineEmits(['close', 'confirm']);
</script>

<template>
    <div v-if="isOpen" class="alert-overlay" @click.self="emit('close')">
        <div class="alert-content">
            <h3 :class="type">{{ title }}</h3>
            <p>{{ message }}</p>
            
            <div class="alert-actions">
                <button class="btn-cancel" @click="emit('close')">{{ cancelText }}</button>
                <button 
                    class="btn-confirm" 
                    :class="type" 
                    @click="emit('confirm')"
                >
                    {{ confirmText }}
                </button>
            </div>
        </div>
    </div>
</template>

<style scoped>
.alert-overlay {
    position: fixed;
    top: 0; left: 0;
    width: 100vw; height: 100vh;
    background: rgba(0, 0, 0, 0.85);
    backdrop-filter: blur(4px);
    z-index: 3000; /* Higher than other modals */
    display: flex;
    justify-content: center;
    align-items: center;
    animation: fadeIn 0.2s ease;
}

.alert-content {
    background: var(--c-surface);
    border: 1px solid var(--border-color);
    padding: 24px;
    border-radius: 12px;
    border-radius: 12px;
    width: 90%;
    max-width: 400px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.6);
    animation: scaleUp 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    text-align: center;
}

h3 {
    margin-top: 0;
    margin-bottom: 12px;
    font-size: 1.2rem;
}

h3.danger { color: #ef4444; }
h3.warning { color: #f59e0b; }
h3.info { color: var(--c-text-primary); }
h3.success { color: #10b981; }

p {
    color: var(--c-text-secondary);
    margin-bottom: 24px;
    line-height: 1.5;
}

.alert-actions {
    display: flex;
    gap: 12px;
    justify-content: center;
}

button {
    padding: 10px 20px;
    border-radius: 8px;
    font-weight: 600;
    cursor: pointer;
    border: none;
    font-size: 0.95rem;
    transition: filter 0.2s;
}

.btn-cancel {
    background: transparent;
    border: 1px solid var(--border-color);
    color: var(--c-text-primary);
}
.btn-cancel:hover { background: var(--c-bg); }

.btn-confirm.danger { background: #ef4444; color: white; }
.btn-confirm.warning { background: #f59e0b; color: white; }
.btn-confirm.info { background: var(--c-accent); color: white; }
.btn-confirm.success { background: #10b981; color: white; }
.btn-confirm:hover { filter: brightness(1.1); }

@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
@keyframes scaleUp { from { transform: scale(0.9); opacity: 0; } to { transform: scale(1); opacity: 1; } }
</style>
