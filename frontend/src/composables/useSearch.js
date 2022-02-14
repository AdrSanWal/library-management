import { toRefs, reactive } from 'vue'
import useApi from '@/composables/useApi'

export default function (query) {
    
    const data = reactive({
        jsonResults: [],
    })

    const search = async (params, query) => {

        const getData = ( async (items, field) => {
                const path = `${items}/?q=${query}`
            const resp = await useApi('GET', path)
            const results = resp.jsonResponse.value // .slice(0,5)
            return results.map(x => ({"id": x['id'], "field": x[field]}))

        })

        if (query === '') {
            Object.keys(data).forEach((i) => data[i] = []);  // set all in data to []
        } else {
        data.jsonResults = await getData('authors', 'name')
        }
    }

    return { ...toRefs(data), search }
}
