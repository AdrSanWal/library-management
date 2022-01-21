<template>
    <div class="items">

        <ItemsTable v-if="id==='list'"
            :items="item"
            :query="queryData"
            :data="data"
            :headers="headersData[item]"
            @changeData="reloadData"/>

        <ItemsDetail v-if="id!=='list'"
            :id="id"
            :data="data"/>
    </div>
</template>

<script>
import useApi from '@/composables/useApi'
import ItemsTable from '@/components/ItemsTable'
import ItemsDetail from '@/components/ItemsDetail'
import { useRoute } from 'vue-router'
import { toRefs, reactive, onMounted } from 'vue'


export default {
    name: 'BooksTable',
    components: {
        ItemsTable,
        ItemsDetail,
    },
    setup() {
        
        const route = useRoute()

        const itemsSelection = reactive({
            id: route.params.id,
            item: route.params.items,
        })

        const initialSortFields = {
            'books': 'title',
            'authors': 'full_name',
            'categories': 'name',
            'series': 'name',
        }

        const queryData = reactive({
            sortField: initialSortFields[itemsSelection.item],
            rows: 5,  // num of initial rows
            page: 1
        })


        const headersData = {
            'books': {
                'Isbn': 'isbn',
                'Title': 'title',
                'Authors': 'authors',
                'Serie': 'serie',
                'Categories': 'categories',
                'Available': 'available'
            },
            'authors': {
                'Name': 'full_name',
                'Pseudonym': 'pseudonym',
                'Born': 'born',
                'Died': 'died',
            },
            'categories': {
                'Name': 'name',
                'Description': 'description'
            },
            'series': {
                'Name': 'name',
            },     
        }
        
        let path
        const data = reactive({
            results: [],
            count: 0,
            previous: null,
            next: null,
        })

        onMounted( async () => {
            reloadData(queryData)
        })

        const reloadData = (async (query) => {  // TODO rehacer
            
            let resp
            if (itemsSelection.id==='list') {
                path = `${itemsSelection.item}/?ordering=${queryData.sortField}&rows=${queryData.rows}&page=${queryData.page}`
                resp = (await useApi('get', path)).jsonResponse.value
                data.results = resp.results
                data.count = resp.count
                data.previous = resp.previous
                data.next = resp.next
            } else if (itemsSelection.item==='books') {
                path = `${itemsSelection.item}/${itemsSelection.id}/`
                resp = (await useApi('get', path)).jsonResponse.value
                data.results = resp
                data.count = 1
                data.previous = null
                data.next = null
            } else {
                path = `books/?${itemsSelection.item}=${itemsSelection.id}`
                resp = (await useApi('get', path)).jsonResponse.value
                data.results = resp.results
                data.count = resp.count
                data.previous = resp.previous
                data.next = resp.next
            }
        })

        return { data, headersData, ...toRefs(itemsSelection), queryData, reloadData }
    }
}
</script>