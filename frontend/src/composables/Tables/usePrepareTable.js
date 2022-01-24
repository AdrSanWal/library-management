export function prepareData(data) {
    data.forEach(x => x.authors = x.authors.join(', '))
    data.forEach(x => x.categories = x.categories.join(', '))

    // const t = '<i class="fas fa-check"></i>'
    // const f = '<i class="fas fa-times"></i>'

    return data
}