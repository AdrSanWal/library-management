<template>
    <div class="container">
        <div class="book-container" v-if="origin==='books'">
            <ItemBook
                :book="data.results"/>
        </div>
        <div class="books-container" v-if="origin!=='books'">

            <div id="t-prev"
                :class="['changePage', {'disabled': !data.previous}]"
                @click="thumbnails.page--;$emit('changeData')">
                <i class="fas fa-chevron-left"></i>
            </div>
            <ItemBooks v-for="book of data.results" :key="book.id" :book="book"/>
            <div id="t-next"
                :class="['changePage', {'disabled': !data.next}]"
                @click="thumbnails.page++;$emit('changeData')">
                <i class="fas fa-chevron-right"></i>
            </div>
        </div>
    </div>
</template>

<script>
import ItemBook from '@/components/Items/Item/ItemBook'
import ItemBooks from '@/components/Items/Item/ItemBooks'

export default {
    name: 'ItemsDetail',
    components: {
        ItemBook,
        ItemBooks,
    },
    props: {
        id: String,
        data: Object,
        origin: String,
        thumbnails: Object,
    },
    setup() {

    }
}
</script>

<style scoped>

.container {
    margin-top: 60px;

}

.book-container {
    display: flex;
    justify-content: center;
}

.books-container {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    gap: 10px;
}

.changePage {
    display: grid;
    background-color: var(--color-hover);
    height: 60px;
    width: 60px;
    color: rgb(145, 145, 145);
    border-radius: 100%;
    border:1px solid var(--color-nav);
    font-size: xx-large;
    align-self: center;
}

.changePage:hover {
    border:5px solid var(--color-nav);
    color: var(--color-nav);
    height: 55px;
    width: 55px;
}

.changePage i {
    display: flex;
    align-self: center;
    justify-self: center;
    font-size:larger;
}

#t-prev {
    transform: translateX(30%);
}

#t-next {
    left:0%;
    transform: translateX(-30%);
}

.disabled {
    opacity:0;
}
</style>