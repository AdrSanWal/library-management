<template>
    <div class="books">
        <br>
        <ItemsTable items="books" :headers="headersTable"/>
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

        return { headersTable }
    }
}
</script>