<template>
    <div>
        Book Detail {{ id }}
        <br>
        {{ data }}
    </div>
</template>

<script>
export default {
    name: 'ItemsDetail',
    props: {
        id: String,
        data: Object,
    },
    setup(props) {
        //console.log(props)
        return { }
    }
}
</script>