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
        
        <!-- Text Container -->
        <div class="taskText">
            <h2 class="taskTitle">{{title}}</h2>
            <!-- Description: Hidden on small screens via CSS -->
            <p class="taskDesc">{{ desc }}</p>
        </div>

        <!-- Button -->
        <button class="detailsBtn">Details</button>
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
        /* Removed min-width so it can shrink on small screens */
        /* min-width: 476px; */
        position: relative; /* Helps with positioning if needed */
        align-items: center; /* Vertically center items */
        padding-right: 15px; /* Spacing for button */
    }

    .taskImage{
        width: 125px;
        height: 125px;
        aspect-ratio: 1/1;
        object-fit: cover;
        margin: 10px;
        flex-shrink: 0;
        border-radius: 10px;
    }

    .taskText {
        flex-grow: 1; /* Takes up available space */
        padding: 10px;
        min-width: 0; /* Allows text truncation to work */
    }

    .taskTitle{
        font-size: 40px;
        margin: 0;
        padding: 0;
        line-height: 1.2;
    }

    .taskDesc{
        margin: 10px 0 0 0;
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
        padding: 10px 20px;
        border-radius: 15px;
        border: none;
        cursor: pointer;
        /* Default State (> 1000px): Button is on the right */
        background-color: #ddd; 
        white-space: nowrap;
        height: fit-content;
    }

    /* --- RESPONSIVE LOGIC (< 1000px) --- */
    @media (max-width: 1000px) {
        
        /* 1. Hide the description */
        .taskDesc {
            display: none;
        }

        /* 2. Make the button take up the space / stand out more */
        .detailsBtn {
            background-color: orangered; /* Example highlighting */
            color: white;
            margin-left: auto; /* Pushes button to far right */
        }
        
        /* Optional: Adjust title size if needed */
        .taskTitle {
            font-size: 30px;
        }
    }
</style>