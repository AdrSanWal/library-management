import { ref } from 'vue'

export default async function (method, path, options=null) {

    let response = ref({})
    const jsonResponse = ref(null)

    const urls = {
        'development': 'http://localhost:8000/',
        'production': '/'
    }

    const apiUrl = `${urls[process.env.NODE_ENV]}api/catalog/${path}`

    const opt = {
        method: method,
        headers:{
            'Content-Type': 'application/json'
            },
        ...options
    }
    const res = await fetch(apiUrl, opt)
    jsonResponse.value = await res.json()
    response.value = res

    return { response, jsonResponse }
}
