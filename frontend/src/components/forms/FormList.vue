<template>
    <transition name="modal">
        <div class="modal-mask">
            <div class="modal-wrapper">
                <div class="modal-container">

                    <header class="modal-header">
                        <slot name="header">
                            <h3>Select any {{ itemsSingularName[fieldName] }} to add</h3>                
                        </slot>
                    </header>

                    <section class="modal-body">
                        
                        <input type="text"
                            placeholder="Filter"
                            id="formFinder"
                            v-model="query"
                            @keyup="page=1;search()"/>

                        <div id="filterForm">
                            <div :class="['t-prev', 'changePage', {'disabled': page===1}]"
                                @click="page--;search()">
                                <i class="fas fa-chevron-left"></i>
                            </div>   
                            <ul class="list-group">
                                <li v-for="el of data.results" :key="el.id"
                                    class="list-group-item"
                                    @click="$emit('addValue', {val: el, field: fieldName})">
                                    {{ el.name }}
                                </li>
                            </ul>
                            <div :class="['t-next', 'changePage', {'disabled': page===data.totalPages}]"
                                @click="page++;search()">
                                <i class="fas fa-chevron-right"></i>
                            </div>
                        </div> 
                    </section>



                    <footer class="modal-footer">
                        <slot name="footer">
                            <button type="button" class="" @click="$emit('close')">Cancel</button >
                            <button type="button" class="bck-green" >Add</button >
                        </slot>
                    </footer>

                </div>
            </div>
        </div>
    </transition>
</template>


<script>
import useApi from '@/composables/useApi'
import useItemsInfo from '@/composables/useItemsInfo'
import { reactive, toRefs, ref } from 'vue'

export default {
    name: 'FormList',
    props: {
        modalList: Object,
        fieldName: String,
        excludeQuery: String,
    },
    setup(props){
        const data = ref(props.modalList)
        const params = reactive({
            page: 1,
            query: '',
        })

        const { itemsSingularName } = useItemsInfo()

        const search = (async() => {
            const path = `${props.fieldName}/?&q=${params.query}&rows=5&page=${params.page}${props.excludeQuery}`
            data.value = (await useApi('GET', path)).jsonResponse.value
        })

        return { ...toRefs(params), search, data, itemsSingularName }
    }
}
</script>

<style scoped>
.modal-mask {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: table;
  transition: opacity 0.3s ease;
  z-index: 1;
}

.modal-wrapper {
  display: table-cell;
  vertical-align: top;
  padding: 100px;
}

.modal-container {
    width: 50%;
    margin: 0px auto;
    padding: 10px 20px;
    background-color: #fff;
    border-radius: 5px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.8);
    transition: all 0.3s ease;
}

.modal-header {
    border-radius: var(--btn-radius);
    background-color: var(--color-nav);
    color: whitesmoke;
    padding: 2px;
    font-size: large;
}

.modal-body {
    margin: 20px 0;
    font-size: large;
}

.modal-footer {
    display: flex;
    justify-content: flex-end;
}

.modal-enter {
    opacity: 0;
}

.modal-leave-active {
    opacity: 0;
}

.modal-enter .modal-container,
.modal-leave-active .modal-container {
    -webkit-transform: scale(1.1);
    transform: scale(1.1);
}

.list-group {
    list-style-type: none;
    -webkit-padding-start: 0;
    text-align: left;
    background-color: var(--color-hover);
    width: 100%;
    margin: 0px;
    cursor: pointer;
}

.list-group-item {
    padding: 5px 40px;
    margin: 10px;
}

#formFinder {
    padding: 5px 10px;
    width: 90%;
    font-size: large;
    margin-bottom: 20px;
    border: 3px solid var(--color-nav);
    border-radius: var(--btn-radius)
}

#formFinder:focus {
    outline-color: var(--color-btn);
}

#filterForm {
    width: 100%;
    display: flex;
}

.changePage {
    background-color: var(--color-nav);
    width: 10%;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: larger;
    color: whitesmoke;
}

.disabled {
    background-color: var(--color-hover);
    color: var(--color-hover);
    opacity: 1;
}

.t-prev {
    border-radius: 5px 0px 0px 5px;
    vertical-align: middle
}

.t-next {
    border-radius: 0px 5px 5px 0px;
}

button {
    padding: 7px 15px;
    font-size: medium;
    font-weight: bold;
}

</style>