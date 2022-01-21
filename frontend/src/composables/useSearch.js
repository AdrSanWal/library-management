import { toRefs, reactive } from 'vue'
import useApi from '@/composables/useApi'

export default function (query) {
    
    const data = reactive({
        jsonAuthors: [],
        jsonBooks: [],
        jsonCategories: [],   
        jsonSeries: [],
    })

    const search = async query => {
        const getData = ( async (items, field) => {
            const path = `${items}/?q=${query}`
            const resp = await useApi('get', path)
            const results = resp.jsonResponse.value.results // .slice(0,5)
            return results.map(x => ({"id": x['id'], "field": x[field]}))

        })

        if (query === '') {
            Object.keys(data).forEach((i) => data[i] = []);  // set all in data to []
        } else {
        data.jsonAuthors = await getData('authors', 'full_name')
        data.jsonBooks = await getData('books', 'title')
        data.jsonCategories = await getData('categories', 'name')
        data.jsonSeries = await getData('series', 'name')
        }
    }

    return { ...toRefs(data), search }
}
