import { toRefs, reactive } from 'vue'
import useApi from '@/composables/useApi'

export default function (query) {
    
    const data = reactive({
        jsonResults: [],
    })

    const search = async (params, query) => {
        console.log('params', params)

        console.log('query', query)


        const getData = ( async (items, field) => {
            const path = `${items}/?q=${query}`
            const resp = await useApi('get', path)
            const results = resp.jsonResponse.value // .slice(0,5)
            return results.map(x => ({"id": x['id'], "field": x[field]}))

        })

        if (query === '') {
            Object.keys(data).forEach((i) => data[i] = []);  // set all in data to []
        } else {
        data.jsonResults = await getData('authors', 'full_name')
        }
    }

    return { ...toRefs(data), search }
}
