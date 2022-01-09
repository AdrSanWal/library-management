import { reactive, toRefs, onMounted } from 'vue'


export default function (items) {
    // range array generator
    const range = (start, stop, step=1) => Array.from({ length: (stop - start) / step + 1}, (_, i) => start + (i * step))
    
    const data = reactive({
        rowsPage: 10,
        numLinks: 5,
        todos: [],
        pages: null,
        actualPage: 1,
        dataPage: [],
        arrayLinks: range(1, 5)  //(1, data.numLinks) 
    })

    let changeArrayLinks = (sign, number) => {
        // Take a number and add or subtract in the whole array
        if (sign === '+') {
            if (data.arrayLinks.at(-1) + data.numLinks > data.pages) {
                return data.arrayLinks = range(data.pages - data.numLinks, data.pages)
            } else {
                return data.arrayLinks = data.arrayLinks.map(x => x + number)
            }
            
        } else {
            if (data.arrayLinks[0] - data.numLinks < 1) {
                return data.arrayLinks = range(1, data.numLinks)
            } else {
                return data.arrayLinks = data.arrayLinks.map(x => x - number)
            }
        }
    }

    onMounted( async () => {
        //const path = './../../public/todos.json'

        const path = 'https://jsonplaceholder.typicode.com/todos'   
        const response = await fetch(path)
        data.todos = await response.json();
        data.pages = Math.ceil(data.todos.length / data.rowsPage)
        data.numLinks = Math.min(data.numLinks, data.pages)
        getDataPage(data.actualPage)  // To load page in page 1
    })

    let getDataPage = (page => {
        let start = (page * data.rowsPage) - data.rowsPage
        let end = (page * data.rowsPage)
        data.actualPage = page  // update actualPage value
        data.dataPage = data.todos.slice(start, end)
    })

    const changePage = (direction) => {
        if (direction === '<' && data.actualPage !== 1) {
            data.actualPage --
            getDataPage(data.actualPage)

            if (data.actualPage < data.arrayLinks[0]) {
                changeArrayLinks('-', 1)
            }
            
        } else if (direction === '>' && data.actualPage !== data.pages) {
            data.actualPage ++
            getDataPage(data.actualPage)

            if (data.actualPage > data.arrayLinks.at(-1)) {
                changeArrayLinks('+', 1)
            }
        } 
    }

    const changeLinks = (direction) => {
        if (direction === '<<' && data.arrayLinks[0] !== 1) {
            changeArrayLinks('-', data.numLinks)
            data.actualPage = Math.max(data.actualPage - data.numLinks, 1)

            getDataPage(data.actualPage)

        } else if (direction === '>>' && data.actualPage !== data.pages) {
            changeArrayLinks('+', data.numLinks)
            data.actualPage = Math.min(data.actualPage + data.numLinks, data.pages)

            getDataPage(data.actualPage)
        }
    }

    const changeRows = (rows) => {  // TODO da errores con los links
        data.rowsPage = rows
        data.pages = Math.ceil(data.todos.length / data.rowsPage)
        data.numLinks = Math.min(data.numLinks, data.pages)
        // If we change to more rows, it will be less pages. If we are on a high
        // page, it may be that with the change that page no longer exists
        data.actualPage = Math.min(data.actualPage, data.pages)
        if (!data.arrayLinks.includes(data.actualPage)) {
            data.arrayLinks = range(data.pages - data.numLinks, data.pages)
        }
        getDataPage(data.actualPage)
    }
  
    return { ...toRefs(data), getDataPage, changePage, changeLinks, changeRows }

}
