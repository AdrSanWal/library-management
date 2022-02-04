<template>
    <div class="items">

        <ItemsTable v-if="id==='list'"
            :items="item"
            :query="queryData"
            :apiData="apiData"
            :headers="itemsHeaders[item]"
            @changeData="reloadData"/>

        <ItemsDetail v-if="id!=='list'"
            :id="id"
            :apiData="apiData"
            :items="item"
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
import { toRefs, reactive, onMounted } from 'vue'


export default {
    name: 'Table-Detail',
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
            rows: 5,  // num of initial rows
            page: 1,
        })
       
        const apiData = reactive({
            results: [],
            totalPages: 1,
            totalItems: 0,
            firstItemOnPage: 0,
            lastItemOnPage: 0,
            currentPage: 1,
            previous: false,
            next: false,
        })

        onMounted( () => {
            reloadData()
        })

        const reloadData = (async () => {
            let path
            let resp
            if (itemsSelection.id==='list') {
                path = `${itemsSelection.item}/?ordering=${queryData.sortField}&rows=${queryData.rows}&page=${queryData.page}`
                resp = (await useApi('get', path)).jsonResponse.value
                console.log('resp', typeof(resp))
                Object.keys(apiData).forEach((key) => {
                    apiData[key] = resp[key]
                })

            } else if (itemsSelection.item==='books') {
                path = `${itemsSelection.item}/${itemsSelection.id}/`
                resp = (await useApi('get', path)).jsonResponse.value
                console.log(resp)
                apiData.results = resp
                apiData.totalPages = 1
                apiData.previous = false
                apiData.next = false

            } else {
                path = `books/?${itemsSelection.item}=${itemsSelection.id}&rows=${thumbnails.number}&page=${thumbnails.page}`
                resp = (await useApi('get', path)).jsonResponse.value
                Object.keys(apiData).forEach((key) => {
                    apiData[key] = resp[key]
                })
            }
        })


        return { apiData,
                 itemsHeaders,
                 ...toRefs(itemsSelection),
                 thumbnails,
                 queryData,
                 reloadData }
    }
}
</script>