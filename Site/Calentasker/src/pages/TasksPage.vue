<script>
import ListTask from '../components/ListTask.vue'
import ListGroup from '../components/ListGroup.vue'

    export default {
        components: {
            ListTask,
            ListGroup
        },
        data(){
            return {
                tasks: [
                    {
                        url: "https://img.pokemondb.net/artwork/large/eevee.jpg",
                        title: "Eevee",
                        desc: "Eevee is a small, mammalian, quadrupedal Pokémon with primarily brown fur. The tip of its bushy tail and its large furry collar are cream-colored. It has short, slender legs with three small toes and a pink paw pad on each foot. Eevee has brown eyes, long pointed ears with dark brown interiors, and a small black nose."
                    },
                    {
                        url: "https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/134.png",
                        title: "Vaporeon",
                        desc: "Vaporeon shares physical traits with aquatic animals and felids in appearance."
                    },
                ],
                groups: [
                    {
                        url: "https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/e8ddc4da-23dd-4502-b65b-378c9cfe5efa/dfgdksx-6cf30959-b9e8-4ee2-b16f-d438f59873a1.png/v1/fill/w_894,h_894/pokemon_unite_logo_by_jormxdos_dfgdksx-pre.png?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7ImhlaWdodCI6Ijw9MTI4MCIsInBhdGgiOiIvZi9lOGRkYzRkYS0yM2RkLTQ1MDItYjY1Yi0zNzhjOWNmZTVlZmEvZGZnZGtzeC02Y2YzMDk1OS1iOWU4LTRlZTItYjE2Zi1kNDM4ZjU5ODczYTEucG5nIiwid2lkdGgiOiI8PTEyODAifV1dLCJhdWQiOlsidXJuOnNlcnZpY2U6aW1hZ2Uub3BlcmF0aW9ucyJdfQ.6vGMaToIMoFZNLK_WgNExVJMMOTfTEehRZYNCIg4qbI",
                        name: "Pokemon Unite",
                    },
                    { 
                        url: "https://googiehost.com/blog/wp-content/uploads/2022/09/Minecraft-.png",
                        name: "Minecraft",
                    }
                ]
            }
        }
    }
</script>

<template>
    <div>
        <div class="container-fluid">
            <div class="row">
                <div class="col-sm-2" style="background-color: red;">
                    <list-group
                        v-for="group in groups"
                        :url="group.url"
                        :name="group.name"
                    />
                </div>
                <div class="col-sm-6" style="background-color: blue;">    
                    <div class="taskList">
                        <list-task 
                            v-for="task in tasks"
                            :url="task.url"
                            :title="task.title"
                            :desc="task.desc"
                        />
                    </div>
                </div>
                <div class="col-sm-4" style="background-color: green;"></div>
            </div>
        </div>
    </div>
</template>

<style scoped>

</style>
