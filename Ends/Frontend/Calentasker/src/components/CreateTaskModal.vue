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
const startDate = ref('');
const isSubmitting = ref(false);
    const error = ref('');

    // New Refs
    const selectedAssignees = ref([]);
    const assigneeSearch = ref('');
    const showAssignDropdown = ref(false);
    const imageUrl = ref('');
    const imageFile = ref(null);
    const imageMode = ref('upload'); 
    const groupMembers = ref([]);
    const loadingMembers = ref(false);

    // Filter members for dropdown (exclude already selected)
    const filteredMembers = computed(() => {
        const search = assigneeSearch.value.toLowerCase();
        return groupMembers.value.filter(m => {
            const isSelected = selectedAssignees.value.some(sel => sel.id === m.id);
            const matchesSearch = m.user_detail.username.toLowerCase().includes(search);
            return !isSelected && matchesSearch;
        });
    });

    const minDate = computed(() => {
        const today = new Date();
        return today.toISOString().split('T')[0];
    });

    // Methods for multi-assign
    const selectAssignee = (member) => {
        selectedAssignees.value.push(member);
        assigneeSearch.value = '';
    };

    const removeAssignee = (memberId) => {
        selectedAssignees.value = selectedAssignees.value.filter(m => m.id !== memberId);
    };
    
    const closeDropdown = () => {
        showAssignDropdown.value = false;
    }

    // Fetch members when modal opens
    import { watch } from 'vue';
    watch(() => props.isOpen, async (newVal) => {
        if (newVal && props.groupId && typeof props.groupId === 'number') {
            loadingMembers.value = true;
            // Reset fields
            title.value = '';
            description.value = '';
            priority.value = 'low';
            dueDate.value = '';
            startDate.value = '';
            selectedAssignees.value = [];
            assigneeSearch.value = '';
            imageUrl.value = '';
            imageFile.value = null;
            imageMode.value = 'upload';
            
            try {
                const response = await axios.get(`http://127.0.0.1:8000/api/group-members/?group=${props.groupId}`);
                groupMembers.value = response.data;
            } catch (e) {
                console.error("Failed to fetch members", e);
            } finally {
                loadingMembers.value = false;
            }
        } else if (newVal) {
            // Own Tasks (No Group)
            loadingMembers.value = true;
            try {
                const userId = parseInt(localStorage.getItem('user_id'));
                if (userId) {
                    const response = await axios.get(`http://127.0.0.1:8000/api/users/${userId}/`);
                    const user = response.data;
                    const meMember = {
                        id: 'self',
                        user_detail: user,
                        role: 'Owner'
                    };
                    groupMembers.value = [meMember];
                    selectedAssignees.value = [meMember];
                } else {
                     groupMembers.value = [];
                }
            } catch (e) {
                console.error("Failed to fetch user for auto-assignment", e);
                groupMembers.value = [];
            } finally {
                loadingMembers.value = false;
            }
        }
    });

    const handleFileChange = (e) => {
        const file = e.target.files[0];
        if (file) {
            imageFile.value = file;
            imageUrl.value = ''; // Clear URL if file selected, avoiding confusion
        }
    };

    const closeModal = () => {
        emit('close');
        // Reset form
        title.value = '';
        description.value = '';
        priority.value = 'low';
        dueDate.value = '';
        startDate.value = '';
        error.value = '';
        assignedUserId.value = null;
        imageUrl.value = '';
        imageFile.value = null;
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
            
            const formData = new FormData();
            if (props.groupId) formData.append('group', props.groupId);
            formData.append('created_by_userid', userId); // Changed from created_by to match serializer
            formData.append('title', title.value);
            formData.append('description', description.value);
            formData.append('priority', priority.value);
            
            if (startDate.value) {
                formData.append('start_date', startDate.value);
            }
            if (dueDate.value) {
                // Ensure YYYY-MM-DD format
                formData.append('due_date', dueDate.value);
            }
            formData.append('status', 'todo');
            
            // Append Multiple Assignees
            selectedAssignees.value.forEach(member => {
                 formData.append('assignee_ids', member.user_detail.id);
            });

            if (imageFile.value) {
                formData.append('image', imageFile.value);
            } else if (imageUrl.value) {
                formData.append('imageUrl', imageUrl.value);
            }

            const response = await axios.post('http://127.0.0.1:8000/api/tasks/', formData, {
                headers: { 'Content-Type': 'multipart/form-data' }
            });
            
            emit('task-created', response.data);
            closeModal();

        } catch (err) {
            console.error('Failed to create task:', err);
            if (err.response && err.response.data) {
                error.value = JSON.stringify(err.response.data); // Better error debug
            } else {
                error.value = 'Network error. Please try again.';
            }
        } finally {
            isSubmitting.value = false;
        }
    };
</script>

<template>
    <div v-if="isOpen" class="modalOverlay" @click.self="closeModal" @click="closeDropdown">
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

                    <!-- Start Date -->
                    <div class="formGroup">
                        <label>Start Date</label>
                        <input 
                            v-model="startDate" 
                            type="date" 
                        >
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

                <!-- NEW: Assign To (Multiple) -->
                <div class="formGroup">
                    <label>Assign To</label>
                    <div class="multi-select-container" :class="{ disabled: loadingMembers }" @click.stop>
                        <!-- Selected Chips -->
                        <div class="chips-area">
                            <div v-for="user in selectedAssignees" :key="user.id" class="user-chip">
                                <img 
                                    v-if="user.user_detail.profile_picture" 
                                    :src="user.user_detail.profile_picture.startsWith('http') ? user.user_detail.profile_picture : 'http://127.0.0.1:8000' + user.user_detail.profile_picture" 
                                    class="chip-avatar"
                                >
                                <div v-else class="chip-avatar-placeholder">
                                    {{ (user.user_detail.username?.[0] || '?').toUpperCase() }}
                                </div>
                                <span>{{ user.user_detail.username }}</span>
                                <button class="chip-remove" @click.stop="removeAssignee(user.id)">&times;</button>
                            </div>
                            
                            <!-- Search Input -->
                            <input 
                                type="text" 
                                v-model="assigneeSearch" 
                                placeholder="Search members..." 
                                class="assign-input"
                                @focus="showAssignDropdown = true"
                                :disabled="loadingMembers"
                            >
                        </div>
                        
                        <!-- Dropdown Options -->
                        <div v-if="showAssignDropdown && filteredMembers.length > 0" class="assign-dropdown" @click.stop>
                            <div 
                                v-for="member in filteredMembers" 
                                :key="member.id" 
                                class="assign-option"
                                @click="selectAssignee(member)"
                            >
                                <img 
                                    v-if="member.user_detail.profile_picture" 
                                    :src="member.user_detail.profile_picture.startsWith('http') ? member.user_detail.profile_picture : 'http://127.0.0.1:8000' + member.user_detail.profile_picture" 
                                    class="option-avatar"
                                >
                                <div v-else class="option-avatar-placeholder">
                                    {{ (member.user_detail.username?.[0] || '?').toUpperCase() }}
                                </div>
                                <span class="option-name">{{ member.user_detail.username }}</span>
                                <span class="option-role">{{ member.role }}</span>
                            </div>
                        </div>
                        <div v-if="showAssignDropdown && filteredMembers.length === 0 && assigneeSearch" class="assign-dropdown">
                             <div class="no-results">No members found</div>
                        </div>
                    </div>
                </div>

                <!-- NEW: Cover Image -->
                <div class="formGroup">
                    <div class="label-row">
                        <label>Cover Image</label>
                        <div class="toggle-switch">
                            <span :class="{ active: imageMode === 'upload' }" @click="imageMode = 'upload'">Upload</span>
                            <span :class="{ active: imageMode === 'url' }" @click="imageMode = 'url'">URL</span>
                        </div>
                    </div>

                    <div v-if="imageMode === 'url'">
                        <input type="text" v-model="imageUrl" placeholder="Image URL (http://...)" class="url-input">
                    </div>
                    
                    <div v-else>
                        <div class="file-upload-wrapper">
                            <label for="cover-upload" class="file-label">
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="17 8 12 3 7 8"></polyline><line x1="12" y1="3" x2="12" y2="15"></line></svg>
                                {{ imageFile ? imageFile.name : 'Upload File' }}
                            </label>
                            <input id="cover-upload" type="file" @change="handleFileChange" accept="image/*" style="display: none;">
                        </div>
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

/* NEW STYLES for Image Inputs */
.label-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
}
.toggle-switch {
    display: flex;
    background: var(--c-bg); /* Darker background */
    border-radius: 6px;
    padding: 2px;
    border: 1px solid var(--border-color);
}
.toggle-switch span {
    padding: 4px 12px;
    font-size: 0.8rem;
    cursor: pointer;
    border-radius: 4px;
    color: var(--c-text-secondary);
    font-weight: 600;
    transition: all 0.2s;
}
.toggle-switch span.active {
    background: var(--c-accent); /* Active Color */
    color: white;
}

.url-input {
    width: 100%;
}
.file-upload-wrapper {
    display: flex;
}
.file-label {
    display: flex;
    align-items: center;
    justify-content: flex-start; /* Aligned left as requested */
    gap: 12px; /* Increased space */
    background: #0d0d0d; /* Very dark background to match image */
    border: 1px dashed #333; /* Darker dashed border */
    padding: 14px 16px; /* Slightly more padding */
    border-radius: 8px;
    cursor: pointer;
    width: 100%;
    color: var(--c-text-secondary);
    transition: all 0.2s;
}
.file-label svg {
    display: block; /* Removes inline spacing */
}
.file-label span {
    line-height: 1; /* Helps with vertical centering alignment */
    padding-top: 2px; /* Optical adjustment if needed */
}
.file-label:hover {
    border-color: var(--c-accent);
    color: var(--c-accent);
    background: rgba(255, 255, 255, 0.05);
}

/* Multi-Assign Styles */
.multi-select-container {
    background: var(--c-bg);
    border: 1px solid var(--border-color);
    border-radius: 10px;
    padding: 8px;
    position: relative;
    min-height: 48px;
}
.multi-select-container.disabled {
    opacity: 0.7;
    pointer-events: none;
}
.chips-area {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    align-items: center;
}
.user-chip {
    display: flex;
    align-items: center;
    background: var(--c-surface); /* Keep surface to distinguish from container bg */
    border: 1px solid var(--border-color);
    border-radius: 20px;
    padding: 4px 12px 4px 4px;
    font-size: 0.9rem;
    color: var(--c-text-primary); /* Ensure text is visible */
}
.chip-avatar {
    width: 24px;
    height: 24px;
    border-radius: 50%;
    margin-right: 8px;
    object-fit: cover;
}
.chip-avatar-placeholder {
    width: 24px;
    height: 24px;
    border-radius: 50%;
    margin-right: 8px;
    background: var(--c-accent);
    color: white;
    font-size: 0.7rem;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
}
.chip-remove {
    background: none;
    border: none;
    margin-left: 8px;
    cursor: pointer;
    color: var(--c-text-secondary);
    font-size: 1.1rem;
    padding: 0;
    line-height: 1;
    display: flex;
    align-items: center;
}
.chip-remove:hover {
    color: #ef4444;
}

.assign-input {
    border: none;
    background: transparent;
    color: var(--c-text-primary);
    outline: none;
    flex: 1;
    min-width: 120px;
    padding: 4px;
    font-size: 0.9rem;
}
.assign-input::placeholder {
    color: var(--c-text-secondary);
    opacity: 0.6;
}

.assign-dropdown {
    position: absolute;
    top: 100%;
    left: 0;
    right: 0;
    background: var(--c-surface);
    border: 1px solid var(--border-color);
    border-radius: 10px;
    margin-top: 4px;
    max-height: 200px;
    overflow-y: auto;
    z-index: 10;
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
}
.assign-option {
    padding: 8px 12px;
    display: flex;
    align-items: center;
    cursor: pointer;
    transition: background 0.2s;
    color: var(--c-text-primary); /* Ensure text is visible */
}
.assign-option:hover {
    background: rgba(255, 255, 255, 0.05);
}
.option-avatar {
    width: 28px;
    height: 28px;
    border-radius: 50%;
    margin-right: 10px;
    object-fit: cover;
}
.option-avatar-placeholder {
     width: 28px;
    height: 28px;
    border-radius: 50%;
    margin-right: 10px;
    background: #555;
    color: white;
    font-size: 0.8rem;
    display: flex;
    align-items: center;
    justify-content: center;
}
.option-name {
    flex: 1;
    font-size: 0.9rem;
    font-weight: 500;
}
.option-role {
    font-size: 0.75rem;
    padding: 2px 6px;
    border-radius: 4px;
    background: rgba(255, 255, 255, 0.1);
    color: var(--c-text-secondary);
}
.no-results {
    padding: 12px;
    text-align: center;
    color: var(--c-text-secondary);
    font-size: 0.9rem;
}
</style>
