export default function () {
    const itemsSortFields = {
        'books': 'title',
        'authors': 'name',
        'categories': 'name',
        'series': 'name',
    }
    const itemsSingularName = {
        'books': 'book',
        'authors': 'author',
        'categories': 'category',
        'series': 'serie',
    }

    const itemsHeaders = {
        'books': [
            'isbn',
            'title',
            'authors',
            'serie',
            'categories',
            'available'
        ],
        'authors': [
            'name',
            'pseudonym',
            'born',
            'died',
        ],
        'categories': [
            'name',
            'description'
        ],
        'series': [
            'name',
         ],     
    }

    const itemsFormFields = {
        'books': {
            'isbn': {'type': 'text', 'value': ''},
            'title': {'type': 'text', 'value': ''},
            'cover': {'type': 'url', 'value': ''},
            'authors': {'type': 'multiSelect', 'value':[]},
            'serie': {'type': 'select', 'value': ''},
            'serie_order': {'type': 'number', 'value': ''},
            'categories': {'type': 'multiSelect', 'value':[]},
            'description': {'type': 'textArea', 'value': ''},
        },
        'authors': {
            'name': {'type': 'text', 'value': ''},
            'pseudonym': {'type': 'text', 'value': ''},
            'born': {'type': 'date', 'value': ''},
            'died': {'type': 'date', 'value': ''},
        },
        'categories': {
            'name': {'type': 'text', 'value': ''},
            'description': {'type': 'textArea', 'value': ''},
        },
        'series': {
            'name': {'type': 'text', 'value': ''},
        }
    }

    return { itemsSortFields,
             itemsHeaders,
             itemsFormFields,
             itemsSingularName }
}
