<template>
    <div class="items">

        <ItemsTable v-if="id==='list'"
            :items="item"
            :query="queryData"
            :data="data"
            :headers="itemsHeaders[item]"
            @changeData="reloadData"/>

        <ItemsDetail v-if="id!=='list'"
            :id="id"
            :data="data"
            :origin="item"
            :thumbnails="thumbnails"
            @changeData="reloadData"/>
    </div>
</template>

<script>
import useItemsInfo from '@/composables/useItemsInfo'
import useApi from '@/composables/useApi'
import ItemsTable from '@/components/Items/ItemsTable'
import ItemsDetail from '@/components/Items/ItemsDetail'
import { useRoute } from 'vue-router'
import { toRefs, reactive, onMounted, ref } from 'vue'


export default {
    name: 'BooksTable',
    components: {
        ItemsTable,
        ItemsDetail,
    },
    setup() {

        const thumbnails = reactive({
            number: Math.floor((window.innerWidth-321)/234),
            page: 1,
        })
        
        const route = useRoute()

        const itemsSelection = reactive({
            id: route.params.id,
            item: route.params.items,
        })

        const { itemsSortFields, itemsHeaders } = useItemsInfo()

        const queryData = reactive({
            sortField: itemsSortFields[itemsSelection.item],
            rows: 10,  // num of initial rows
            page: 1,
        })
       
        let path
        const data = reactive({
            results: [],
            totalPages: 1,
            totalItems: 0,
            firstItemOnPage: 0,
            lastItemOnPage: 0,
            currentPage: 1,
            previous: false,
            next: false,
        })

        onMounted( async () => {
            reloadData()
        })

        const reloadData = (async () => {

            let resp
            if (itemsSelection.id==='list') {
                path = `${itemsSelection.item}/?ordering=${queryData.sortField}&rows=${queryData.rows}&page=${queryData.page}`
                resp = (await useApi('get', path)).jsonResponse.value
                Object.keys(data).forEach((key) => {
                    data[key] = resp[key]
                })

            } else if (itemsSelection.item==='books') {
                path = `${itemsSelection.item}/${itemsSelection.id}/`
                resp = (await useApi('get', path)).jsonResponse.value
                data.results = resp
                data.totalPages = 1
                data.previous = false
                data.next = false
            } else {
                path = `books/?${itemsSelection.item}=${itemsSelection.id}&rows=${thumbnails.number}&page=${thumbnails.page}`
                resp = (await useApi('get', path)).jsonResponse.value
                Object.keys(data).forEach((key) => {
                    data[key] = resp[key]
                })
            }
        })


        return { data,
                 itemsHeaders,
                 ...toRefs(itemsSelection),
                 thumbnails,
                 queryData,
                 reloadData }
    }
}
</script>