<template>
    <div id="thumbnail-group" @click="$router.push({name: 'Items', params: {items: 'books', id: book.id}})">
        <div id="thumbnail-img">
            <img class="thumbnail" :src="book.cover" alt="">
        </div>
        <div id="thumbnail-title">
            <p>{{ book.title }}</p>
        </div>
    </div>
</template>

<script>
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

#thumbnail-group {
    width: 220px;
    height: 100%;
    box-shadow: 0 5px 5px 10px rgba(0, 0, 0, 0.2);
    border-radius: var(--btn-radius);
    cursor: pointer;
}

.thumbnail {
    height: 300px;
    width: 190px;
}

#thumbnail-img {
    padding:15px;
    border-radius: var(--btn-radius) var(--btn-radius) 0px 0px;
    background-color: whitesmoke;
}

#thumbnail-title {
    height: 20%;
    border-radius: 0px 0px var(--btn-radius) var(--btn-radius);
    border: 2px solid var(--color-nav);
    font-size: 16px;
    font-weight: bold;
    background-color: var(--color-nav);
    color: whitesmoke;
    display: flex;
    align-items: center;
    justify-content: center;

}

#thumbnail-group:hover .thumbnail{
    transform: scale(105%);
}

#thumbnail-group:hover{
    transform: scale(110%);
    box-shadow: 0 5px 20px rgba(0, 0, 0, 1);
}

</style>
