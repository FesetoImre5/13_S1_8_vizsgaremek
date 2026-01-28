<script setup>
import { ref, computed } from 'vue';
import axios from 'axios';

const props = defineProps({
    groupId: {
        type: Number,
        required: true
    },
    isOpen: {
        type: Boolean,
        default: false
    }
});

const emit = defineEmits(['close', 'task-created']);

const title = ref('');
const description = ref('');
const priority = ref('low'); // low, medium, high, urgent
const dueDate = ref('');
const isSubmitting = ref(false);
const error = ref('');

const minDate = computed(() => {
    const today = new Date();
    return today.toISOString().split('T')[0];
});

const closeModal = () => {
    emit('close');
    // Reset form
    title.value = '';
    description.value = '';
    priority.value = 'low';
    dueDate.value = '';
    error.value = '';
};

const createTask = async () => {
    if (!title.value.trim()) {
        error.value = 'Task title is required';
        return;
    }

    isSubmitting.value = true;
    error.value = '';

    try {
        const userId = parseInt(localStorage.getItem('user_id'));
        
        const payload = {
            group: props.groupId,
            created_by: userId,
            title: title.value,
            description: description.value,
            priority: priority.value,
            due_date: dueDate.value ? new Date(dueDate.value).toISOString() : null,
            status: 'todo'
        };

        const response = await axios.post('http://127.0.0.1:8000/api/tasks/', payload);
        
        emit('task-created', response.data);
        closeModal();

    } catch (err) {
        console.error('Failed to create task:', err);
        if (err.response && err.response.data) {
            error.value = err.response.data.detail || 'Failed to create task';
        } else {
            error.value = 'Network error. Please try again.';
        }
    } finally {
        isSubmitting.value = false;
    }
};
</script>

<template>
    <div v-if="isOpen" class="modal-overlay" @click.self="closeModal">
        <div class="modal-content">
            <div class="modal-header">
                <h3>Create New Task</h3>
                <button class="close-btn" @click="closeModal">&times;</button>
            </div>
            
            <div class="modal-body">
                <!-- Title -->
                <div class="form-group">
                    <label>Title *</label>
                    <input 
                        v-model="title" 
                        type="text" 
                        placeholder="What needs to be done?"
                        autofocus
                    >
                </div>

                <!-- Description -->
                <div class="form-group">
                    <label>Description</label>
                    <textarea 
                        v-model="description" 
                        rows="3" 
                        placeholder="Add more details..."
                    ></textarea>
                </div>

                <div class="row">
                    <!-- Priority -->
                    <div class="form-group">
                        <label>Priority</label>
                        <select v-model="priority">
                            <option value="low">Low</option>
                            <option value="medium">Medium</option>
                            <option value="high">High</option>
                            <option value="urgent">Urgent</option>
                        </select>
                    </div>

                    <!-- Due Date -->
                    <div class="form-group">
                        <label>Due Date</label>
                        <input 
                            v-model="dueDate" 
                            type="date" 
                            :min="minDate"
                        >
                    </div>
                </div>

                <div v-if="error" class="error-message">{{ error }}</div>
            </div>

            <div class="modal-footer">
                <button class="btn-cancel" @click="closeModal" :disabled="isSubmitting">Cancel</button>
                <button class="btn-create" @click="createTask" :disabled="isSubmitting">
                    {{ isSubmitting ? 'Creating...' : 'Create Task' }}
                </button>
            </div>
        </div>
    </div>
</template>

<style scoped>
.modal-overlay {
    position: fixed;
    top: 0; left: 0;
    width: 100vw; height: 100vh;
    background: rgba(0, 0, 0, 0.8);
    backdrop-filter: blur(5px);
    z-index: 2000;
    display: flex;
    justify-content: center;
    align-items: center;
    animation: fadeIn 0.2s ease;
}

.modal-content {
    background: var(--c-surface);
    width: 90%;
    max-width: 500px;
    border-radius: 16px;
    border: 1px solid var(--border-color);
    box-shadow: 0 20px 50px rgba(0,0,0,0.5);
    display: flex;
    flex-direction: column;
    overflow: hidden;
    animation: scaleUp 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

.modal-header {
    padding: 20px 24px;
    border-bottom: 1px solid var(--border-color);
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.modal-header h3 {
    margin: 0;
    color: var(--c-text-primary);
    font-size: 1.2rem;
}

.close-btn {
    background: none;
    border: none;
    color: var(--c-text-secondary);
    font-size: 2rem;
    line-height: 1;
    cursor: pointer;
    padding: 0;
}
.close-btn:hover { color: var(--c-text-primary); }

.modal-body {
    padding: 24px;
    display: flex;
    flex-direction: column;
    gap: 20px;
}

.form-group {
    display: flex;
    flex-direction: column;
    gap: 8px;
    flex: 1;
}

.form-group label {
    font-size: 0.9rem;
    color: var(--c-text-secondary);
    font-weight: 600;
}

.form-group input,
.form-group textarea,
.form-group select {
    background: var(--c-bg);
    border: 1px solid var(--border-color);
    color: var(--c-text-primary);
    padding: 10px 12px;
    border-radius: 8px;
    font-size: 0.95rem;
    outline: none;
    font-family: inherit;
}

.form-group input:focus,
.form-group textarea:focus,
.form-group select:focus {
    border-color: var(--c-accent);
}

.row {
    display: flex;
    gap: 20px;
}

.error-message {
    color: #ef4444;
    font-size: 0.9rem;
    background: rgba(239, 68, 68, 0.1);
    padding: 10px;
    border-radius: 6px;
}

.modal-footer {
    padding: 20px 24px;
    border-top: 1px solid var(--border-color);
    display: flex;
    justify-content: flex-end;
    gap: 12px;
}

.btn-cancel {
    background: transparent;
    border: 1px solid var(--border-color);
    color: var(--c-text-secondary);
    padding: 8px 16px;
    border-radius: 8px;
    cursor: pointer;
    font-weight: 600;
}
.btn-cancel:hover { background: var(--c-bg); color: var(--c-text-primary); }

.btn-create {
    background: var(--c-accent);
    border: none;
    color: white;
    padding: 8px 24px;
    border-radius: 8px;
    cursor: pointer;
    font-weight: 600;
}
.btn-create:hover { filter: brightness(1.1); }
.btn-create:disabled { opacity: 0.7; cursor: not-allowed; }

@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
@keyframes scaleUp { from { transform: scale(0.95); opacity: 0; } to { transform: scale(1); opacity: 1; } }
</style>
