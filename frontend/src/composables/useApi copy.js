import { ref, onMounted } from 'vue'

export default function (method, items, options=null) {
    let response = ref({})
    const json_response = ref({})

    const urls = {
        'development': 'http://localhost:8000/',
        'production': '/'
    }

    const apiUrl = urls[process.env.NODE_ENV] + 'api/catalog'


    onMounted( async () => {
        
        const opt = {
            method: method,
            headers:{
                'Content-Type':'application/json'
                },
            options
        }

        const res = await fetch(apiUrl + '/' + items + '/', opt)
        json_response.value = await res.json()
        response.value = res
    })

    const table = {
        'authors': {
            'Name': 'full_name',
            'Pseudonym': 'pseudonym',
            'Born': 'born',
            'Died': 'died'
        },
        'categories': {
            'Name': 'name',
            'Description': 'description'
        },
        'series': {
            'Name': 'name'
        },
        'books': {
            'Isbn': 'isbn',
            'Title': 'title',
            'Serie': 'serie',
            'Categories': 'categories',
            'Available': 'available',
        }
    }

    return { response, json_response, table }
}
