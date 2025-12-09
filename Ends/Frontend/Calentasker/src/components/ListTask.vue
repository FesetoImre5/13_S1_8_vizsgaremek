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
        },
        emits: ['click']
    }
</script>

<template>
    <div class="task">
        <img :src="url" alt="" class="taskImage">
        
        <div class="taskText">
            <h2 class="taskTitle">{{title}}</h2>
            <p class="taskDesc">{{ desc }}</p>
            <button class="detailsBtn" @click="$emit('click')">Details</button>
        </div>
    </div>
</template>

<style scoped>
    /* ... (Desktop styles remain unchanged) ... */
    .task {
        display: flex;
        flex-direction: row;
        background-color: gray;
        border-radius: 15px;
        font-family: Arial, Helvetica, sans-serif;
        width: 100%;
        margin: 10px 0;
        max-height: 145px;
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
        align-self: center;
        background-color: #fff;
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
        background-color: #ddd; 
        white-space: nowrap;
        position: absolute;
        right: 0;      
        top: 0;        
        height: 100%;  
        border-radius: 0; 
    }

    /* 
       --- MOBILE TILE LAYOUT (< 530px) --- 
    */
    @media (max-width: 530px) {
        .task {
            flex-direction: column;
            margin: 10px 0;
            padding: 0;
            
            aspect-ratio: 2 / 1; 
            height: auto; 
            max-height: none; 
            width: 100%; 
            min-width: 0; 
            
            border: 2px solid white;
            
            /* 1. ADDED: Dark background to the container itself.
               This fills any sub-pixel gaps between the border and image 
               so the page background (blue) doesn't leak through. */
            background-color: #222; 
            
            cursor: pointer; 
            
            /* Ensure clipping works perfectly on mobile browsers */
            transform: translateZ(0); 
        }

        .taskImage {
            width: 100%;
            height: 100%;
            margin: 0;
            
            /* 2. CHANGED: Remove border radius from the child.
               Let the parent .task (overflow: hidden) handle the clipping.
               This removes the mismatch gap. */
            border-radius: 0; 
            
            aspect-ratio: auto;
            object-fit: cover; 
            object-position: center; 
        }

        .taskText {
            padding: 10px;
            position: absolute;
            bottom: 0;
            left: 0;
            width: 100%;
            background-color: rgba(50, 50, 50, 0.85); 
            backdrop-filter: blur(2px); 
            
            /* 3. CHANGED: Remove border radius here too. */
            border-radius: 0; 
            
            display: block;
            text-align: center;
        }

        .taskTitle {
            font-size: 20px;
            color: white;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        .taskDesc {
            display: none;
        }

        .detailsBtn {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            opacity: 0; 
            z-index: 10;
            margin: 0;
            background-color: transparent;
            border-radius: 0; /* Remove radius here too */
        }
    }
</style>