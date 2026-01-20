<script setup>
import { ref, watch, computed, nextTick } from 'vue';
import axios from 'axios';

const props = defineProps({
    task: { type: Object, default: null },
    isOpen: { type: Boolean, default: false }
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

const editTask = () => {
    alert("Edit functionality coming soon!");
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
            <button class="close-btn" @click="$emit('close')">&times;</button>
            
            <div v-if="task" class="modal-body">
                <!-- HEADER IMAGE -->
                <div v-if="task.imageUrl" class="task-image">
                    <img :src="task.imageUrl" alt="Task Cover">
                </div>

                <div class="content-padding">
                    <!-- TITLE & METADATA -->
                    <div class="header-section">
                        <div class="title-row">
                            <h2>{{ task.title }}</h2>
                            <span class="status-badge" :class="priorityClass">{{ task.priority }}</span>
                        </div>
                        <p class="description">{{ task.description || "No description provided." }}</p>
                    </div>

                    <!-- INFO GRID -->
                    <div class="info-grid">
                        <div class="info-item">
                            <span class="label">Created By</span>
                            <span class="value">{{ task.created_by?.username || 'Unknown' }}</span>
                        </div>
                        <div class="info-item">
                            <span class="label">Assigned To</span>
                            <span class="value">{{ task.assigned_to?.username || 'Unassigned' }}</span>
                        </div>
                        <div class="info-item">
                            <span class="label">Start Date</span>
                            <span class="value">{{ formattedDate(task.start_date) }}</span>
                        </div>
                        <div class="info-item">
                            <span class="label">Due Date</span>
                            <span class="value">{{ formattedDate(task.due_date) }}</span>
                        </div>
                    </div>

                    <!-- ACTIONS -->
                    <div class="actions-bar">
                        <button class="btn btn-primary" @click="markComplete">
                            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <polyline points="20 6 9 17 4 12"></polyline>
                            </svg>
                            Mark Complete
                        </button>
                        <button v-if="isCreator" class="btn btn-secondary" @click="editTask">
                            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                                <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
                            </svg>
                            Edit Task
                        </button>
                    </div>

                    <!-- COMMENTS SECTION -->
                    <div class="comments-section">
                        <h3>Comments</h3>
                        
                        <div class="comments-list">
                            <div v-if="isLoadingComments" class="loading-text">Loading comments...</div>
                            <div v-else-if="comments.length === 0" class="no-comments">No comments yet.</div>
                            
                            <div v-for="comment in comments" :key="comment.id" class="comment-item">
                                <div class="comment-avatar">
                                    {{ comment.user_detail?.username?.charAt(0).toUpperCase() || '?' }}
                                </div>
                                <div class="comment-content">
                                    <div class="comment-header">
                                        <span class="username">{{ comment.user_detail?.username || 'Unknown' }}</span>
                                        <span class="timestamp">{{ formattedDate(comment.created_at) }}</span>
                                    </div>
                                    <p class="text">{{ comment.content }}</p>
                                </div>
                            </div>
                        </div>

                        <!-- ADD COMMENT -->
                        <div class="add-comment">
                            <textarea 
                                v-model="newComment" 
                                placeholder="Write a comment..."
                                rows="2"
                            ></textarea>
                            <button :disabled="isSubmitting" @click="submitComment">
                                {{ isSubmitting ? 'Posting...' : 'Post' }}
                            </button>
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
    background: rgba(0, 0, 0, 0.75);
    backdrop-filter: blur(4px);
    z-index: 2000;
    display: flex;
    justify-content: center;
    align-items: center;
    animation: fadeIn 0.2s ease;
}

.modal-content {
    background: var(--c-surface);
    width: 90%;
    max-width: 600px;
    max-height: 90vh;
    border-radius: 16px;
    border: 1px solid var(--border-color);
    box-shadow: 0 20px 50px rgba(0,0,0,0.5);
    display: flex;
    flex-direction: column;
    overflow: hidden;
    position: relative;
    animation: scaleUp 0.2s cubic-bezier(0.16, 1, 0.3, 1);
}

.modal-body {
    overflow-y: auto;
}

.close-btn {
    position: absolute;
    top: 15px; right: 15px;
    background: rgba(0,0,0,0.5);
    color: white;
    border: none;
    width: 32px; height: 32px;
    border-radius: 50%;
    font-size: 1.5rem;
    line-height: 1;
    cursor: pointer;
    z-index: 10;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: background 0.2s;
}
.close-btn:hover { background: rgba(0,0,0,0.8); }

/* TASK IMAGE */
.task-image {
    width: 100%;
    height: 200px;
    overflow: hidden;
}
.task-image img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.content-padding {
    padding: 24px;
}

/* HEADER */
.header-section { margin-bottom: 24px; }

.title-row {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 15px;
    margin-bottom: 10px;
}

.title-row h2 {
    margin: 0;
    font-size: 1.5rem;
    color: var(--c-text-primary);
    line-height: 1.2;
}

.status-badge {
    padding: 4px 10px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    background: var(--c-surface-hover);
    color: var(--c-text-secondary);
}
.priority-high { color: #f97316; background: rgba(249, 115, 22, 0.15); }
.priority-urgent { color: #ef4444; background: rgba(220, 38, 38, 0.15); }
.priority-medium { color: #eab308; background: rgba(234, 179, 8, 0.15); }
.priority-low { color: #22c55e; background: rgba(34, 197, 94, 0.15); }

.description {
    color: var(--c-text-secondary);
    line-height: 1.5;
    margin: 0;
}

/* INFO GRID */
.info-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
    margin-bottom: 24px;
    padding-bottom: 24px;
    border-bottom: 1px solid var(--border-color);
}

.info-item { display: flex; flex-direction: column; gap: 4px; }
.label { font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.5px; color: var(--c-text-secondary); opacity: 0.7; }
.value { font-size: 0.95rem; color: var(--c-text-primary); font-weight: 500; }

/* ACTIONS */
.actions-bar {
    display: flex;
    gap: 12px;
    margin-bottom: 30px;
}
.btn {
    flex: 1;
    padding: 10px;
    border-radius: 8px;
    border: none;
    font-weight: 600;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    transition: filter 0.2s;
}
.btn:hover { filter: brightness(1.1); }
.btn-primary { background: var(--c-accent); color: white; }
.btn-secondary { background: var(--c-surface-hover); color: var(--c-text-primary); border: 1px solid var(--border-color); }

/* COMMENTS */
.comments-section h3 {
    font-size: 1.1rem;
    color: var(--c-text-primary);
    margin-bottom: 15px;
}

.comments-list {
    display: flex;
    flex-direction: column;
    gap: 15px;
    margin-bottom: 20px;
    max-height: 300px;
    overflow-y: auto;
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
    font-size: 0.9rem;
    flex-shrink: 0;
}

.comment-content {
    flex: 1;
    background: rgba(255,255,255,0.03);
    padding: 10px 14px;
    border-radius: 12px;
}

.comment-header {
    display: flex;
    justify-content: space-between;
    margin-bottom: 4px;
    font-size: 0.85rem;
}

.username { font-weight: 600; color: var(--c-text-primary); }
.timestamp { color: var(--c-text-secondary); font-size: 0.75rem; }
.text { margin: 0; color: var(--c-text-secondary); font-size: 0.9rem; line-height: 1.4; word-break: break-word;}

.add-comment {
    display: flex;
    gap: 10px;
    align-items: flex-start;
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
}
.add-comment textarea:focus { outline: none; border-color: var(--c-accent); }
.add-comment button {
    background: var(--c-accent);
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 8px;
    font-weight: 600;
    cursor: pointer;
    height: 42px;
}
.add-comment button:disabled { opacity: 0.5; cursor: not-allowed; }

@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
@keyframes scaleUp { from { transform: scale(0.95); opacity: 0; } to { transform: scale(1); opacity: 1; } }
</style>
