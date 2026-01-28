<script setup>
import { ref, watch, computed, nextTick } from 'vue';
import axios from 'axios';

const props = defineProps({
    task: { type: Object, default: null },
    isOpen: { type: Boolean, default: false },
    userRole: { type: String, default: null } // 'leader', 'operator', 'owner', or null
});

const emit = defineEmits(['close', 'task-updated']);

const comments = ref([]);
const newComment = ref('');
const isSubmitting = ref(false);
const isLoadingComments = ref(false);

const currentUserId = ref(parseInt(localStorage.getItem('user_id') || '0'));

// --- COMPUTED ---
const formattedDate = (dateStr) => {
    if (!dateStr) return 'N/A';
    return new Date(dateStr).toLocaleDateString('en-US', { 
        month: 'short', day: 'numeric', year: 'numeric' 
    });
};

const isCreator = computed(() => {
    if (!props.task) return false;
    // Check both direct ID field and nested object if available
    const creatorId = props.task.created_by_userid || (props.task.created_by ? props.task.created_by.id : null);
    return creatorId === currentUserId.value;
});

const priorityClass = computed(() => {
    if (!props.task) return '';
    return `priority-${props.task.priority || 'low'}`;
});

const formatStatus = (status) => {
    const map = {
        'todo': 'To Do',
        'in_progress': 'In Progress',
        'done': 'Done',
        'missed': 'Missed',
        'archived': 'Archived'
    };
    return map[status] || status;
};

const canDelete = computed(() => {
    if (props.userRole === 'leader' || props.userRole === 'operator') return true;
    if (props.userRole === 'owner') return isCreator.value; // For Own Tasks, only creator
    // Optional: Allow creator to delete in groups too? "Make sure only group leaders or operators can delete" 
    // implies creators cannot delete in groups. So we stick to the above.
    return false; 
});

// --- ACTIONS ---
const fetchComments = async () => {
    if (!props.task) return;
    isLoadingComments.value = true;
    try {
        const response = await axios.get(`http://127.0.0.1:8000/api/comments/?task=${props.task.id}`);
        comments.value = response.data;
    } catch (error) {
        console.error("Failed to load comments", error);
    } finally {
        isLoadingComments.value = false;
    }
};

const submitComment = async () => {
    if (!newComment.value.trim() || !props.task) return;
    
    isSubmitting.value = true;
    try {
        await axios.post('http://127.0.0.1:8000/api/comments/', {
            task: props.task.id,
            user: currentUserId.value, 
            content: newComment.value
        });
        newComment.value = '';
        await fetchComments(); // Refresh list
    } catch (error) {
        console.error("Failed to post comment", error);
        alert("Failed to post comment");
    } finally {
        isSubmitting.value = false;
    }
};

const markComplete = async () => {
    if (!props.task) return;
    if (!confirm("Mark this task as complete?")) return;

    try {
        await axios.patch(`http://127.0.0.1:8000/api/tasks/${props.task.id}/`, {
            status: 'done',
            completed_at: new Date().toISOString()
        });
        emit('task-updated');
        emit('close');
    } catch (error) {
        console.error("Failed to update task", error);
        alert("Failed to mark complete");
    }
};

const deleteTask = async () => {
    if (!props.task) return;
    if (!confirm("Are you sure you want to delete this task? This cannot be undone.")) return;
    
    try {
        await axios.delete(`http://127.0.0.1:8000/api/tasks/${props.task.id}/`);
        emit('task-updated'); // Will refresh list
        emit('close');
    } catch (error) {
        console.error("Failed to delete task", error);
        alert("Failed to delete task. You might not have permission.");
    }
};

const editTask = () => {
    alert("Edit functionality coming soon!");
};

// --- WATCHERS ---
const editingCommentId = ref(null);
const editContent = ref('');

const isCommentOwner = (comment) => {
    // Handling case where user_detail might be number or object depending on serialization depth
    // Usually it's object from serializer.
    const uid = comment.user_detail?.id || comment.user;
    return uid === currentUserId.value;
};

const isEdited = (comment) => {
    if (!comment.updated_at || !comment.created_at) return false;
    // Check if updated_at is significantly after created_at (e.g. > 2 seconds)
    const created = new Date(comment.created_at).getTime();
    const updated = new Date(comment.updated_at).getTime();
    return (updated - created) > 2000;
};

const startEdit = (comment) => {
    editingCommentId.value = comment.id;
    editContent.value = comment.content;
};

const cancelEdit = () => {
    editingCommentId.value = null;
    editContent.value = '';
};

const saveEdit = async (commentId) => {
    if (!editContent.value.trim()) return;
    
    try {
        await axios.patch(`http://127.0.0.1:8000/api/comments/${commentId}/`, {
            content: editContent.value
        });
        await fetchComments();
        cancelEdit();
    } catch (error) {
        console.error("Failed to update comment", error);
        alert("Failed to update comment.");
    }
};

const deleteComment = async (commentId) => {
    if (!confirm("Delete this comment?")) return;
    
    try {
        await axios.delete(`http://127.0.0.1:8000/api/comments/${commentId}/`);
        // Remove locally to be snappy, or refresh
        comments.value = comments.value.filter(c => c.id !== commentId);
    } catch (error) {
        console.error("Failed to delete comment", error);
        alert("Failed to delete comment.");
    }
};

// --- WATCHERS ---
watch(() => props.isOpen, (newVal) => {
    if (newVal && props.task) {
        comments.value = []; // Clear old comments
        fetchComments();
    }
});
</script>

<template>
    <div v-if="isOpen" class="modal-overlay" @click.self="$emit('close')">
        <div class="modal-content">
            <button class="close-btn" @click="$emit('close')">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                    <line x1="18" y1="6" x2="6" y2="18"></line>
                    <line x1="6" y1="6" x2="18" y2="18"></line>
                </svg>
            </button>
            
            <div v-if="task" class="modal-body-grid">

                <!-- LEFT COLUMN: DETAILS -->
                <div class="details-column custom-scroll">
                    
                    <!-- TOP SECTION: IMAGE + TITLE/ASSIGNED -->
                    <div class="top-section">
                        <!-- Small Image Top Left -->
                        <div v-if="task.imageUrl || task.image" class="small-task-image">
                            <img :src="task.imageUrl || task.image" alt="Task Cover">
                        </div>
                        <div v-else class="small-task-image placeholder-img">
                            <span>No Image</span>
                        </div>

                        <!-- Right of Image: Title + Assigned -->
                        <div class="header-info">
                            <div class="title-row">
                                <h2>{{ task.title }}</h2>
                                <span class="status-badge" :class="priorityClass">{{ task.priority }}</span>
                            </div>
                            
                            <!-- Assigned Users (Under Title) -->
                            <div class="assigned-row">
                                <span class="label-small">Assigned to:</span>
                                <div class="user-chip">
                                    <img v-if="task.assigned_to?.profile_picture" :src="task.assigned_to.profile_picture" class="avatar-small img-fit">
                                    <span v-else class="avatar-small">{{ task.assigned_to?.username?.charAt(0).toUpperCase() || '?' }}</span>
                                    <span>{{ task.assigned_to?.username || 'Unassigned' }}</span>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- DESCRIPTION (Under Image/Title) -->
                    <div class="description-section">
                        <label>Description</label>
                        <p class="description">{{ task.description || "No description provided." }}</p>
                    </div>

                    <!-- META ROW: TIMESPAN + STATUS -->
                    <div class="meta-row">
                        <!-- TIMESPAN (Usage already existing styles, now inside row) -->
                        <div class="timespan-section">
                            <div class="time-block">
                                <span class="label-icon">📅 Start</span>
                                <span class="value">{{ formattedDate(task.start_date || new Date()) }}</span>
                            </div>
                            <div class="arrow">→</div>
                            <div class="time-block">
                                <span class="label-icon">🏁 Due</span>
                                <span class="value">{{ formattedDate(task.due_date) }}</span>
                            </div>
                        </div>

                        <!-- NEW: STATUS INDICATOR -->
                        <div class="status-indicator">
                            <span class="label-icon">Current Status</span>
                            <div class="status-value" :class="`status-${task.status}`">
                                <span class="status-dot"></span>
                                {{ formatStatus(task.status) }}
                            </div>
                        </div>
                    </div>

                    <!-- META / ACTIONS (Bottom) -->
                    <div class="meta-footer">
                        <div class="meta-info">
                            <span class="meta-text">Created by {{ task.created_by?.username }}</span>
                        </div>
                        <div class="actions-bar">
                            <button class="btn btn-primary" @click="markComplete">Mark Complete</button>
                            <button v-if="isCreator" class="btn btn-secondary" @click="editTask">Edit</button>
                            <button v-if="canDelete" class="btn btn-danger" @click="deleteTask">Delete</button>
                        </div>
                    </div>
                </div>
                
                <!-- RIGHT COLUMN: COMMENTS -->
                <div class="comments-column custom-scroll">
                    <div class="comments-section">
                        <h3>Comments</h3>
                        
                        <!-- ADD COMMENT -->
                        <div class="add-comment">
                            <textarea 
                                v-model="newComment" 
                                placeholder="Write a comment..."
                                rows="2"
                            ></textarea>
                            <button :disabled="isSubmitting" @click="submitComment">
                                {{ isSubmitting ? '...' : 'Post' }}
                            </button>
                        </div>

                        <div class="comments-list">
                            <div v-if="isLoadingComments" class="loading-text">Loading comments...</div>
                            <div v-else-if="comments.length === 0" class="no-comments">No comments yet.</div>
                            
                            <div v-for="comment in comments" :key="comment.id" class="comment-item">
                                <img v-if="comment.user_detail?.profile_picture" :src="comment.user_detail.profile_picture" class="comment-avatar img-fit">
                                <div v-else class="comment-avatar">
                                    {{ comment.user_detail?.username?.charAt(0).toUpperCase() || '?' }}
                                </div>
                                <div class="comment-content">
                                    <div class="comment-header">
                                        <span class="username">{{ comment.user_detail?.username || 'Unknown' }}</span>
                                        <span class="timestamp">
                                            {{ formattedDate(comment.created_at) }}
                                            <span v-if="isEdited(comment)" class="edited-label">(edited)</span>
                                        </span>
                                    </div>
                                    
                                    <!-- EDIT MODE -->
                                    <div v-if="editingCommentId === comment.id" class="edit-mode">
                                        <textarea v-model="editContent" rows="2" class="edit-input"></textarea>
                                        <div class="edit-actions">
                                            <button class="btn-xs btn-save" @click="saveEdit(comment.id)">Save</button>
                                            <button class="btn-xs btn-cancel" @click="cancelEdit">Cancel</button>
                                        </div>
                                    </div>
                                    
                                    <!-- VIEW MODE -->
                                    <div v-else>
                                        <p class="text">{{ comment.content }}</p>
                                        <div v-if="isCommentOwner(comment)" class="comment-actions">
                                            <button class="action-link" @click="startEdit(comment)">Edit</button>
                                            <button class="action-link delete" @click="deleteComment(comment.id)">Delete</button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

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
    max-width: 1000px; /* Wider for 2 columns */
    height: 80vh; /* Fixed height for scrollable areas */
    border-radius: 16px;
    border: 1px solid var(--border-color);
    box-shadow: 0 20px 50px rgba(0,0,0,0.5);
    display: flex;
    flex-direction: column;
    overflow: hidden;
    position: relative;
    animation: scaleUp 0.2s cubic-bezier(0.16, 1, 0.3, 1);
}

.modal-body-grid {
    display: grid;
    grid-template-columns: 1fr 350px; /* Details first, Comments second (fixed width) */
    height: 100%;
    overflow: hidden;
}

.close-btn {
    position: absolute;
    top: 15px; right: 15px;
    background: rgba(0,0,0,0.5);
    color: white;
    border: none;
    width: 32px; height: 32px;
    border-radius: 50%;
    
    /* Centering */
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 0;
    
    cursor: pointer;
    z-index: 50;
    transition: background 0.2s, transform 0.1s;
}
.close-btn:hover { background: rgba(0,0,0,0.8); transform: scale(1.05); }

/* --- LEFT COLUMN: DETAILS (Now Left) --- */
.details-column {
    padding: 30px;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    gap: 24px;
}

/* --- RIGHT COLUMN: COMMENTS (Now Right) --- */
.comments-column {
    background: rgba(0,0,0,0.1); 
    border-left: 1px solid var(--border-color); /* Changed from border-right */
    padding: 24px;
    display: flex;
    flex-direction: column;
    overflow-y: auto;
}

.comments-section h3 {
    font-size: 1.1rem;
    color: var(--c-text-primary);
    margin-bottom: 20px;
    margin-top: 0;
}

.add-comment {
    display: flex;
    gap: 10px;
    margin-bottom: 20px;
}
.add-comment textarea {
    flex: 1;
    background: var(--c-bg);
    border: 1px solid var(--border-color);
    border-radius: 8px;
    padding: 10px;
    color: var(--c-text-primary);
    font-family: inherit;
    resize: none;
    font-size: 0.9rem;
}
.add-comment button {
    background: var(--c-accent);
    color: white;
    border: none;
    padding: 0 16px;
    border-radius: 8px;
    font-weight: 600;
    cursor: pointer;
    font-size: 0.9rem;
}

.comments-list {
    display: flex;
    flex-direction: column;
    gap: 16px;
}

.comment-item {
    display: flex;
    gap: 12px;
}
.comment-avatar {
    width: 32px; height: 32px;
    border-radius: 50%;
    background: var(--c-surface-hover);
    color: var(--c-text-primary);
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    font-size: 0.8rem;
    flex-shrink: 0;
}
.comment-content {
    flex: 1;
    background: var(--c-bg);
    padding: 10px 14px;
    border-radius: 12px;
    border: 1px solid var(--border-color);
}
.comment-header {
    display: flex;
    justify-content: space-between;
    margin-bottom: 4px;
    font-size: 0.8rem;
}
.username { font-weight: 600; color: var(--c-text-primary); }
.timestamp { color: var(--c-text-secondary); }
.text { margin: 0; color: var(--c-text-secondary); font-size: 0.9rem; line-height: 1.4; word-break: break-word;}

/* --- RIGHT COLUMN: DETAILS --- */
.details-column {
    padding: 30px;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    gap: 24px;
}

/* TOP SCETION */
.top-section {
    display: flex;
    gap: 20px;
}

.small-task-image {
    width: 100px; 
    height: 100px;
    border-radius: 12px;
    overflow: hidden;
    flex-shrink: 0;
    border: 1px solid var(--border-color);
}
.placeholder-img {
    background: var(--c-surface-hover);
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--c-text-secondary);
    font-size: 0.8rem;
}
.small-task-image img {
    width: 100%; height: 100%; object-fit: cover;
}

.header-info {
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: center; 
    gap: 10px;
}

.title-row {
    display: flex;
    align-items: center;
    gap: 10px;
    flex-wrap: wrap;
}
.title-row h2 {
    margin: 0;
    font-size: 1.6rem;
    color: var(--c-text-primary);
    line-height: 1.2;
}

.status-badge {
    padding: 2px 8px;
    border-radius: 12px;
    font-size: 0.7rem;
    font-weight: 700;
    text-transform: uppercase;
    background: var(--c-surface-hover);
    color: var(--c-text-secondary);
}
.priority-high { color: #f97316; background: rgba(249, 115, 22, 0.15); }
.priority-urgent { color: #ef4444; background: rgba(220, 38, 38, 0.15); }

.assigned-row {
    display: flex;
    align-items: center;
    gap: 10px;
}
.label-small { color: var(--c-text-secondary); font-size: 0.9rem; }
.user-chip {
    display: flex;
    align-items: center;
    gap: 8px;
    background: var(--c-surface-hover);
    padding: 4px 10px 4px 4px;
    border-radius: 20px;
    font-size: 0.9rem;
    color: var(--c-text-primary);
}
.avatar-small {
    width: 24px; height: 24px;
    border-radius: 50%;
    background: var(--c-accent);
    color: white;
    display: flex; 
    align-items: center; 
    justify-content: center;
    font-size: 0.7rem;
    font-weight: bold;
}
/* Helper for images reusing avatar classes */
.img-fit {
    object-fit: cover;
    background: transparent;
}

/* DESCRIPTION */
.description-section label {
    display: block;
    font-size: 0.8rem;
    text-transform: uppercase;
    color: var(--c-text-secondary);
    margin-bottom: 8px;
    opacity: 0.7;
    letter-spacing: 0.5px;
}
.description {
    margin: 0;
    color: var(--c-text-primary);
    line-height: 1.6;
    font-size: 1rem;
    background: rgba(255,255,255,0.02);
    padding: 15px;
    border-radius: 8px;
    border: 1px solid rgba(255,255,255,0.05);
}

/* META ROW */
.meta-row {
    display: flex;
    gap: 20px;
    align-items: stretch; /* Ensure same height */
    flex-wrap: wrap; /* responsive wrap */
}

/* TIMESPAN */
.timespan-section {
    display: flex;
    align-items: center;
    gap: 15px;
    background: var(--c-surface-hover);
    padding: 15px;
    border-radius: 12px;
    /* align-self removed to fit flex stretch */
}
.time-block { display: flex; flex-direction: column; gap: 4px; }
.label-icon { font-size: 0.8rem; color: var(--c-text-secondary); text-transform: uppercase; letter-spacing: 0.5px; opacity: 0.8; }
.value { font-weight: 600; color: var(--c-text-primary); }
.arrow { color: var(--c-text-secondary); opacity: 0.5; }

/* STATUS INDICATOR */
.status-indicator {
    background: var(--c-surface-hover);
    padding: 15px 20px;
    border-radius: 12px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    gap: 6px;
    min-width: 140px;
}
.status-value {
    display: flex;
    align-items: center;
    gap: 8px;
    font-weight: 700;
    font-size: 1rem;
    color: var(--c-text-primary);
    text-transform: capitalize;
}
.status-dot {
    width: 10px; height: 10px;
    border-radius: 50%;
    background: gray;
    box-shadow: 0 0 5px rgba(255,255,255,0.2);
}

/* Status Colors */
.status-todo .status-dot { background: #3b82f6; box-shadow: 0 0 8px rgba(59, 130, 246, 0.4); }
.status-in_progress .status-dot { background: #f59e0b; box-shadow: 0 0 8px rgba(245, 158, 11, 0.4); }
.status-done .status-dot { background: #10b981; box-shadow: 0 0 8px rgba(16, 185, 129, 0.4); }
.status-missed .status-dot { background: #ef4444; box-shadow: 0 0 8px rgba(239, 68, 68, 0.4); }
.status-archived .status-dot { background: #6b7280; }

/* FOOTER / ACTIONS */
.meta-footer {
    margin-top: auto; /* Push to bottom */
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-top: 20px;
    border-top: 1px solid var(--border-color);
}
.meta-text { font-size: 0.85rem; color: var(--c-text-secondary); font-style: italic; }

.actions-bar { display: flex; gap: 10px; }
.btn {
    padding: 8px 16px;
    border-radius: 8px;
    border: none;
    font-weight: 600;
    cursor: pointer;
    font-size: 0.9rem;
    transition: filter 0.2s;
}
.btn:hover { filter: brightness(1.1); }
.btn-primary { background: var(--c-accent); color: white; }
.btn-primary { background: var(--c-accent); color: white; }
.btn-secondary { background: transparent; color: var(--c-text-primary); border: 1px solid var(--border-color); }
.btn-danger { background: rgba(239, 68, 68, 0.2); color: #ef4444; border: 1px solid #ef4444; }
.btn-danger:hover { background: #ef4444; color: white; }

/* SCROLLBAR CUSTOMIZATION */
.custom-scroll::-webkit-scrollbar { width: 6px; }
.custom-scroll::-webkit-scrollbar-track { background: transparent; }
.custom-scroll::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 3px; }
.custom-scroll::-webkit-scrollbar-thumb:hover { background: rgba(255,255,255,0.2); }

@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
@keyframes scaleUp { from { transform: scale(0.95); opacity: 0; } to { transform: scale(1); opacity: 1; } }

/* RESPONSIVE */
@media (max-width: 800px) {
    .modal-body-grid {
        grid-template-columns: 1fr;
        overflow-y: auto;
    }
    .comments-column {
        order: 2; /* Move comments to bottom on mobile */
        height: 300px; /* Fixed height for comments on mobile */
        border-right: none;
        border-top: 1px solid var(--border-color);
    }
    .details-column {
        order: 1;
        overflow: visible; /* Let it scroll with parent */
    }
    .modal-content {
        height: 90vh; /* Taller on mobile */
    }
}

/* NEW STYLES FOR COMMENT EDITING */
.edited-label {
    font-size: 0.75rem;
    color: var(--c-text-secondary);
    font-style: italic;
    margin-left: 5px;
}

.comment-actions {
    margin-top: 8px;
    display: flex;
    gap: 10px;
    justify-content: flex-end; /* Move to bottom right */
}

.action-link {
    background: none;
    border: none;
    padding: 0;
    font-size: 0.8rem;
    color: var(--c-text-secondary);
    cursor: pointer;
    text-decoration: underline;
    opacity: 0.7;
}
.action-link:hover { opacity: 1; color: var(--c-accent); }
.action-link.delete:hover { color: #ef4444; }

.edit-mode {
    margin-top: 5px;
}
.edit-input {
    width: 100%;
    background: var(--c-bg);
    border: 1px solid var(--c-accent);
    color: var(--c-text-primary);
    border-radius: 6px;
    padding: 8px;
    font-family: inherit;
    font-size: 0.9rem;
    resize: none;
}
.edit-actions {
    display: flex;
    gap: 8px;
    margin-top: 6px;
    justify-content: flex-end;
}
.btn-xs {
    padding: 4px 10px;
    border-radius: 4px;
    font-size: 0.8rem;
    font-weight: 600;
    cursor: pointer;
    border: none;
}
.btn-save { background: var(--c-accent); color: white; }
.btn-cancel { background: transparent; border: 1px solid var(--border-color); color: var(--c-text-secondary); }
</style>
