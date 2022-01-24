<template>
    <div @click="$router.push({name: 'Items', params: {items: 'books', id: book.id}})">
        <img class="thumbnail" :src="book.cover" alt="">
    </div>
</template>

<script>
import { inject } from 'vue'

export default {
    name: 'ItemBooks',
    props: {
        book: Object,
    },
    setup() {

    }
}
</script>

<style>
.thumbnail {
    height: 300px;
    width: 190px;
    padding: 15px;
    border: 2px solid var(--color-btn);
    border-radius: var(--btn-radius);
    background-color: whitesmoke;
}

.thumbnail:hover {
    padding: 5px;
    height: 320px;
    width: 210px;
}

</style>