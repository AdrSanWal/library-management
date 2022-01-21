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
                            {{ key }} <i :class="['fas', 'fa-sort-down', {'active': value===query.sortField}]"></i>
                    </th>
                    <th class="h-right">
                        Add <i class="fas fa-external-link-alt"></i>
                    </th>  
                </tr>
            </thead>

            <tbody>
                <tr v-for="(item, index) of data.results"
                    :key="index"
                    @click="$router.push({name: 'Items', params: {id: item.id}})">
                    <td>1</td>
                    <td v-for="(value, key, index) of headers"
                        :key="index">
                        <span>{{ item[value] }}</span>
                    </td>
                    <td class="exclude" @click.stop>
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
                        <div class="f-item">{{ data.count }}  Results</div>
                        <div class="f-item right">Page TODO of TODO</div>
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
                                        @click="query.rows=n;$emit('changeData', query)">{{n}} rows
                                    </li>
                                </ul>
                            </transition>
                        </div>
                    </td>
                </tr>
            </tfoot>

        </table>

    </div>
</template>

<script>
import { ref } from 'vue'


export default {
    name: 'ItemsTable',
    props: {
        items: String,
        query: Object,
        data: Object,
        headers: Object,
    },
    setup(props) {

        const show = ref(false)
        const cols = Object.keys(props.headers).length + 1

        return { show,
                 cols }
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

th>.active {
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

.pagination a.active {
    background-color: var(--color-btn);
    color: white;
}

.page-item {
    cursor: pointer;
}

</style>