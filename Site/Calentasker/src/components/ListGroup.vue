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
            }
        }
    }
</script>

<template>
    <div class="listGroup">
        <img :src="url" alt="">
        <p class="groupName">{{name}}</p>
    </div>
</template>

<style scoped>
.listGroup {
    /* 1. Enable Container Queries */
    container-type: inline-size;
    container-name: group-item;

    display: flex;
    flex-direction: row;
    align-items: center; /* Center vertically */
    background-color: gray;
    border-radius: 15px;
    font-family: Arial, Helvetica, sans-serif;
    width: 100%;
    margin: 10px auto;
    height: 60px; /* Fixed height helps with transitions */
    overflow: hidden;
}

.listGroup img {
    width: 50px;
    height: 50px;
    aspect-ratio: 1/1;
    object-fit: cover;
    margin: 5px;
    border-radius: 10px;
    flex-shrink: 0; /* Prevents image from squishing */
}

.groupName {
    margin: 0 0 0 10px;
    padding: 0;
    font-size: 20px;
    white-space: nowrap; /* Don't let text wrap to next line */
    color: white; /* Added for better visibility on gray */
}

/* --- COMPACT STATE (Image Only) --- */
/* When the component width is smaller than 120px, hide text */
@container group-item (max-width: 160px) {
    .groupName {
        display: none;
    }
    .listGroup {
        justify-content: center; /* Center the image horizontally */
    }
    .listGroup img {
        /*margin: 0 auto; /* Remove margin for perfect centering */
    }
}
</style>