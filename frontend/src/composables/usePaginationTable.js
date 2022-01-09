import { ref, reactive, toRefs, onMounted } from 'vue'
import useApi from '@/composables/useApi'

export default function (path, sortedBy) {
    // range array generator
    const numLinks = ref(3)
    const range = (start) => Array.from({ length: numLinks.value}, (_, i) => start + i)
    
    
    const data = reactive({
        rowsPage: 10,
        dataPage: [],
        pages: 1,
        actualPage: 1,
        json: [],
        arrayLinks: range(1, numLinks.value) 
    })

    onMounted( async () => {
        const { json_response } = await useApi('get', path)
        data.json = json_response.value
        data.pages = Math.ceil(data.json.length / data.rowsPage)
        numLinks.value = Math.min(numLinks.value, data.pages)

        getDataPage(data.actualPage)
    })

    // let sortBy = ((arr, field) => {
    //     arr.sort(function (a, b) {
    //         var fieldA = a[field];
    //         var fieldB = b[field];
    //         return (fieldA < fieldB) ? -1 : (fieldA > fieldB) ? 1 : 0;
    //       });
    //     return arr
    // })

    let getDataPage = (page => {
        // data.json = sortBy(data.json, sortedBy)
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
                data.arrayLinks = range(data.arrayLinks[0] - 1)
            }
            
        } else if (direction === '>' && data.actualPage !== data.pages) {
            data.actualPage ++
            getDataPage(data.actualPage)
            if (data.actualPage > data.arrayLinks.at(-1)) {
                data.arrayLinks = range(data.arrayLinks[0] + 1)
            }
        } 
    }

    const changeRows = (rows) => {
        data.rowsPage = rows
        data.pages = Math.ceil(data.json.length / data.rowsPage)
        numLinks.value = Math.min(numLinks.value, data.pages)
        // If we change to more rows, it will be less pages. If we are on a high
        // page, it may be that with the change that page no longer exists
        data.actualPage = Math.min(data.actualPage, data.pages)
        if (!data.arrayLinks.includes(data.actualPage)) {
            data.arrayLinks = range(data.pages - numLinks.value, data.pages)
        }
        getDataPage(data.actualPage)
    }
  
    return { ...toRefs(data), getDataPage, changePage, changeRows }

}
