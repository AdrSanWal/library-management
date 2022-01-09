<template>
    <div class="series">
        <br>
        <ItemsTable items="series" :headers="headersTable"/>
    </div>
</template>

<script>
import ItemsTable from '@/components/ItemsTable'

export default {
    name: 'SeriessTable',
    components: {
        ItemsTable
    },
    setup() {
        const headersTable = {
            'Name': 'name',
        }

        return { headersTable }
    }
}
</script>