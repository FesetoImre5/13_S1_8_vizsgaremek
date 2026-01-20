<script setup>
const props = defineProps({
    url: {
        type: String,
        default: "https://www.mariposakids.co.nz/wp-content/uploads/2014/08/image-placeholder2.jpg"
    },
    name: {
        type: String,
        default: "Group Name"
    },
    isActive: {
        type: Boolean,
        default: false
    }
});
</script>

<template>
    <div class="listGroupItem" :class="{ 'active-group': isActive }">
        <div class="groupIcon">
            <img :src="url" alt="">
        </div>
        <span class="groupName">{{ name }}</span>
    </div>
</template>

<style scoped>
.listGroupItem {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 10px 12px;
    margin-bottom: 8px;
    background-color: var(--c-surface);
    border: 1px solid var(--border-color);
    border-radius: 10px;
    cursor: pointer;
    transition: all 0.2s ease;
}

.listGroupItem:hover {
    background-color: var(--c-bg);
    border-color: var(--c-accent);
    transform: translateX(4px);
}

.listGroupItem.active-group {
    background-color: var(--c-accent);
    border-color: var(--c-accent);
    box-shadow: 0 2px 8px rgba(249, 115, 22, 0.3);
}

.listGroupItem.active-group .groupName {
    color: white;
    font-weight: bold;
}

.groupIcon {
    width: 40px;
    height: 40px;
    flex-shrink: 0;
    border-radius: 8px;
    overflow: hidden;
    background-color: var(--c-bg);
}

.groupIcon img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.groupName {
    flex: 1;
    color: var(--c-text-primary);
    font-size: 14px;
    font-weight: 500;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}
</style>