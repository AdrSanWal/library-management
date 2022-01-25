<template>
    <div class="container">

        <div id="itemsOptions">
            <p v-for="(field, items, index) of itemsFields" :key="index"
                @click="itemsSelected=items;search()"
                :class="[{'selected': items===itemsSelected}]">{{ items }}</p>
        </div>
        <div id="finder">
            <input id="fnd"
                type="text"
                placeholder="&#xF002; Search"
                v-model="query"
                autocomplete="off"
                @keyup="search()">
        </div>

        <div class="table">
            <DropdownSearch :item="itemsSelected" :data="jsonResults"/>
        </div>
    </div>
</template>

<script>
import DropdownSearch from '@/components/DropdownSearch'
import useApi from '@/composables/useApi'
import { toRefs, reactive } from 'vue'


export default {
    name: 'Home',
    components: {
        DropdownSearch,
    },
    setup() {
        const itemsFields = {
            'books': 'title',
            'authors': 'full_name',
            'categories': 'name',
            'series': 'name'}

        const data = reactive({
            itemsSelected: 'books',
            query: '',
            jsonResults: [],
        })

        const search = async () => {

            if (data.query === '') {
                data.jsonResults = []
            } else {
                const path = `${data.itemsSelected}/?q=${data.query}`
                const resp = await useApi('GET', path)
                const results = resp.jsonResponse.value
                data.jsonResults = results.map(x => ({"id": x['id'], "field": x[itemsFields[data.itemsSelected]]}))
            }
        }

        return { itemsFields, ...toRefs(data), search }
    }
}
</script>

<style scoped>

.container {
    
}


/* Finder ------------------------------------------------------------ Finder */

/* #finder {

}*/

#fnd { 
    font-family: monospace, Fontawesome;
    font-size: larger;
    margin: 10px auto;
    width: var(--width-fnd);
    height: 30px;
    padding: 6px 20px;
    border: 2px solid var(--color-nav);
    border-radius: var(--btn-radius);
    background-color: #ece9e3;
}


/* Options ---------------------------------------------------------- Options */

#itemsOptions {
    margin-top: 150px;
    width: var(--width-fnd);
    display: flex;
    font-size: large;
    font-weight: bold;
    color: var(--color-nav);
    padding: 0px 20px;
    justify-content: space-between;   
}

#itemsOptions>p {
    padding-bottom: 5px;
    cursor: pointer;
}

p.selected {
    border-bottom: 2px solid var(--color-nav);
}

/* Dropdowns ------------------------------------------------------ Dropdowns */

/* .table {
    display: flex;
    justify-content: center;
} */

</style>