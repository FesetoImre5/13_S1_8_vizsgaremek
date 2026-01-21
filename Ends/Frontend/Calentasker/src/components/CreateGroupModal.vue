<script setup>
import { ref } from 'vue';
import axios from 'axios';

const emit = defineEmits(['close', 'groupCreated']);

// Form state
const groupTitle = ref('');
const groupDescription = ref('');
const coverImage = ref(null);
const coverImagePreview = ref('');
const memberUsernames = ref('');
const isSubmitting = ref(false);
const error = ref('');
const success = ref('');

// Handle image upload
const handleImageUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
        coverImage.value = file;
        const reader = new FileReader();
        reader.onload = (e) => {
            coverImagePreview.value = e.target.result;
        };
        reader.readAsDataURL(file);
    }
};

// Remove uploaded image
const removeImage = () => {
    coverImage.value = null;
    coverImagePreview.value = '';
};

// Create group
const createGroup = async () => {
    error.value = '';
    success.value = '';
    
    if (!groupTitle.value.trim()) {
        error.value = 'Group title is required';
        return;
    }
    
    isSubmitting.value = true;
    
    try {
        // Create FormData for file upload
        const formData = new FormData();
        formData.append('groupname', groupTitle.value);
        if (groupDescription.value.trim()) {
            formData.append('description', groupDescription.value);
        }
        if (coverImage.value) {
            formData.append('imageUrl', coverImage.value);
        }
        
        // Create the group
        const response = await axios.post('http://127.0.0.1:8000/api/groups/', formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        });
        
        const newGroup = response.data;
        
        // Add members if specified
        if (memberUsernames.value.trim()) {
            const usernames = memberUsernames.value.split(',').map(u => u.trim()).filter(u => u);
            for (const username of usernames) {
                try {
                    await axios.post('http://127.0.0.1:8000/api/group-members/', {
                        group: newGroup.id,
                        username: username
                    });
                } catch (err) {
                    console.error(`Failed to add member ${username}:`, err);
                }
            }
        }
        
        success.value = 'Group created successfully!';
        setTimeout(() => {
            emit('groupCreated', newGroup);
            emit('close');
        }, 1000);
        
    } catch (err) {
        console.error('Failed to create group:', err);
        if (err.response && err.response.data) {
            const data = err.response.data;
            error.value = data.detail || data.groupname?.[0] || 'Failed to create group';
        } else {
            error.value = 'Network error. Please try again.';
        }
    } finally {
        isSubmitting.value = false;
    }
};

// Close modal
const closeModal = () => {
    emit('close');
};
</script>

<template>
    <div class="modalOverlay" @click.self="closeModal">
        <div class="modalContent">
            <div class="modalHeader">
                <h3>Create New Group</h3>
                <button class="closeBtn" @click="closeModal">&times;</button>
            </div>
            
            <div class="modalBody">
                <!-- Cover Image Upload -->
                <div class="formGroup">
                    <label>Cover Image</label>
                    <div class="imageUploadArea">
                        <div v-if="!coverImagePreview" class="uploadPlaceholder">
                            <input 
                                type="file" 
                                id="coverImageInput" 
                                accept="image/*" 
                                @change="handleImageUpload"
                                style="display: none;"
                            >
                            <label for="coverImageInput" class="uploadLabel">
                                <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                    <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
                                    <circle cx="8.5" cy="8.5" r="1.5"></circle>
                                    <polyline points="21 15 16 10 5 21"></polyline>
                                </svg>
                                <span>Click to upload cover image</span>
                            </label>
                        </div>
                        <div v-else class="imagePreview">
                            <img :src="coverImagePreview" alt="Cover preview">
                            <button class="removeImageBtn" @click="removeImage">&times;</button>
                        </div>
                    </div>
                </div>
                
                <!-- Group Title -->
                <div class="formGroup">
                    <label for="groupTitle">Group Title *</label>
                    <input 
                        id="groupTitle"
                        v-model="groupTitle" 
                        type="text" 
                        placeholder="Enter group name..."
                        maxlength="100"
                    >
                </div>
                
                <!-- Group Description -->
                <div class="formGroup">
                    <label for="groupDescription">Description</label>
                    <textarea 
                        id="groupDescription"
                        v-model="groupDescription" 
                        placeholder="Enter group description..."
                        rows="4"
                    ></textarea>
                </div>
                
                <!-- Add Members -->
                <div class="formGroup">
                    <label for="memberUsernames">Add Members (optional)</label>
                    <input 
                        id="memberUsernames"
                        v-model="memberUsernames" 
                        type="text" 
                        placeholder="Enter usernames separated by commas..."
                    >
                    <small class="helpText">Example: user1, user2, user3</small>
                </div>
                
                <!-- Error/Success Messages -->
                <div v-if="error" class="errorMessage">{{ error }}</div>
                <div v-if="success" class="successMessage">{{ success }}</div>
            </div>
            
            <div class="modalFooter">
                <button class="cancelBtn" @click="closeModal" :disabled="isSubmitting">Cancel</button>
                <button class="createBtn" @click="createGroup" :disabled="isSubmitting">
                    {{ isSubmitting ? 'Creating...' : 'Create Group' }}
                </button>
            </div>
        </div>
    </div>
</template>

<style scoped>
.modalOverlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0, 0, 0, 0.7);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
    backdrop-filter: blur(4px);
}

.modalContent {
    background: var(--c-surface);
    border: 1px solid var(--border-color);
    border-radius: 16px;
    width: 90%;
    max-width: 600px;
    max-height: 90vh;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
}

.modalHeader {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px 24px;
    border-bottom: 1px solid var(--border-color);
}

.modalHeader h3 {
    margin: 0;
    color: var(--c-text-primary);
    font-size: 1.5rem;
}

.closeBtn {
    background: none;
    border: none;
    font-size: 2rem;
    color: var(--c-text-secondary);
    cursor: pointer;
    padding: 0;
    width: 32px;
    height: 32px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 8px;
    transition: all 0.2s;
}

.closeBtn:hover {
    background: var(--c-bg);
    color: var(--c-text-primary);
}

.modalBody {
    padding: 24px;
    overflow-y: auto;
    flex: 1;
}

.formGroup {
    margin-bottom: 20px;
}

.formGroup label {
    display: block;
    color: var(--c-text-secondary);
    font-size: 0.9rem;
    font-weight: 600;
    margin-bottom: 8px;
}

.formGroup input,
.formGroup textarea {
    width: 100%;
    background: var(--c-bg);
    border: 1px solid var(--border-color);
    color: var(--c-text-primary);
    padding: 12px 16px;
    border-radius: 10px;
    font-size: 0.95rem;
    outline: none;
    transition: border-color 0.2s;
    font-family: inherit;
}

.formGroup input:focus,
.formGroup textarea:focus {
    border-color: var(--c-accent);
}

.formGroup textarea {
    resize: vertical;
    min-height: 100px;
}

.helpText {
    display: block;
    margin-top: 6px;
    color: var(--c-text-secondary);
    font-size: 0.85rem;
}

/* Image Upload */
.imageUploadArea {
    width: 100%;
    height: 200px;
    border-radius: 12px;
    overflow: hidden;
}

.uploadPlaceholder {
    width: 100%;
    height: 100%;
    background: var(--c-bg);
    border: 2px dashed var(--border-color);
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.2s;
}

.uploadPlaceholder:hover {
    border-color: var(--c-accent);
    background: var(--c-surface);
}

.uploadLabel {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 12px;
    cursor: pointer;
    color: var(--c-text-secondary);
    padding: 20px;
}

.uploadLabel svg {
    opacity: 0.5;
}

.uploadLabel span {
    font-size: 0.9rem;
}

.imagePreview {
    width: 100%;
    height: 100%;
    position: relative;
}

.imagePreview img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.removeImageBtn {
    position: absolute;
    top: 10px;
    right: 10px;
    background: rgba(0, 0, 0, 0.7);
    color: white;
    border: none;
    width: 32px;
    height: 32px;
    border-radius: 50%;
    font-size: 1.5rem;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.2s;
}

.removeImageBtn:hover {
    background: rgba(255, 0, 0, 0.8);
    transform: scale(1.1);
}

/* Messages */
.errorMessage {
    padding: 12px 16px;
    background: rgba(239, 68, 68, 0.1);
    border: 1px solid rgba(239, 68, 68, 0.3);
    border-radius: 8px;
    color: #ef4444;
    font-size: 0.9rem;
}

.successMessage {
    padding: 12px 16px;
    background: rgba(34, 197, 94, 0.1);
    border: 1px solid rgba(34, 197, 94, 0.3);
    border-radius: 8px;
    color: #22c55e;
    font-size: 0.9rem;
}

/* Modal Footer */
.modalFooter {
    display: flex;
    gap: 12px;
    padding: 20px 24px;
    border-top: 1px solid var(--border-color);
    justify-content: flex-end;
}

.cancelBtn,
.createBtn {
    padding: 12px 24px;
    border-radius: 10px;
    font-size: 0.95rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s;
    border: none;
}

.cancelBtn {
    background: var(--c-bg);
    color: var(--c-text-secondary);
    border: 1px solid var(--border-color);
}

.cancelBtn:hover:not(:disabled) {
    background: var(--c-surface);
    color: var(--c-text-primary);
}

.createBtn {
    background: var(--c-accent);
    color: white;
}

.createBtn:hover:not(:disabled) {
    opacity: 0.9;
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(249, 115, 22, 0.3);
}

.cancelBtn:disabled,
.createBtn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

/* Scrollbar */
.modalBody::-webkit-scrollbar {
    width: 6px;
}

.modalBody::-webkit-scrollbar-thumb {
    background: var(--border-color);
    border-radius: 10px;
}
</style>
