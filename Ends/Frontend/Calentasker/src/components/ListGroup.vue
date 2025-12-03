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
}

.listGroup img {
    width: 50px;
    height: 50px;
    aspect-ratio: 1/1;
    object-fit: cover;
    border-radius: 10px;
    flex-shrink: 0;
    
    /* DEFAULT STATE (Expanded) */
    /* We want margin to be 5px */
    margin: 5px;
    
    /* LOGIC: When returning to this state (Expanding), transition the margin with 0s duration and 0s delay. This makes the jump to 5px happen IMMEDIATELY. */
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
        /* We remove padding so the auto-margins calculate correctly */
        padding: 0;
    }

    .listGroup img {
        /* We want the image centered */
        margin: auto;

        /* LOGIC: When entering this state (Collapsing), transition the margin with 0s duration BUT 0.3s delay. This forces the image to stay at '5px' until the parent animation (which takes 0.3s) is finished, then it snaps to center. */
        transition: margin 0s;
    }
}
</style>