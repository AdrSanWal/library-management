<template>
    <div class="items">
        <br>
        <ItemsTable v-if="id==='list'"
            :items="item"
            :data="data"
            :headers="itemsData[item].headers"
            :sortField="itemsData[item].sortField"/>

        <BookDetail v-if="id!=='list'"
            :id="id"
            :data="data"/>
    </div>
</template>

<script>
import useApi from '@/composables/useApi'
import ItemsTable from '@/components/ItemsTable'
import BookDetail from '@/components/BookDetail'
import { useRoute, useRouter } from 'vue-router'
import { ref, toRefs, reactive, onMounted } from 'vue'


export default {
    name: 'BooksTable',
    components: {
        ItemsTable,
        BookDetail,
    },
    setup() {
        
        const route = useRoute()
        const router = useRouter()

        const itemsSelection = reactive({
            id: route.params.id,
            item: route.params.items,
        })

        const data = ref()

        const itemsData = {
            'books': {
                'headers': {
                    'Isbn': 'isbn',
                    'Title': 'title',
                    'Authors': 'authors',
                    'Serie': 'serie',
                    'Categories': 'categories',
                    'Available': 'available'
                },
                'sortField': 'title',
            },
            'authors': {
                'headers': {
                    'Name': 'full_name',
                    'Pseudonym': 'pseudonym',
                    'Born': 'born',
                    'Died': 'died',
                },
                'sortField': 'full_name',
            },
            'categories': {
                'headers': {
                    'Name': 'name',
                    'Description': 'description'
                },
                'sortField': 'name',
            },
            'series': {
                'headers': {
                    'Name': 'name',
                },
                'sortField': 'name',
            },     
        }


        onMounted( async () => {

        let path
        if (itemsSelection.id==='list') {
            path = `${itemsSelection.item}/`
        } else if (itemsSelection.item==='books') {
            path = `${itemsSelection.item}/${itemsSelection.id}/`
        } else {
            path = `books/?${itemsSelection.item}=${itemsSelection.id}`
        }

        const res = await useApi('get', path)
        data.value = res.jsonResponse.value
        })

        return { data, itemsData, ...toRefs(itemsSelection) }
    }
}
</script>