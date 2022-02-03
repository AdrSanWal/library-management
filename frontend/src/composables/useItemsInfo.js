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
            'isbn': 'text',
            'title': 'text',
            'cover': 'url',
            'authors': 'multiSelect',
            'serie': 'select',
            'serie_order': 'number',
            'categories': 'multiSelect',
            'description': 'textArea',
        },
        'authors': {
            'name': 'text',
            'pseudonym': 'text',
            'born': 'date',
            'died': 'date',
        },
        'categories': {
            'name': 'text',
            'description': 'textArea',
        },
        'series': {
            'name': 'text',
        }
    }

    return { itemsSortFields,
             itemsHeaders,
             itemsFormFields,
             itemsSingularName }
}
