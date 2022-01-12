<template>
    <div class="container">
        <h2>List of {{ items }}</h2>
        <table id="table">
            <thead id="t-head">
                <tr>
                    <th>#</th>
                    <th v-for="(value, key, index) of headers"
                        :key="index"
                        @click="sortField=value;sortByField(value)">
                            {{ key }} <i :class="['fas', 'fa-sort-down', {'active': value===sortField}]"></i>
                    </th>
                    <th class="h-right">
                        Add <i class="fas fa-external-link-alt"></i>
                    </th>  
                </tr>
            </thead>

            <tbody>
                <tr v-for="(item, index) of dataPage" :key="index">
                    <td>{{ (index + (rowsPage * (actualPage - 1 ))) + 1}}</td>
                    <!--<td v-for="(value, key, index) of headers" :key="index">{{ transform(item[value]) }}</td>-->
                    <td v-for="(value, key, index) of headers" :key="index">
                        {{ transform(items, item[value], key) }}
                        <i class="fas fa-check" v-if="item[value]===true"></i>
                        <i class="fas fa-times" v-if="item[value]===false"></i>
                    </td>
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
import { ref, onMounted, reactive } from 'vue'

export default {
    name: 'ItemsTable',
    props: {
        items: String,
        headers: Object,
        sort: String,
    },
    setup(props) {
        const items = props.items
        const headers = props.headers

        const show = ref(false)
        const sortField = ref(props.sort)

        const cols = Object.keys(headers).length + 1

        const path = `api/catalog/${items}/`

        const related = reactive({
            series: [],
            categories: []
        })

        onMounted( async () => {
            if (items==='books') {
                related.series = await getRelatedData('series')
                related.categories = await getRelatedData('categories')
            }
        })

        const transform = ((items, value, field) => {  // Transform data
            if (items!=='books') {
                return value
            } else {
                if (value===true || value===false) {
                    return ''
                } else {
                    if (field==='Serie') {
                        let serie = related.series.find(x => x.id === value)
                        return serie ? serie.name : null

                    } else if (field==='Categories') {
                        let categories = related.categories.filter(x => Object.values(value).includes(x.id))
                        console.log(categories.map(x => x.name))

                        return categories ? categories.map(x => x.name).join(', ') : null
                    }
                }
            }    
            return value
         })

        const { rowsPage,
                dataPage,
                pages,
                actualPage,
                arrayLinks,
                results,
                getDataPage,
                changePage,
                changeLinks,
                changeRows,
                sortByField,
                getRelatedData } = usePaginationTable(path, sortField)

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
                 show,
                 sortField,
                 sortByField,
                 transform }
    }
}
</script>

<style scope>


/* Tables ------------------------------------------------------------ Tables */

table {
    text-align: left;
    cursor:pointer;
    table-layout: fixed;
    max-width: 80%;
}

thead {
    color: whitesmoke;
    font-size: larger;
}

#t-head {
    opacity: 0.7;
    background-color: var(--color-nav);
}

th>.fa-sort-down {
    opacity: 0.3;
}

th>.active {
    opacity: 1;
}

th {
    padding: 10px 20px;
}

td {
    padding: 5px 20px;
    max-width: 600px;
}

tr:nth-child(even){
    background-color: #d8941746;
}

tbody>tr:hover {
    background-color: var(--color-hover);
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

.fa-check {
    color: green;
}

.fa-times {
    color:red;
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
    border: 1px solid var(--color-hover);
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