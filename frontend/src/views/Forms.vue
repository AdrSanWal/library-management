<template>
    <div class="container">

        <FormList v-if="isFormListVisible" 
        @close="isFormListVisible = false"
        :modalList="modalList"
        :fieldName="fieldName"
        :excludeQuery="excludeQuery"
        @addValue="addValue"/>

        <div class="form">
            <p id="form-title">{{capitalize($route.params.option)}} {{ itemsSingularName[items] }}</p>

            <div v-for="(values, field) of item"
                class="form-field"
                :key="field">

                <label :for="`f-${field}`"
                    class="form-label"
                    v-if="values.type!=='notShow'">
                        {{ capitalize(field) }}
                </label>

                <input :id="`f-${field}`"
                    class="form-input"
                    :type="values.type"
                    v-model="item[field].value"
                    v-if="['text', 'url', 'number', 'date'].includes(values.type)"/>

                <textarea :id="`f-${field}`"
                    class="form-input"
                    rows="10"
                    v-model="item[field].value"
                    v-if="values.type==='textArea'"/>

                <div v-if="values.type==='select'"
                    class="form-select">
                    <input :id="`f-${field}`"
                        class="form-input select"
                        type="text"
                        v-model="item.serie.value['name']"
                        disabled/>
                    <button :class="['form-button', 'bck-red', {'disabled': !item[field].value}]"
                        @click="removeSelected(field)">
                        <i class="fas fa-minus"></i>
                    </button>
                    <button class="form-button bck-green"
                        @click="addNewValue(field)">
                        <i :class="['fas', {'fa-exchange-alt': item[field].value, 'fa-plus': !item[field].value}]" ></i>
                    </button>
                </div>

                <div v-if="values.type==='multiSelect'"
                    class="form-select">
                    <select :id="`f-${field}`"
                        class="form-input select"
                        multiple
                        size="5">
                        <option v-for="val of item[field].value"
                            :key="val.id"
                            :value="val.id"
                            class='opt-sel'
                            :id="`opt-${field}-${val.id}`">
                                {{ val.name }}
                        </option>
                    </select>
                    <button :class="['form-button', 'bck-red', {'disabled': item[field].value.length===0}]"
                        @click="removeSelected(field, item[field].value)">
                        <i class="fas fa-minus"></i>
                    </button>
                    <button class="form-button bck-green"
                        @click="addNewValue(field)">
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
import FormList from '@/components/forms/FormList'
import useApi from '@/composables/useApi'
import { capitalize } from '@/composables/useHelpFunctions'
import { useRoute, useRouter } from 'vue-router'
import { onMounted, ref, reactive } from 'vue'


export default {
    name: 'Form',
    components: {
        FormList
    },
    setup() {
        const route = useRoute()
        const router = useRouter()
        const items = route.params.items
        const id = route.params.id

        const { itemsFormFields, itemsSingularName } = useItemsInfo()

        const item = reactive(itemsFormFields[items])
        const errors = ref({})

        const isFormListVisible = ref(false)

        const relatedFields = reactive({
            authors: [],
            categories: []
        })

        const getData = (async () => {
            const path = `${items}/${id}/`
            const response = (await useApi('GET', path)).jsonResponse.value
            if (!response.serie) {response.serie=''}
            return response
        })
       
        onMounted(async () => {
            if (id!=='new') {
                const res = await getData()

                for (let field in res) {
                    if (field in item) {
                        item[field]['value'] = await res[field]
                    }
                }
            }

        })

        const updateInfo = (async () => {

            let response
            let newItem = new Object()
            Object.keys(item).map(key => {
                newItem[key] = item[key].value              
            })
           
            if (id==='new'){
                const path = `${items}/`
                response = await useApi('POST', path, {body: JSON.stringify(newItem)})
            } else {
                const path = `${items}/${id}/`
                response = await useApi('PUT', path, {body: JSON.stringify(newItem)})
            }
            const status = response.response.value.status
            if ( status === 400) {
                // If status = 400 assign the error message
                errors.value = await response.jsonResponse.value 

            } else if (status === 200 || status === 201) {
                router.go(-1);
            } 
        })

        const removeSelected = ((field) => {
            const selected = document.querySelectorAll(`#f-${field} :checked`)
            relatedFields[field] = [...selected].map(e => parseInt(e.value))
            if (field==='serie') {
                item.serie.value = ''
                item.serie_order.value = ''
            } else {
                item[field].value = item[field].value.filter(
                    e => !relatedFields[field].includes(e.id)
                )
            }
        })

        const fieldName = ref('')
        const modalList = ref({})
        const page = ref(1)
        const excludeQuery = ref('')

        const addNewValue = (async (field) => {
            if (field==='serie') {
                fieldName.value = 'series'
                const excludeId = item[field].value.id
                excludeQuery.value = excludeId ? `&not=${excludeId}` : ''

            } else {
                fieldName.value = field
                const excludeIds = item[field].value.map(e => e.id)
                excludeQuery.value = excludeIds.length===0 ? '' : `&not=${excludeIds}`
            }

            const path = `${fieldName.value}/?&rows=5&page=${page.value}${excludeQuery.value}`
            console.log(path)
            modalList.value = (await useApi('GET', path)).jsonResponse.value
            isFormListVisible.value=true
        })

        const addValue = ((d) => {
            if (d['field']==='series') {
                item.serie.value = d['val']
                item.serie_order.value = ''
            } else {
                item[d['field']].value.push(d['val'])
            }
            isFormListVisible.value=false
        })

    return { item,
             items,
             itemsFormFields,
             capitalize,
             itemsSingularName,
             removeSelected,
             errors,
             isFormListVisible,
             addNewValue,
             modalList,
             fieldName,
             excludeQuery,
             addValue,
             updateInfo }
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