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
        'books': {
            'Isbn': 'isbn',
            'Title': 'title',
            'Authors': 'authors',
            'Serie': 'serie',
            'Categories': 'categories',
            'Available': 'available'
        },
        'authors': {
            'Name': 'name',
            'Pseudonym': 'pseudonym',
            'Born': 'born',
            'Died': 'died',
        },
        'categories': {
            'Name': 'name',
            'Description': 'description'
        },
        'series': {
            'Name': 'name',
        },     
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
