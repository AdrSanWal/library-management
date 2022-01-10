<template>
    <div class="categories">
        <br>
        <ItemsTable items="categories"
                    :headers="headersTable"
                    :sort="defaulSort"/>
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

        const defaulSort = 'name'

        return { headersTable, defaulSort }
    }
}
</script>