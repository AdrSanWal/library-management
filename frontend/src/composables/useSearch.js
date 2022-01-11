import { toRefs, reactive } from 'vue'
import useApi from '@/composables/useApi'

export default function (query) {
    
    const data = reactive({
        json_authors: [],
        json_books: [],
        json_categories: [],   
        json_series: [],
    })

    const search = async query => {
        const getData = ( async (items, field) => {
            const path = `api/catalog/${items}/?q=${query}`
            const resp = await useApi('get', path)
            
            return resp.json_response.value.map(x => ({"id": x['id'], "field": x[field]}))
        })

        if (query === '') {
            Object.keys(data).forEach((i) => data[i] = []);  // set all in data to []
        } else {
        data.json_authors = await getData('authors', 'full_name')
        data.json_books = await getData('books', 'title')
        data.json_categories = await getData('categories', 'name')
        data.json_series = await getData('series', 'name')
        }
    }

    return { ...toRefs(data), search }
}
