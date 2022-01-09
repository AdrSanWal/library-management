<template>
    <div class="container">
        <h2>List of {{ items }}</h2>

        <table id="table">
            <thead>
                <tr>
                    <th>#</th>
                    <th v-for="(value, key, index) of headers" :key="index">{{ key }}</th>
                    <th class="add">
                        Add <i class="fas fa-external-link-alt"></i>
                    </th>  
                </tr>
            </thead>

            <tbody>
                <tr v-for="(item, index) of dataPage" :key="index">
                    <td>{{ index +1 }}</td>
                    <td v-for="(value, key, index) of headers" :key="index">{{ item[value] }}</td>
                    <td class="exclude">
                        <button class="btn-edit btn-lst"><i class="fa-solid fa-pen-to-square"></i></button>
                        <button class="btn-del btn-lst"><i class="fa-solid fa-trash-can"></i></button>
                    </td>
                </tr>
            </tbody>
 
            <tfoot>
                <br>
                <tr>
                    <td colspan="2" class="exclude">Page {{ actualPage }} of {{ pages }}</td>
                </tr>
            </tfoot>
        </table>

        <br>
        <!-- Page navigation numbers. If there is only one page, it is not displayed -->
        <nav aria-label="Page navigation example" v-if="pages > 1">
                
            <div class="pagination">

                <a @click="changePage('<')"
                    :class="['page-item', {'disabled': actualPage===1}]">
                        <i class="fas fa-chevron-left"></i>
                </a>

                <a @click="getDataPage(page)"
                    v-for="page in arrayLinks"
                    :key="page"
                    :class="['page-item', {'active': page===actualPage}]">
                        {{ page }}
                </a>

                <a @click="changePage('>')"
                    :class="['page-item', {'disabled': actualPage===pages}]">
                        <i class="fas fa-chevron-right"></i>
                </a>
            </div>
        </nav>

    </div>
</template>

<script>
import usePaginationTable from '@/composables/usePaginationTable'
import { ref } from 'vue'

export default {
    name: 'ItemsTable',
    props: {
        items: String,
        headers: Object,
    },
    setup(props) {
        const items = props.items
        const headers = props.headers

        const sortedBy = ref('title')

        const path = `api/catalog/${items}/`

        const { rowsPage,
                dataPage,
                pages,
                actualPage,
                arrayLinks,
                getDataPage,
                changePage,
                changeLinks,
                changeRows } = usePaginationTable(path, sortedBy.value)


        return { items,
                 headers,
                 rowsPage,
                 dataPage,
                 pages,
                 actualPage,
                 arrayLinks,
                 getDataPage,
                 changePage,
                 changeLinks,
                 changeRows,
                 sortedBy }
    }
}
</script>

<style scope>

/* Tables ------------------------------------------------------------ Tables */

table {
    text-align: left;
    cursor:pointer;
    table-layout: fixed;
    max-width: 60%;
}

thead {
    background-color: var(--color-nav);
    opacity: 0.5;
    color: whitesmoke;
    font-size: larger;
}

th {
    padding: 10px 20px;
    /*min-width: 55px;*/
}

td {
    padding: 5px 20px;
}

tr:nth-child(even){
    background-color: #faddc2;
}

tbody>tr:hover {
    background-color: rgb(221, 221, 221);
}

.btn-lst {
    padding: 4px;
    width: 25px;
}

.exclude {
    background-color: white;
    cursor:auto;
}

button {
    padding: 5px;
    width: 100px;
}

.add {
    background-color:var(--color-btn);
}

/* Pagination ---------------------------------------------------- Pagination */

.pagination {
    display: inline-block;
}

.pagination a {
  color: var(--color-nav);
  float: left;
  padding: 8px 16px;
  text-decoration: none;
  border: 1px solid rgb(214, 211, 211);
  margin: 0 2px;
}

.pagination a.active {
  background-color: var(--color-btn);
  color: white;
}

.page-item {
    cursor: pointer;
}

</style>