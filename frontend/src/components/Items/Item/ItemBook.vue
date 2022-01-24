<template>
    <div class="book-detail">
        <div class="col">
            <img id="cover" :src="book.cover" alt="">
        </div>
        <div class="col vert">
            <div id="book-title">
                <p id="title">{{ book.title }}</p>
                <p id="isAvailableAdv"
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
                <div id="isNotAvl"
                    v-if="!book.available">
                    <table>
                        <tr>
                            <th>Loan date</th>
                            <td>{{ book.loan_date }}</td>
                        </tr>
                        <tr>
                            <th>Return date</th>
                            <td>{{ book.expected_return_date }}</td>
                        </tr>
                    </table>
                    <button id="cancel" class="button bck-red"
                        @click="changeLoan(true)">
                        Cancel loan
                    </button>
                </div>
                <div id="isAvl"
                    v-if="book.available">
                    <button id="reserve" class="button bck-green"
                        @click="changeLoan(false)">
                        Reserve
                    </button>
                    {{ book.loan_date }}
                    <br>
                    {{ book.expected_return_date }}
                </div>

            </div>
        </div>
    </div>
</template>

<script>
import useApi from '@/composables/useApi'

export default {
    name: 'ItemBook',
    props: {
        book: Object,
    },
    setup(props) {

        const changeIsAvailable = ((value) => {
            const transformText = {'true': 'Available', 'false': 'Not Availabe'}
            return transformText[value]
        })

        const changeLoan = (async (value) => {
            const path = `books/${props.book.id}/`
            props.book.available = value

            const { jsonResponse } = await useApi('PATCH', path, {body: JSON.stringify({'available': props.book.available})})

            props.book.loan_date = jsonResponse.value.loan_date
            props.book.expected_return_date = jsonResponse.value.expected_return_date
        })

        return { changeIsAvailable, changeLoan }
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

#isAvailableAdv {
    color:whitesmoke;
    font-size: medium;
    font-weight: bold;
    padding: 5px;
}

#book-info {
    height: 100%;
    padding:10px;
}

table {
    text-align: justify;
}

table>tr>th {
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

#isNotAvl {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
}

#cancel {
    font-weight: bold;
    border: 1px solid rgb(161, 17, 17);
}

#reserve {
    width: 80%;
    font-weight: bold;
    border: 1px solid rgb(32, 114, 25);
}

</style>