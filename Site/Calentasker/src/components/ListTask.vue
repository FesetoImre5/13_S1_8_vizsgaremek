<template>
    <div class="Task">
        <img height="1000" width="1000" src="https://img.pokemondb.net/artwork/large/eevee.jpg" alt="" class="TaskImage">
        <div class="TaskText">
            <h2 class="TaskTitle">
                Title
            </h2>
            <div class="TaskDesc">
                <p>
                    This is a somewhat sort, but still padded sentence to function as a Description example. Yaay.
                    This is a somewhat sort, but still padded sentence to function as a Description example. Yaay.
                    This is a somewhat sort, but still padded sentence to function as a Description example. Yaay.
                    This is a somewhat sort, but still padded sentence to function as a Description example. Yaay.
                    This is a somewhat sort, but still padded sentence to function as a Description example. Yaay.
                    This is a somewhat sort, but still padded sentence to function as a Description example. Yaay.
                    This is a somewhat sort, but still padded sentence to function as a Description example. Yaay.
                    This is a somewhat sort, but still padded sentence to function as a Description example. Yaay.
                    This is a somewhat sort, but still padded sentence to function as a Description example. Yaay.
                    This is a somewhat sort, but still padded sentence to function as a Description example. Yaay.
                    This is a somewhat sort, but still padded sentence to function as a Description example. Yaay.
                    This is a somewhat sort, but still padded sentence to function as a Description example. Yaay.
                </p>
                <button>Details</button>
            </div>
        </div>
    </div>
</template>

<script>

</script>

<style scoped>
    .Task {
        display: flex;
        flex-direction: row;
        background-color: gray;
        border-radius: 15px;
        font-family: Arial, Helvetica, sans-serif;
        width: 100%;
        margin: 10px 0;
    }
    .TaskImage{
        max-width: 125px;
        height: 125px;
        aspect-ratio: 1/1;
        object-fit: cover;
        background-color: red;
        margin: 10px;
    }
    .TaskTitle{
        font-size: 40px;
        margin: 0;
        padding: 10px 0 0 0;
    }
    .TaskDesc{
        display: flex;
        flex-direction: row;
    }
    .TaskDesc p{
        margin: 0;
        padding: 10px 10px 0 0;
        display: -webkit-box;
        text-overflow: ellipsis;
        overflow: hidden;
        -webkit-box-orient: vertical;
        -webkit-line-clamp: 3;
        word-break: keep-all;
    }
    .TaskDesc button{
        font-size: 14px;
        font-weight: bold;
        height: 60px;
        margin: 0 10px;
        padding: 0 20px;
    }
</style>