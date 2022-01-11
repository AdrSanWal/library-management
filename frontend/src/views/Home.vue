<template>
    <div class="home">

        <div id="finder">
            <input id="fnd"
                type="text"
                placeholder="&#xF002; Search"
                v-model="query"
                @keyup="search(query)">
        </div>

        <div class="table">

            <DropdownSearch item="Author" :data="json_authors"/>
            <DropdownSearch item="Categories" :data="json_categories"/>
            <DropdownSearch item="Series" :data="json_series"/>
            <DropdownSearch item="Books" :data="json_books"/>

        </div>
    </div>
</template>

<script>
import DropdownSearch from '@/components/DropdownSearch'
import useSearch from '@/composables/useSearch'
import { ref } from 'vue'


export default {
    name: 'Home',
    components: {
        DropdownSearch,
    },
    setup() {
        const query = ref('')

        const { json_authors,
                json_books,
                json_categories,
                json_series,
                search } = useSearch(query)

        return { json_authors,
                 json_books,
                 json_categories,
                 json_series,
                 search,
                 query }
    }
}
</script>

<style scoped>

.home {
    margin-top: 150px;
}


/* Finder ------------------------------------------------------------ Finder */

#finder {
    display: flex;
    justify-content: center;
}

#fnd {
    font-family: monospace, Fontawesome;
    font-size: larger;
    margin: 10px auto;
    width: 500px;
    height: 30px;
    padding: 6px 20px;
    border: 2px solid var(--color-nav);
    border-radius: var(--btn-radius);
    background-color: #ece9e3;
}


/* Dropdowns ------------------------------------------------------ Dropdowns */

.table {
    display: flex;
    justify-content: center;
}

</style>