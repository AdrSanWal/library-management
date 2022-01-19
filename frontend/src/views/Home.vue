<template>
    <div class="home">

        <div id="finder">
            <input id="fnd"
                type="text"
                placeholder="&#xF002; Search"
                v-model="query"
                autocomplete="off"
                @keyup="search(query)">
        </div>

        <div class="table">

            <DropdownSearch item="Author" :data="jsonAuthors"/>
            <DropdownSearch item="Categories" :data="jsonCategories"/>
            <DropdownSearch item="Series" :data="jsonSeries"/>
            <DropdownSearch item="Books" :data="jsonBooks"/>

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

        const { jsonAuthors,
                jsonBooks,
                jsonCategories,
                jsonSeries,
                search } = useSearch(query)

        return { jsonAuthors,
                 jsonBooks,
                 jsonCategories,
                 jsonSeries,
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