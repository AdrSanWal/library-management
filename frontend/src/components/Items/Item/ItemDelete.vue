<template>
    <transition name="modal">
        <div class="modal-mask">
            <div class="modal-wrapper">
                <div class="modal-container">

                    <header class="modal-header">
                        <slot name="header">
                            <h3>Are you sure you want to delete this instances?</h3>                        
                        </slot>
                    </header>

                    <section class="modal-body">
                        <slot name="header">
                            <h3>The next {{ itemsSingularName[items] }} will be deleted</h3>                        
                        </slot>
                        
                        <slot name="body">
                            <ul class="list-group">
                                 <li class="list-group-item list-group-item-dark"
                                    v-if="items==='books'">
                                        {{ item.isbn }} - {{ item.title }}</li>
                                <li class="list-group-item list-group-item-dark"
                                    v-if="items!=='books'">
                                        {{ item.name }}</li>       
                            </ul>
                        </slot>
                    </section>

                    <section class="modal-body" v-if="books.length!==0">
                        <slot name="header">
                            <h3>The next books will be deleted</h3>
    
                        </slot>
                        <slot name="body">
                            <ul class="list-group">
                                 <li class="list-group-item"
                                    v-for="book of books" :key="book">
                                        {{ book.isbn }} - {{ book.title }}</li>  
                            </ul>
                        </slot>
                    </section>

                    <footer class="modal-footer">
                        <slot name="footer">
                            <button type="button" class="" @click="$emit('close')">Cancel</button >
                            <button type="button" class="bck-red" @click="confirmDelete()">Delete</button >
                        </slot>
                    </footer>

                </div>
            </div>
        </div>
    </transition>
</template>

<script>
import useApi from '@/composables/useApi'
import useIetmsInfo from '@/composables/useItemsInfo'

export default {
    name: 'ItemDelete',
    props: {
        items: String,
        item: Object,
        books: Object
    },
    setup(props, { emit }){

        const { itemsSingularName } = useIetmsInfo()

        const confirmDelete = (async () => {
            const path = `${props.items}/${props.item.id}/`
            await useApi('DELETE', path)
            await emit('refresh')
            emit('close')
        })

        return { confirmDelete, itemsSingularName }
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
    text-align: left;
    background-color: var(--color-hover);
    border-radius: var(--btn-radius);
}

.list-group-item {
    padding: 5px;
    font-size: large;
}

button {
    padding: 7px 15px;
    font-size: medium;
    font-weight: bold;
}

</style>
