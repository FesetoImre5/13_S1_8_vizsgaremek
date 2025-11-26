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
        </div>
        <button>Details</button>
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
    }
    .taskImage{
        max-width: 125px;
        height: 125px;
        aspect-ratio: 1/1;
        object-fit: cover;
        margin: 10px;
    }
    .taskTitle{
        font-size: 40px;
        margin: 0;
        padding: 10px 0 0 0;
    }
    .taskDesc{
        display: flex;
        flex-direction: row;
        margin: 0;
        padding: 10px 10px 0 0;
        display: -webkit-box;
        text-overflow: ellipsis;
        overflow: hidden;
        -webkit-box-orient: vertical;
        -webkit-line-clamp: 3;
        word-break: keep-all;
    }
    button{
        font-size: 14px;
        font-weight: bold;
        margin: 0 0 0 auto;
        padding: 0 20px;
        border-radius: 0 15px 15px 0;
        float: right;
    }
</style>