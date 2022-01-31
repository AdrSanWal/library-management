export function capitalize(word) {
        return word.charAt(0).toUpperCase() + word.slice(1)
    }

export function compareObjects(items, iniObj, finObj) {
    // compare two objects. if the value for a key in finObj is different in iniObj, add it to updates
    
    // delete iniObj['created']
    // delete iniObj['updated']
    console.log('ini', iniObj, finObj)
    let updates = new Object
    

    if (items==='books') {
        // Object.keys(iniObj).forEach(key => {
        //     console.log(key, finObj[key])
        // })
    } else {
        Object.keys(iniObj).forEach(key => {
            if (iniObj[key]!==finObj[key]) {
                updates[key] = finObj[key]
            }
        })
    }
    return updates
}