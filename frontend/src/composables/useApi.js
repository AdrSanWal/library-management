import { ref, inject } from 'vue'

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

    //const isLoading = inject('isLoading')
    //isLoading.value = true

    const res = await fetch(apiUrl, opt)
    if (res.status===204) {return}
    jsonResponse.value = await res.json()
    response.value = res
    
    //isLoading.value = false

    return { response, jsonResponse }
}
