<template>
    <div class="container">
        <div class="book-container" v-if="items==='books'">
            <ItemBook
                :book="apiData.results"/>
        </div>

        <div class="books-container" v-if="items!=='books' && apiData.results.length!==0">

            <div id="t-prev"
                :class="['changePage', {'disabled': !apiData.previous}]"
                @click="thumbnails.page--;$emit('changeData')">
                <i class="fas fa-chevron-left"></i>
            </div>
            <ItemBooks v-for="book of apiData.results" :key="book.id" :book="book"/>
            <div id="t-next"
                :class="['changePage', {'disabled': !apiData.next}]"
                @click="thumbnails.page++;$emit('changeData')">
                <i class="fas fa-chevron-right"></i>
            </div>
        </div>

        <div v-show="apiData.results.length===0"
            id="no-books">
            <img src="https://zum-talent.ecore.com.sg/assets/frontend/image/no_result.jpeg" alt="">
            <h1>This {{itemsSingularName[items]}} has not books yet</h1>
            <div class="add-book">
                <h3>Maybe you want to add some one</h3>
                <i class="fas fa-arrow-right"></i>
                <button class="bck-green"
                @click="$router.push({name: 'Forms', params: {items: 'books', option: 'add', id: 'new'}})">
                    <i class="fa-solid fa-pen-to-square"></i> Add Book</button>
            </div>
        </div>
    </div>
</template>

<script>
import useItemsInfo from '@/composables/useItemsInfo'
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
        apiData: Object,
        items: String,
        thumbnails: Object,
    },
    setup() {
        const { itemsSingularName } = useItemsInfo()

        return { itemsSingularName }
    }
}

</script>

<style scoped>

.container {
    margin-top: var(--margin-top);
}

.book-container {
    display: flex;
    justify-content: center;
    width: 65%;
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

.fa-arrow-right {
    color: var(--color-btn)
}

.add-book {
    display: flex;
    flex-direction: row;
    justify-content: space-around;
    align-items: center;
    padding: 0px 70px;
}

</style>
