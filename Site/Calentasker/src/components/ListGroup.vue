<script>

</script>

<template>
    <div class="listGroup">
        <img height="1000" width="1000" src="https://www.mariposakids.co.nz/wp-content/uploads/2014/08/image-placeholder2.jpg" alt="">
        <p>Csoportnév</p>
    </div>
</template>

<style scoped>
.listGroup{
    display: flex;
    flex-direction: row;
    background-color: gray;
    border-radius: 15px;
    font-family: Arial, Helvetica, sans-serif;
    width: 100%;
    margin: 10px 0;
    align-content: center;
}
.listGroup p{
    display: block;
    margin: auto;
}

.listGroup img{
    max-width: 50px;
    height: 50px;
    aspect-ratio: 1/1;
    object-fit: cover;
    background-color: red;
    margin: 5px;
    border-radius: 10px;
}
</style>