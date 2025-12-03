<script>
    export default {
        props: {
            url: {
                type: String,
                default: "https://www.mariposakids.co.nz/wp-content/uploads/2014/08/image-placeholder2.jpg"
            },
            title: {
                type: String,
                default: "Placeholder Title"
            },
            desc: {
                type: String,
                default: "This is a somewhat sort, but still padded sentence to function as a Description example. Yaay."
            }
        }
    }
</script>

<template>
    <div class="task">
        <img :src="url" alt="" class="taskImage">
        
        <div class="taskText">
            <h2 class="taskTitle">{{title}}</h2>
            <p class="taskDesc">{{ desc }}</p>
            <button class="detailsBtn">Details</button>
        </div>
    </div>
</template>

<style scoped>
.task {
    display: flex;
    flex-direction: row;
    background-color: gray;
    border-radius: 15px;
    font-family: Arial, Helvetica, sans-serif;
    width: 100%;
    margin: 10px 0;
    max-height: 145px;
    
    /* CHANGED: 'stretch' ensures the text area is as tall as the image, 
        so the button can sit at the very bottom flush. */
    align-items: stretch; 
    
    position: relative; 
    overflow: hidden;
}

.taskImage{
    width: 125px;
    height: 125px;
    aspect-ratio: 1/1;
    object-fit: cover;
    margin: 10px;
    flex-shrink: 0;
    border-radius: 10px;
    /* Center image vertically if needed due to 'stretch' alignment */
    align-self: center; 
}

.taskText {
    flex-grow: 1; 
    padding: 10px;
    min-width: 0; 
    padding-right: 100px; 
}

.taskTitle{
    font-size: 40px;
    margin: 0;
    padding: 0;
    line-height: 1.2;
}

.taskDesc{
    margin: 0;
    font-size: 18px;
    display: -webkit-box;
    text-overflow: ellipsis;
    overflow: hidden;
    -webkit-box-orient: vertical;
    -webkit-line-clamp: 3;
    word-break: keep-all;
}

.detailsBtn {
    font-size: 14px;
    font-weight: bold;
    padding: 0 20px;
    border: none;
    cursor: pointer;
    background-color: orangered; 
    color: white;
    white-space: nowrap;
    
    /* Desktop: Absolute Right */
    position: absolute;
    right: 0;      
    top: 0;        
    height: 100%;  
    border-radius: 0; 
}

/* --- RESPONSIVE LOGIC (< 1000px) --- */
@media (max-width: 1000px) {
    .taskText {
        padding-right: 10px;
        display: flex;
        flex-direction: column;
        /* Pushes content apart so button hits the bottom */
        justify-content: flex-end; 
    }

    .taskDesc {
        display: none;
    }

    .detailsBtn {
        position: static;
        height: auto; 
        padding: 15px 0; /* Taller button for mobile touch */
        text-align: center;
        
        background-color: orangered; 
        color: white;
        
        /* --- THE FIX FOR FLUSH EDGES --- */
        /* 1. Reset border radius */
        border-radius: 100px 0 0 0; 
        
        /* 2. Use negative margins to counteract .taskText padding (10px) */
        margin-left: -10px;
        margin-right: -10px;
        margin-bottom: -10px; /* Pulls it down to touch the container edge */
        
        /* 3. Calculate width to include the padding space we ignored */
        width: calc(100% + 20px); 
        
        /* 4. Add margin top to separate from Title */
        margin-top: 10px;
    }
}
</style>