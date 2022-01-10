<template>
    <div class="books">
        <br>
        <ItemsTable items="books"
                    :headers="headersTable"
                    :sort="defaulSort"/>
    </div>
</template>

<script>
import ItemsTable from '@/components/ItemsTable'

export default {
    name: 'BooksTable',
    components: {
        ItemsTable
    },
    setup() {
        const headersTable = {
            'Isbn': 'isbn',
            'Title': 'title',
            'Serie': 'serie',
            'Categories': 'categories',
            'Available': 'available',
        }

        const defaulSort = 'title'

        return { headersTable, defaulSort }
    }
}
</script>