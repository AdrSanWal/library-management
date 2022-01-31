<template>
    <div class="container">
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
                        class="form-input"
                        :type="type"
                        v-model="item[field]"
                        disabled/>
                    <button class="form-button">
                        <i class="fas fa-exchange-alt"></i>
                    </button>
                    <button class="form-button bck-red">
                        <i class="fas fa-minus"></i>
                    </button>
                    <button class="form-button bck-green">
                        <i class="fas fa-plus"></i>
                    </button>
                </div>

                <div v-if="type==='multiSelect'"
                    class="form-select">
                    <select :id="`f-${field}`"
                        class="form-input select"
                        multiple
                        size="5">
                        <option v-for="(val, i) of item[field]"
                            :key="val" :value="val"
                            @click="prueba(i)"
                            class='opt-sel'
                            :id="`opt-${i}`">
                                {{ val }}
                        </option>
                    </select>
                    <button class="form-button del">
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
                <button @click="$router.go(-1)">Cancel</button>
            </div>
        </div>
    </div>
</template>

<script>
import useItemsInfo from '@/composables/useItemsInfo'
import useApi from '@/composables/useApi'
import { capitalize, compareObjects } from '@/composables/useHelpFunctions'
import { useRoute, useRouter } from 'vue-router'
import { onMounted, ref } from 'vue'


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
        const originalItem = ref({})
       
        onMounted(async () => {
            if (id!=='new') {
                const path = `${items}/${id}/`
                item.value = (await useApi('GET', path)).jsonResponse.value
                originalItem.value = JSON.parse(JSON.stringify(item.value))
            }
        })

        const updateInfo = (async () => {
            // checks if there are changes and if there are, returns only those fields

            let response
            
            if (id==='new'){
                const path = `${items}/`
                response = await useApi('POST', path, {body: JSON.stringify(item.value)})
            } else {
                // const updates = compareObjects(items, originalItem.value, item.value)
                const path = `${items}/${id}/`
                
                response = await useApi('PUT', path, {body: JSON.stringify(item.value)})

            }

            if (response.response.value.status === 400) {
                // If status = 400 assign the error message
                errors.value = await response.jsonResponse.value 

            } else if (response.response.value.status === 200) {
                router.go(-1);
            } 

        })

        const prueba = ((sel) => {
            document.getElementById(`opt-${sel}`).selectedIndex = "2"
            console.log(sel)
        })

    return { originalItem,
             item,
             items,
             itemsFormFields,
             capitalize,
             itemsSingularName,
             updateInfo,
             errors,
             prueba }
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
    width: 95%;
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

.del {
    background-color: red;
}


/* Errors ------------------------------------------------------------ Errors */

.err {
    color: red;
}

</style>