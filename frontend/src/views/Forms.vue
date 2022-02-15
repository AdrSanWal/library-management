<template>
    <div class="container">
    <br>
    <strong>Item:</strong> <p>{{ item }}</p>
    <strong>Serie:</strong> <p>{{ item.serie }}</p>
    <strong>Authors:</strong> <p>{{ item.authors }}</p>
    <strong>Categories:</strong> <p>{{ item.categories }}</p>

        <div class="form">
            <p id="form-title">{{capitalize($route.params.option)}} {{ itemsSingularName[items] }}</p>

            <div v-for="(type, field) of itemsFormFields[items]"
                class="form-field"
                :key="field">

                <label :for="`f-${field}`"
                    class="form-label">
                        {{ capitalize(field) }}
                </label>

                <input :id="`f-${field}`"
                    class="form-input"
                    :type="type"
                    v-model="item[field]"
                    v-if="['text', 'url', 'number', 'date'].includes(type)"/>

                <textarea :id="`f-${field}`"
                    class="form-input"
                    rows="10"
                    v-model="item[field]"
                    v-if="type==='textArea'"/>

                <div v-if="type==='select'"
                    class="form-select">
                    <input :id="`f-${field}`"
                        class="form-input select"
                        type="text"
                        :value="itemsRelated[field]"
                        disabled/>
                    <button :class="['form-button', 'bck-red', {'disabled': !itemsRelated.serie}]"
                        @click="removeSelected(field, itemsRelated.serie)">
                        <i class="fas fa-minus"></i>
                    </button>
                    <button class="form-button bck-green">
                        <i :class="['fas', {'fa-exchange-alt': itemsRelated.serie, 'fa-plus': !itemsRelated.serie}]" ></i>
                    </button>
                </div>

                <div v-if="type==='multiSelect'"
                    class="form-select">
                    <select :id="`f-${field}`"
                        class="form-input select"
                        multiple
                        size="5">
                        <option v-for="val of item[field]"
                            :key="val.id"
                            :value="val.id"
                            @click="multiSelectClick(field, val)"
                            class='opt-sel'
                            :id="`opt-${field}-${val.id}`">
                                {{ val.name }}
                        </option>
                    </select>
                    <button :class="['form-button', 'bck-red', {'disabled': itemsRelated[field].length===0}]"
                        @click="removeSelected(field, itemsRelated[field])">
                        <i class="fas fa-minus"></i>
                    </button>
                    <button class="form-button bck-green">
                        <i class="fas fa-plus"></i>
                    </button>
                </div>

                <ul v-if="errors[field]">
                    <li v-for="(error, i) of errors[field]"
                        :key="i"
                        class="err">{{ error }}</li>
                </ul> 
            </div>
            <br>
            <div class="right">
                <button class="bck-green" @click="updateInfo()">{{ capitalize($route.params.option) }}</button>
                <button @click="$router.push({name: 'Items', params: {items:items, id: 'list'}})">Cancel</button>
            </div>
        </div>
    </div>
</template>

<script>
import useItemsInfo from '@/composables/useItemsInfo'
import useApi from '@/composables/useApi'
import { capitalize } from '@/composables/useHelpFunctions'
import { useRoute, useRouter } from 'vue-router'
import { onMounted, ref, reactive } from 'vue'


export default {
    name: 'Form',
    setup() {
        const route = useRoute()
        const router = useRouter()
        const items = route.params.items
        const id = route.params.id

        const { itemsFormFields, itemsSingularName } = useItemsInfo()

        const item = ref({})
        const errors = ref({})

        const itemsRelated = reactive({
            serie: null,
            authors: [],
            categories: []
        })
       
        onMounted(async () => {
            if (id!=='new') {
                const path = `${items}/${id}/`
                item.value = (await useApi('GET', path)).jsonResponse.value
                console.log('item', item.value['serie'].name)
                if (items==='books' && item.value['serie']) {
                    itemsRelated.serie = item.value['serie'].name
                }
            }
        })

        const updateInfo = (async () => {

            let response
            
            if (id==='new'){
                const path = `${items}/`
                response = await useApi('POST', path, {body: JSON.stringify(item.value)})
            } else {
                const path = `${items}/${id}/`
                
                response = await useApi('PUT', path, {body: JSON.stringify(item.value)})

            }

            const status = response.response.value.status
            if ( status === 400) {
                // If status = 400 assign the error message
                errors.value = await response.jsonResponse.value 

            } else if (status === 200 || status === 201) {
                router.go(-1);
            } 

        })

        const multiSelectClick = ((field, val) => {
            if (!itemsRelated[field].includes(val.id)) { 
                itemsRelated[field].push(val.id);
            } else {
                itemsRelated[field].splice(itemsRelated[field].indexOf(val.id), 1);
            }
        })

        const removeSelected = ((field, ids) => {
            //itemsRelated[field] are the name(serie) or the ids(authors, categories) of the options selected when click -
            if (field==='serie') {
                itemsRelated.serie = null
                item.value['serie'] = null
                item.value['serie_order'] = null
            } else {
                ids.forEach(id => {
                        item.value[field] = item.value[field].filter((item) => item.id !== id);
                    }
                )
            }
        })

    return { itemsRelated,
             item,
             items,
             itemsFormFields,
             capitalize,
             itemsSingularName,
             updateInfo,
             errors,
             multiSelectClick,
             removeSelected }
    }
}
</script>

<style scoped>

/* Form ---------------------------------------------------------------- Form */

.form {
    display: flex;
    flex-direction: column;
    margin-top: var(--margin-top);
    border-radius: 10px;
    border: 3px solid var(--color-nav);
    padding: 15px;
    background-color: var(--color-light);
    width: 60%;

}

#form-title {
    color: var(--color-nav);
    font-size: larger;
    font-weight: bold;
    margin: 0px;
    padding: 5px;
}

.form-field {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
}

.form-label {
    margin-top: 5px;
    padding: 5px;
    color: var(--color-nav);
    font-size: large;
    font-weight: bold;

}

.form-input {
    border: 1px solid var(--color-nav);
    padding: 3px 0px 3px 10px;
    width: calc(100% - 13px);
    border-radius: var(--btn-radius);
    background-color: whitesmoke;
    font-size: large;
}

.form-input:focus {
    outline-color: var(--color-btn);
}


/* Specific Inputs ------------------------------------------ Specific Inputs */

textarea {
    resize: vertical;
}

.select {
    width: 90%;
}

.form-select {
    width: calc(100% - 3px);
    display: flex;
    justify-content: space-between;
    gap: 10px;
}

.form-button {
    width: 50px;
    height: 100%;
    margin: 0px;
    padding: 5px;
    font-size: larger;
    color: whitesmoke;
}


.opt-sel:checked {
    background-color: var(--color-nav);
    color: white;
    opacity: 0.6;
}


/* Buttons ---------------------------------------------------------- Buttons */

.right {
    display: flex;
    flex-direction: row-reverse;
}

.right button {
    font-size: large;
    font-weight: bold;
    padding: 7px 15px;
}


/* Errors ------------------------------------------------------------ Errors */

.err {
    color: red;
}

</style>