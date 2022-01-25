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
            <transition name="matches">
                <div class="drpdwn" v-if="jsonResults">
                    <div class="col-drp">
                        <p>{{ itemsSelected }}</p>
                    </div>
                    <div class="col-drp">
                        <ul class="list">
                            <li v-for="x of jsonResults" :key="x.id">{{ x.field }}</li>
                        </ul>
                    </div>
                </div>
            </transition>
        </div>
    </div>
</template>

<script>
import useApi from '@/composables/useApi'
import { toRefs, reactive } from 'vue'


export default {
    name: 'Home',
    setup() {
        const itemsFields = {
            'books': 'title',
            'authors': 'full_name',
            'categories': 'name',
            'series': 'name'}

        const data = reactive({
            itemsSelected: 'books',
            query: '',
            jsonResults: null,
        })

        const search = async () => {
            if (data.query === '') {
                data.jsonResults = null
            } else {
                const path = `${data.itemsSelected}/?q=${data.query}`
                const resp = await useApi('GET', path)
                const results = resp.jsonResponse.value
                if (Object.keys(results).length === 0) {
                    data.jsonResults = null
                } else {
                    data.jsonResults = results.map(x => ({"id": x['id'], "field": x[itemsFields[data.itemsSelected]]}))
                }
            }
        }
        return { itemsFields, ...toRefs(data), search }
    }
}
</script>

<style scoped>


/* Finder ------------------------------------------------------------ Finder */

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
    border-bottom: 3px solid var(--color-btn);
}

/* Dropdowns ------------------------------------------------------ Dropdowns */

.table {
    width: var(--width-fnd);
}

.drpdwn {
    margin: 15px;
    padding: 0;
    list-style-type: none;
    transform-origin: top;
    transition: transform 0.5s ease-in-out;
}



.col-drp>p {
    background-color: var(--color-nav);
    color:whitesmoke;
    padding: 10px;
    font-size: larger;
    font-weight: bold;

}

.col-drp>ul {
    background-color: var(--color-hover);
    list-style-type: none;
    margin: 0;
    padding: 0;
}

.list>li {
    padding: 15px 10px;
    font-size: large;
}

.list>li:hover {
    background-color: rgb(201, 195, 195);
    cursor: pointer;
}

.matches-leave-to {
    transform: scaleY(0);
}

</style>