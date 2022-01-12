import { reactive, toRefs, onMounted } from 'vue'
import useApi from '@/composables/useApi'

export default function (path, sortField) {
    // range array generator
    const initialLinks = 3
    const range = (start, length=initialLinks) => Array.from(
        { length: length}, (_, i) => start + i
    )
    
    
    const data = reactive({
        numLinks: initialLinks,
        rowsPage: 10,
        dataPage: [],
        pages: 1,
        actualPage: 1,
        json: [],
        arrayLinks: range(1, initialLinks),
        results: 0
    })

    onMounted( async () => {
        const { json_response } = await useApi('get', path)
        data.json = sortBy(json_response.value, sortField.value) // sort by default field
        data.results = data.json.length
        data.pages = Math.ceil(data.json.length / data.rowsPage)
        data.numLinks = Math.min(data.numLinks, data.pages)

        getDataPage(data.actualPage)
    })

    let sortBy = ((arr, field) => {
        arr.sort(function (a, b) {
            return (a[field]===b[field]) ? 0
            : (b[field]===null || b[field]==='') ? 1
            : (a[field]===null || a[field]==='') ? -1
            : (a[field] < b[field]) ? -1 : 1;
        })
        return arr
    })

    let sortByField = (field => {
        data.json = sortBy(data.json, field)
        getDataPage(data.actualPage)
    })


    let getDataPage = (page => {
        let start = (page * data.rowsPage) - data.rowsPage
        let end = (page * data.rowsPage)
        data.actualPage = page  // update actualPage value
        data.dataPage = data.json.slice(start, end)
    })

    const changePage = (direction) => {
        if (direction === '<' && data.actualPage !== 1) {
            data.actualPage --
            getDataPage(data.actualPage)

            if (data.actualPage < data.arrayLinks[0]) {
                data.arrayLinks = range(data.arrayLinks[0] - 1, data.numLinks)
            }
            
        } else if (direction === '>' && data.actualPage !== data.pages) {
            data.actualPage ++
            getDataPage(data.actualPage)
            if (data.actualPage > data.arrayLinks.at(-1)) {
                data.arrayLinks = range(data.arrayLinks[0] + 1, data.numLinks)
            }
        } 
    }

    const changeRows = (rows) => {
        data.rowsPage = rows
        data.pages = Math.ceil(data.results / data.rowsPage)
        data.numLinks = Math.min(initialLinks, data.pages)
        data.actualPage = 1
        data.arrayLinks = range(1, data.numLinks)

        getDataPage(data.actualPage)
    }

    const getRelatedData = (async field => {
        const response = await useApi('get', `api/catalog/${field}/`)
        return response.json_response.value
    })
  
    return { ...toRefs(data),
                getDataPage,
                changePage,
                changeRows,
                sortByField,
                getRelatedData }

}