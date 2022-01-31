<template>
    <div class="container">
        <h2>List of {{ items }}</h2>
        <table id="table">
            <thead id="t-head">
                <tr class="headers">
                    <th>#</th>
                    <th v-for="(value, key, index) of headers"
                        :key="index"
                        @click="query.sortField=value;$emit('changeData', query)">
                            {{ key }} <i :class="['fas', 'fa-sort-down', {'selected': value===query.sortField}]"></i>
                    </th>
                    <th class="h-right"
                        @click="$router.push({name: 'Forms', params: {items: items, option: 'add', id: 'new'}})">
                        Add <i class="fas fa-external-link-alt"></i>
                    </th>  
                </tr>
            </thead>

            <tbody>
                <tr v-for="(item, index) of data.results"
                    :key="index"
                    @click="$router.push({name: 'Items', params: {id: item.id}})">
                    <td>{{ (index + (query.rows * (data.currentPage - 1 ))) + 1}}</td>
                    <td v-for="(value, key, index) of headers"
                        :key="index">
                        <span>{{ item[value] }}</span>
                    </td>
                    <td class="exclude" @click.stop>
                        <div class="btn">
                            <button class="bck-green btn-lst"
                                @click="$router.push({name: 'Forms', params: {items: items, option: 'update', id: item.id}})">
                                <i class="fa-solid fa-pen-to-square"></i>
                            </button>
                            <button class="bck-red btn-lst">
                                <i class="fa-solid fa-trash-can"></i>
                            </button>
                        </div>
                    </td>
                </tr>
            </tbody>

            <br>

            <tfoot id="t-foot">
                <tr>
                    <td :colspan="cols" id="t-subfoot">
                        <div class="f-item">{{ data.firstItemOnPage }}-{{ data.lastItemOnPage }} of {{ data.totalItems }}</div>
                        <div class="f-item right">Page {{ query.page }} of {{ data.totalPages }}</div>
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
                                        @click="query.page=1;query.rows=n;$emit('changeData', query)">{{n}} rows
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
        <nav aria-label="Page navigation example" v-if="data.totalPages > 1">
                
            <div class="pagination">
                
                <a @click="query.page--;arrayLinks();$emit('changeData', query)"
                    :class="['page-item', {'disabled': !data.previous}]">
                        <i class="fas fa-chevron-left"></i>
                </a>

                <a @click="query.page=pageNumber;$emit('changeData', query)"
                    v-for="pageNumber in arrayLinks()"
                    :key="pageNumber"
                    :class="['page-item', {'selected': pageNumber===data.currentPage}]">
                        {{ pageNumber }}
                </a>

                <a @click="query.page++;arrayLinks();$emit('changeData', query)"
                    :class="['page-item', {'disabled': !data.next}]">
                        <i class="fas fa-chevron-right"></i>
                </a>
            </div>
        </nav>

    </div>
</template>

<script>
import { ref, reactive, toRefs, onMounted } from 'vue'


export default {
    name: 'ItemsTable',
    props: {
        items: String,
        query: Object,
        data: Object,
        headers: Object,
    },
    setup(props, { emit }) {

        const show = ref(false)
        const cols = Object.keys(props.headers).length + 1
        const numberOfLinks = 5

        const links = reactive({
            startLink: 1,
        })

        const arrayLinks = (() => {
            const n = Math.min(numberOfLinks, props.data.totalPages)
            if (props.query.page>links.startLink + n -1) {
                links.startLink++
            } else if (props.query.page<links.startLink) {
                links.startLink--
            }
            return Array.from({length: n}, (_, i) => links.startLink + i)
        })

        return { arrayLinks,
                 show,
                 cols,
                 ...toRefs(links) }
    }
}
</script>

<style scope>


/* Tables ------------------------------------------------------------ Tables */

#table {
    cursor:pointer;
    text-align: left;
    table-layout: fixed;
    max-width: 85%;
}

thead {
    color: whitesmoke;
    font-size: larger;
}

#t-head {
    opacity: 0.7;
    background-color: var(--color-nav);
}

.headers {
    height: 60px;
}

th>.fa-sort-down {
    opacity: 0.3;
}

th>.selected {
    opacity: 1;
}

th {
    padding: 10px 20px;
}

#table td {
    padding: 5px 20px;
    max-width: 600px;
}

#table tr:nth-child(even){
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

.changeRows>li {
    
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

.pagination a.selected {
    background-color: var(--color-btn);
    color: white;
}

.page-item {
    cursor: pointer;
}

</style>