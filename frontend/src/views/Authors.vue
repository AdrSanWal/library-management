<template>
    <div class="authors">
        <br>
        <ItemsTable items="authors"
                    :headers="headersTable"
                    :sort="defaulSort"/>
    </div>
</template>

<script>
import ItemsTable from '@/components/ItemsTable'

export default {
    name: 'AuthorsTable',
    components: {
        ItemsTable
    },
    setup() {
        const headersTable = {
            'Name': 'full_name',
            'Pseudonym': 'pseudonym',
            'Born': 'born',
            'Died': 'died'
        }

        const defaulSort = 'full_name'

        return { headersTable, defaulSort }
    }
}
</script>