<template>
    <div class="book-detail">
        <div class="col">
            <img id="cover" :src="book.cover" alt="">
        </div>
        <div class="col vert">
            <div id="book-title">
                <p id="title">{{ book.title }}</p>
                <p id="isAvailable"
                    :class="{'bck-green':book.available, 'bck-red':!book.available}" >{{ changeIsAvailable(book.available) }}</p>
            </div>
            <div id="book-info">
                <table id="book-table">
                    <tr>
                        <th>Isbn</th>
                        <td>{{ book.isbn }}</td>
                    </tr>
                    <tr>
                        <th>Authors</th>
                        <td>
                            <ul>
                                <li v-for="author of book.authors" :key="author">{{ author }}</li>
                            </ul>
                        </td>
                    </tr>
                    <tr>
                        <th>Categories</th>
                            <ul>
                                <li v-for="category of book.categories" :key="category">{{ category }}</li>
                            </ul>
                    </tr>
                    <tr v-if="book.serie">
                        <th>Serie</th>
                        <td>{{ book.serie }} ({{ book.serie_order}}º)</td>
                    </tr>
                    <tr>
                        <th>Description</th>
                        <td>{{ book.description }}</td>
                    </tr>
                </table>
                <br>
                <hr>
                <br>

            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'ItemBook',
    props: {
        book: Object,
    },
    setup() {

        const changeIsAvailable = ((value) => {
            const transformText = {'true': 'Available', 'false': 'Not Availabe'}
            return transformText[value]
        })

        return { changeIsAvailable }
    }
}
</script>

<style scope>
.book-detail {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    gap: 15px;
    border-radius: 10px;
    border: 3px solid var(--color-nav);
    padding: 15px;
    background-color: rgb(235, 235, 235);
    width: 65%;
}

.vert {
    display: flex;
    flex-direction: column;
    width: 100%;
    border-radius: var(--btn-radius);
}

#cover {
    padding:15px;
    border-radius: var(--btn-radius);
    background-color: var(--color-btn);
    width: 320px;
    height: 500px;
}

#book-title {
    display:flex;
    flex-direction: row;
    justify-content: space-between;
    border: 1px solid var(--color-btn);
    border-radius: var(--btn-radius);
    padding: 0 40px;
    background-color: var(--color-hover);
}

#title {
    font-size: larger;
    font-weight: bolder;
}

#isAvailable {
    color:whitesmoke;
    padding: 5px;
}

#book-info {
    height: 100%;
    padding:10px;
}

#book-table {
    text-align: justify;
}

#book-table>tr>th {
    width:100px;
    vertical-align: top;
}

#book-table>tr>td {
    text-align: justify;
}

hr {
    border: 1px solid var(--color-btn);
    opacity: 0.5;
}

</style>