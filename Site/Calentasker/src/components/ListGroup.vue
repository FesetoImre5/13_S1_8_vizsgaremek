<template>
    <div class="ListGroup">
        <img height="1000" width="1000" src="https://img.pokemondb.net/artwork/large/eevee.jpg" alt="">
        <p>Csoportnév</p>
    </div>
</template>

<script>

</script>

<style scoped>
.ListGroup{
    display: flex;
    flex-direction: row;
    background-color: gray;
    border-radius: 15px;
    font-family: Arial, Helvetica, sans-serif;
    width: 100%;
    margin: 10px 0;
    align-content: center;
}
.ListGroup p{
    display: block;
    margin: auto;
}

.ListGroup img{
    max-width: 25px;
    height: 25px;
    aspect-ratio: 1/1;
    object-fit: cover;
    background-color: red;
    margin: 10px;
}
</style>