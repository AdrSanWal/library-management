import { ref } from 'vue'

export default async function (method, path, options=null) {
    let response = ref({})
    const json_response = ref(null)

    const urls = {
        'development': 'http://localhost:8000/',
        'production': '/'
    }

    const apiUrl = urls[process.env.NODE_ENV] + path

    const opt = {
        method: method,
        headers:{
            'Content-Type': 'application/json'
            },
        options
    }

    const res = await fetch(apiUrl, opt)
    json_response.value = await res.json()
    response.value = res

    return { response, json_response }
}
