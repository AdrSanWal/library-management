import { reactive, toRefs } from 'vue'
import { sortByField } from '@/composables/Tables/useSortTable'


export default function (dataJson) {
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
        arrayLinks: range(1, initialLinks),
        results: 0
    })

    let getDataPage = (page => {
        let start = (page * data.rowsPage) - data.rowsPage
        let end = (page * data.rowsPage)
        data.actualPage = page  // update actualPage value
        data.dataPage = data.json.slice(start, end)

    })

    return { ...toRefs(data), getDataPage }

}
