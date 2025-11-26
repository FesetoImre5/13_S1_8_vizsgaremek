<script>
    export default {
        props: {
            url: {
                type: String,
                default: "https://www.mariposakids.co.nz/wp-content/uploads/2014/08/image-placeholder2.jpg"
            },
            name: {
                type: String,
                default: "Group Name"
            }
        },
        computed: {
            // Generates "PU" from "Pokemon Unite" or "M" from "Minecraft"
            acronym() {
                if (!this.name) return '';
                return this.name
                    .split(' ')              // Split by spaces
                    .map(word => word[0])    // Take first letter of each word
                    .join('')                // Join them back
                    .substring(0, 2)         // Limit to max 2 letters (optional)
                    .toUpperCase();          // Make uppercase
            }
        }
    }
</script>

<template>
    <div class="listGroup">
        <img :src="url" alt="">
        
        <!-- Text Wrapper -->
        <div class="text-content">
            <span class="full-name">{{ name }}</span>
            <span class="acronym">{{ acronym }}</span>
        </div>
    </div>
</template>

<style scoped>
.listGroup {
    /* 1. Define this element as a container for query logic */
    container-type: inline-size;
    container-name: group-item;

    display: flex;
    flex-direction: row;
    align-items: center; /* Center vertically */
    background-color: gray;
    border-radius: 15px;
    font-family: Arial, Helvetica, sans-serif;
    width: 100%;
    margin: 10px auto;
    height: 60px; /* Fixed height helps with alignment during resizing */
    overflow: hidden; /* Prevents text from spilling out while resizing */
    transition: all 0.3s ease;
}

.listGroup img {
    width: 50px;
    height: 50px;
    aspect-ratio: 1/1;
    object-fit: cover;
    margin: 5px;
    border-radius: 10px;
    flex-shrink: 0; /* Prevents image from squishing */
}

.text-content {
    margin-left: 10px;
    white-space: nowrap;
}

.listGroup p, .full-name, .acronym {
    font-size: 20px;
    color: white; /* Added color for visibility on gray */
}

/* --- DEFAULT STATE (Wide) --- */
.acronym {
    display: none; /* Hide acronym by default */
}

/* --- STATE 2: MEDIUM WIDTH (Show Acronym, Hide Name) --- */
/* When the component is smaller than 180px but bigger than 70px */
@container group-item (max-width: 180px) {
    .full-name {
        display: none;
    }
    .acronym {
        display: block;
        font-weight: bold;
    }
}

/* --- STATE 3: SMALLEST WIDTH (Image Only) --- */
/* When the component is smaller than 80px */
@container group-item (max-width: 80px) {
    .text-content {
        display: none; /* Hide all text */
    }
    .listGroup {
        justify-content: center; /* Center the image */
        padding: 0;
    }
    .listGroup img {
        margin: 0; /* Remove margin to center perfectly */
    }
}
</style>