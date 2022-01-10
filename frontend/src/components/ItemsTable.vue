<template>
    <div class="container">
        <h2>List of {{ items }}</h2>

        <table id="table">

            <thead id="t-head">
                <tr>
                    <th>#</th>
                    <th v-for="(value, key, index) of headers" :key="index">{{ key }}</th>
                    <th class="h-right">
                        Add <i class="fas fa-external-link-alt"></i>
                    </th>  
                </tr>
            </thead>

            <tbody>
                <tr v-for="(item, index) of dataPage" :key="index">
                    <td>{{ (index + (rowsPage * (actualPage - 1 ))) + 1}}</td>
                    <td v-for="(value, key, index) of headers" :key="index">{{ item[value] }}</td>
                    <td class="exclude">
                        <div class="btn">
                            <button class="btn-edit btn-lst"><i class="fa-solid fa-pen-to-square"></i></button>
                            <button class="btn-del btn-lst"><i class="fa-solid fa-trash-can"></i></button>
                        </div>
                    </td>
                </tr>
            </tbody>

            <br>

            <tfoot id="t-foot">
                <tr>
                    <td :colspan="cols" id="t-subfoot">
                        <div class="f-item">{{ results }}  Results</div>
                        <div class="f-item right">Page {{ actualPage }} of {{ pages }}</div>
                    </td>
                    <td class="h-right">
                        <div class="dropdown" @mouseenter="show=true" @mouseleave="show=false">
                            <div id="selectRows">
                                <p>Rows <i class="fas fa-caret-down"></i></p>
                            </div>
                            <transition name="rows">
                                <ul v-if="show" class="changeRows">
                                    <li v-for="(n, i) in [5,10,25]"
                                        :key="i"
                                        @click="changeRows(n)">{{n}} rows
                                    </li>
                                </ul>
                            </transition>
                        </div>
                    </td>
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

        const show = ref(false)  // change to false when works

        const cols = Object.keys(headers).length + 1

        const sortedBy = ref('title')

        const path = `api/catalog/${items}/`

        const { rowsPage,
                dataPage,
                pages,
                actualPage,
                arrayLinks,
                results,
                getDataPage,
                changePage,
                changeLinks,
                changeRows } = usePaginationTable(path, sortedBy.value)


        return { cols,
                 items,
                 headers,
                 rowsPage,
                 dataPage,
                 pages,
                 actualPage,
                 arrayLinks,
                 results,
                 getDataPage,
                 changePage,
                 changeLinks,
                 changeRows,
                 sortedBy,
                 show }
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
    color: whitesmoke;
    font-size: larger;
}

#t-head {
    opacity: 0.7;
    background-color: var(--color-nav);
}

th {
    padding: 10px 20px;
    /*min-width: 55px;*/
}

td {
    padding: 5px 20px;
}

tr:nth-child(even){
    background-color: #d8941746;
}

tbody>tr:hover {
    background-color: rgb(221, 221, 221);
}

.btn {
    display: flex;
}

.btn-lst {
    padding: 8px;
    width: 30px;
}

.exclude {
    background-color: white;
    cursor:auto;
}

button {
    padding: 5px;
    width: 100px;
}

.h-right {
    background-color: var(--color-btn);
}

.h-right:hover {
    background-color: var(--color-hover);
    color:black;
}

/* Table foot ---------------------------------------------------- Table foot */

#t-foot {
    opacity: 0.6;
    background-color: var(--color-nav);
    color: whitesmoke;
    font-size: larger;
    font-weight: bold;
}

.f-item {
    display: inline-flex;

}

/* Change rows -------------------------------------------------- Change rows */

#selectRows > p {
    margin: 1px;
    height: 25px;
}

.right {
    float: right;
}

.changeRows {
    position: absolute;
    width: 108px;
    margin: 6px 0 0 -20px;
    padding: 0;
    list-style-type: none;
    transform-origin: top;
    transition: transform 0.5s ease-in-out;

}

li {
    
    padding: 10px;
    color:black;
    background: var(--color-hover);
    border-bottom: solid thin var(--color-nav);
    border-left: solid medium var(--color-nav);
  }

.rows-enter, .rows-leave-to{
    transform: scaleY(0);
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