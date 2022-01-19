export function sortByField(data, field) {
    let sortBy = ((arr, field) => {
        arr.sort(function (a, b) {
            return (a[field]===b[field]) ? 0
            : (b[field]===null || b[field]==='') ? 1
            : (a[field]===null || a[field]==='') ? -1
            : (a[field] < b[field]) ? -1 : 1;
        })
        return arr
    })
    return sortBy(data, field)
}
