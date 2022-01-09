<template>
    <div class="container">
        
    </div>
</template>

<script>
import usePaginationTable from '@/composables/usePaginationTable'
import useApi from '@/composables/useApi'

export default {
    name: 'ItemsTable',
    props: {
        items: String,
    },
    setup(props) {
        const items = props.items

        const { json_response, table } = useApi('get', props.items)

        const { rowsPage,
                dataPage,
                pages,
                actualPage,
                getDataPage,
                changePage,
                changeLinks,
                arrayLinks,
                numLinks,
                changeRows } = usePaginationTable(json_response)

        return { rowsPage,
                 dataPage,
                 pages,
                 actualPage,
                 getDataPage,
                 changePage,
                 changeLinks,
                 arrayLinks,
                 numLinks,
                 rowsPage,
                 changeRows,
                 json_response,
                 table,
                 items }
    }
}
</script>

<style scope>
/* Tables ------------------------------------------------------------ Tables */

table {
    text-align: left;
    cursor:pointer;
    max-width: 70%;
}

thead {
    background-color: var(--color-nav);
    opacity: 0.5;
    color: whitesmoke;
    font-size: larger;
}

th {
    padding: 10px 20px;
    min-width: 60px;
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