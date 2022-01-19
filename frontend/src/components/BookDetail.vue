<template>
    <div>
        Book Detail {{ id }}
        <br>
        {{ data }}
    </div>
</template>

<script>
export default {
    name: 'BookDetail',
    props: {
        id: String,
        data: Object,
    },
    setup(props) {

    }
}
</script>