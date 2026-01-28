<script setup>
import { ref, computed } from 'vue';
import axios from 'axios';

const props = defineProps({
    groupId: {
        type: [Number, String], // Allow null or special value if needed, though strictly we pass null or ID
        required: false,
        default: null
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
    <div v-if="isOpen" class="modalOverlay" @click.self="closeModal">
        <div class="modalContent">
            <div class="modalHeader">
                <h3>Create New Task</h3>
                <button class="closeBtn" @click="closeModal">&times;</button>
            </div>
            
            <div class="modalBody">
                <!-- Title -->
                <div class="formGroup">
                    <label>Title *</label>
                    <input 
                        v-model="title" 
                        type="text" 
                        placeholder="What needs to be done?"
                        autofocus
                    >
                </div>

                <!-- Description -->
                <div class="formGroup">
                    <label>Description</label>
                    <textarea 
                        v-model="description" 
                        rows="3" 
                        placeholder="Add more details..."
                    ></textarea>
                </div>

                <div class="row">
                    <!-- Priority -->
                    <div class="formGroup">
                        <label>Priority</label>
                        <select v-model="priority">
                            <option value="low">Low</option>
                            <option value="medium">Medium</option>
                            <option value="high">High</option>
                            <option value="urgent">Urgent</option>
                        </select>
                    </div>

                    <!-- Due Date -->
                    <div class="formGroup">
                        <label>Due Date</label>
                        <input 
                            v-model="dueDate" 
                            type="date" 
                            :min="minDate"
                        >
                    </div>
                </div>

                <div v-if="error" class="errorMessage">{{ error }}</div>
            </div>

            <div class="modalFooter">
                <button class="btnCancel" @click="closeModal" :disabled="isSubmitting">Cancel</button>
                <button class="btnCreate" @click="createTask" :disabled="isSubmitting">
                    {{ isSubmitting ? 'Creating...' : 'Create Task' }}
                </button>
            </div>
        </div>
    </div>
</template>

<style scoped>
.modalOverlay {
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

.modalContent {
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

.modalHeader {
    padding: 20px 24px;
    border-bottom: 1px solid var(--border-color);
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.modalHeader h3 {
    margin: 0;
    color: var(--c-text-primary);
    font-size: 1.2rem;
}

.closeBtn {
    background: none;
    border: none;
    color: var(--c-text-secondary);
    font-size: 2rem;
    line-height: 1;
    cursor: pointer;
    padding: 0;
}
.closeBtn:hover { color: var(--c-text-primary); }

.modalBody {
    padding: 24px;
    display: flex;
    flex-direction: column;
    gap: 20px;
}

.formGroup {
    display: flex;
    flex-direction: column;
    gap: 8px;
    flex: 1;
}

.formGroup label {
    font-size: 0.9rem;
    color: var(--c-text-secondary);
    font-weight: 600;
}

.formGroup input,
.formGroup textarea,
.formGroup select {
    background: var(--c-bg);
    border: 1px solid var(--border-color);
    color: var(--c-text-primary);
    padding: 10px 12px;
    border-radius: 8px;
    font-size: 0.95rem;
    outline: none;
    font-family: inherit;
}

.formGroup input:focus,
.formGroup textarea:focus,
.formGroup select:focus {
    border-color: var(--c-accent);
}

.row {
    display: flex;
    gap: 20px;
}

.errorMessage {
    color: #ef4444;
    font-size: 0.9rem;
    background: rgba(239, 68, 68, 0.1);
    padding: 10px;
    border-radius: 6px;
}

.modalFooter {
    padding: 20px 24px;
    border-top: 1px solid var(--border-color);
    display: flex;
    justify-content: flex-end;
    gap: 12px;
}

.btnCancel {
    background: transparent;
    border: 1px solid var(--border-color);
    color: var(--c-text-secondary);
    padding: 8px 16px;
    border-radius: 8px;
    cursor: pointer;
    font-weight: 600;
}
.btnCancel:hover { background: var(--c-bg); color: var(--c-text-primary); }

.btnCreate {
    background: var(--c-accent);
    border: none;
    color: white;
    padding: 8px 24px;
    border-radius: 8px;
    cursor: pointer;
    font-weight: 600;
}
.btnCreate:hover { filter: brightness(1.1); }
.btnCreate:disabled { opacity: 0.7; cursor: not-allowed; }

@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
@keyframes scaleUp { from { transform: scale(0.95); opacity: 0; } to { transform: scale(1); opacity: 1; } }
</style>
