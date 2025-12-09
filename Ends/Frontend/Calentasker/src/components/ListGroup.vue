<script>
    export default {
        props: {
            url: {
                type: String,
                default: "https://www.mariposakids.co.nz/wp-content/uploads/2014/08/image-placeholder2.jpg"
            },
            name: {
                type: String,
                default: "Group Name"
            },
            // NEW PROP: To highlight the selected group
            isActive: {
                type: Boolean,
                default: false
            }
        }
    }
</script>

<template>
    <!-- Add active class if selected -->
    <div class="listGroup" :class="{ 'active-group': isActive }">
        <img :src="url" alt="">
        <p class="groupName">{{name}}</p>
    </div>
</template>

<style scoped>
.listGroup {
    container-type: inline-size;
    container-name: group-item;

    display: flex;
    flex-direction: row;
    align-items: center;
    background-color: gray;
    border-radius: 15px;
    font-family: Arial, Helvetica, sans-serif;
    width: 100%;
    margin: 10px auto;
    height: 60px;
    overflow: hidden;
    transition: all 0.3s ease;
    
    /* Make it clickable */
    cursor: pointer;
    border: 2px solid transparent; 
}

/* Hover Effect */
.listGroup:hover {
    filter: brightness(1.1);
}

/* Selected State */
.active-group {
    background-color: #333; /* Darker background when active */
    border-color: white;    /* Border to indicate selection */
}

.listGroup img {
    width: 50px;
    height: 50px;
    aspect-ratio: 1/1;
    object-fit: cover;
    border-radius: 10px;
    flex-shrink: 0;
    margin: 5px;
    transition: margin 0s 0s;
}

.groupName {
    margin: 0 0 0 10px;
    padding: 0;
    font-size: 20px;
    white-space: nowrap;
    color: white;
    transition: opacity 0.2s;
}

/* --- COLLAPSED STATE --- */
@container group-item (max-width: 60px) {
    .groupName {
        display: none;
    }
    
    .listGroup {
        padding: 0;
    }

    .listGroup img {
        margin: auto;
        transition: margin 0s;
    }
}
</style>