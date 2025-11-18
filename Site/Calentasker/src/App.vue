<script>
  export default {
    data(){
      return {
        tasks: [
          {
            url: "https://img.pokemondb.net/artwork/large/eevee.jpg",
            title: "Eevee",
            desc: "Eevee is a small, mammalian, quadrupedal Pokémon with primarily brown fur. The tip of its bushy tail and its large furry collar are cream-colored. It has short, slender legs with three small toes and a pink paw pad on each foot. Eevee has brown eyes, long pointed ears with dark brown interiors, and a small black nose."
          },
        ],
        groups: []
      }
    }
  }
</script>

<template>
  <div>
    <div class="row">
      <div class="col-sm-1" style="background-color: red;">
        <list-group></list-group>
      </div>
      <div class="col-sm-7" style="background-color: blue;">    
        <div class="TaskList">
          <list-task 
            v-for="task in tasks"
            :url="task.url"
            :title="task.title"
            :desc="task.desc"
          />
        </div>
      </div>
      <div class="col-sm-4" style="background-color: green;">

      </div>
    </div>
  </div>
</template>

<style scoped>

</style>
