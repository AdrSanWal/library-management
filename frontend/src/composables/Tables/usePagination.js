import { reactive, toRefs } from 'vue'

export function changeLinks(direction) {
    const links = reactive ({
        numberOfLinks: 3,
        arrayLinks: [],
    })

    const range = (start, length=links.numberOfLinks) => Array.from(
        { length: length}, (_, i) => start + i
    )

    return { ...toRefs(links) }
        
}

export default function () {

    const changePage = ((direction) => {
        if (direction === '<' && 3 !== 1) {
            console.log(`direccion ${changeLinks(direction)}`)
        } else if (direction === '>' && 1 !== 2) {
            console.log('direccion >')
        }
    })

    return { changePage }

    // if (direction === '<' && props.query.page !== 1) {
    //     props.query.page--
    //     if (props.query.page<arrayLinks.value[0]) {
    //         arrayLinks.value = range(arrayLinks.value[0]-1)
    //     }
    //     emit('changeData', props.query)
    // } else if (direction === '>' && props.query.page !== props.data.totalPages) {
    //     props.query.page++
    //     if (props.query.page>arrayLinks.value.slice(-1)) {
    //         arrayLinks.value = range(arrayLinks.value[0]+1)
    //     }
    //     emit('changeData', props.query)
    // } else {
    //     console.log(direction)
    // }
}