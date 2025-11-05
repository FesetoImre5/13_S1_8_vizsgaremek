<script>
  export default {
    data(){
      
    }
  }
</script>

<template>
  <div id="wrapper">
    <list-task v-for="x in items">
      <div>
        <img :src="x.url">
      </div>
      <div>
        <h3>{{ x.title }}</h3>
        <p>{{ x.description }}</p>
      </div>
    </list-task>
  </div>
</template>

<style scoped>

</style>
