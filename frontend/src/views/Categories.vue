<template>
    <div class="categories">
        <br>
        <ItemsTable items="categories" :headers="headersTable"/>
    </div>
</template>

<script>
import ItemsTable from '@/components/ItemsTable'

export default {
    name: 'CategoriesTable',
    components: {
        ItemsTable
    },
    setup() {
        const headersTable = {
            'Name': 'name',
            'Description': 'description'
        }

        return { headersTable }
    }
}
</script>