<template>
    <transition name="matches">
        <div class="drpdwn" v-if="data[0]">
            <div class="col-drp">
                <p>{{ item }}</p>
            </div>
            <div class="col-drp">
                <ul class="list">
                    <li v-for="(x) of data" :key="x.id">{{ x.field }}</li>
                </ul>
            </div>
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

<style scoped>
    
.drpdwn {
    flex-direction: row;
    margin: 15px;
    width: 20%;
    padding: 0;
    list-style-type: none;
    transform-origin: top;
    transition: transform 0.5s ease-in-out;
}

.col-drp {
    width: 300px;
}

.col-drp>p {

    background-color: var(--color-nav);
    color:whitesmoke;
    padding: 10px;
    font-size: larger;
    font-weight: bold;

}

.col-drp>ul {
    background-color: var(--color-hover);
    list-style-type: none;
    margin: 0;
    padding: 0;
}

.list>li {
    padding: 15px 10px;
    font-size: large;
}

.list>li:hover {
    background-color: rgb(201, 195, 195);
    cursor: pointer;
}

.matches-leave-to {
    transform: scaleY(0);
}

</style>