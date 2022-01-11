<template>
    <transition name="matches">
        <div class="col">
            <p>{{ item }}</p>
            <ul class="list">
                <li v-for="(x) of data" :key="x.id">{{ x.field }}</li>
            </ul>
        </div>
    </transition>
</template>

<script>

export default {
    name: 'DropdownSearch',
    props: {
        item: String,
        data: Object,
    },
    setup(props) {
        const item = props.item

        return { item }
    }
}
</script>

<style>
    
.col {
    flex-direction: row;
    margin: 100px;
}

.col {
    width: 108px;
    padding: 0;
    list-style-type: none;
    transform-origin: top;
    transition: transform 0.5s ease-in-out;

}

</style>