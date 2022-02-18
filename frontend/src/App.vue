<template>
  <div id="nav">
    <router-link class="home" :to="{name: 'Home'}"><i class="fa-solid fa-house-chimney"></i> Home</router-link> |
    <router-link :to="{name: 'Items', params: {items: 'authors', id: 'list'}}">Authors</router-link>
    <router-link :to="{name: 'Items', params: {items: 'categories', id: 'list'}}">Categories</router-link>
    <router-link :to="{name: 'Items', params: {items: 'series', id: 'list'}}">Series</router-link>
    <router-link :to="{name: 'Items', params: {items: 'books', id: 'list'}}">Books</router-link>
  </div>
  <LoaderPage v-if="isLoading"/>
  <router-view :key="$route.fullPath"/>
</template>

<script>
import LoaderPage from './components/LoaderPage.vue'
import { ref, provide } from 'vue'

export default{
    components: { 
        LoaderPage
    },
    setup() {
        const isLoading = ref(false)
        provide('isLoading', isLoading)

        return { isLoading }
    }
}
</script>


<style>
:root {
    --color-btn:#d89417;
    --color-nav: rgb(45, 34, 83);
    --btn-radius: 5px;
    --font-fam: monospace;
    --color-hover: rgb(221, 221, 221);
    --width-fnd: 500px;
    --margin-top: 50px;
    --color-light: rgb(235, 235, 235);
}

body {
    margin: 0px;
}

#app {
    font-family: var(--font-fam);
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
}

.container {
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
}

.disabled {
    opacity: 0.4;
    cursor: default !important;
    pointer-events: none;
}

/* Navbar ------------------------------------------------------------ Navbar */

#nav {
    position: sticky;
    top: 0px;
    z-index: 1;
    background-color: var(--color-nav);
    overflow: hidden;
    box-shadow: 0px 0px 10px 0px rgba(0, 0, 0, 0.9);
}

#nav a {
    float: left;
    color: whitesmoke;
    text-align: center;
    padding: 15px;
    font-size: 16px;
    text-decoration: none;
}

#nav a:hover {
    background-color: var(--color-hover);
    color: black;
}

#nav a.home {
    background-color: var(--color-btn);
    color: white;
}


#nav a.router-link-exact-active, a.exact-active {
  font-weight:bolder
}

/* Buttons ---------------------------------------------------------- Buttons */

button {
    border-radius: var(--btn-radius);
    background-color: var(--color-btn);
    color: whitesmoke;
    margin: 2px;
    cursor: pointer;
    border:none;
    padding: 5px;
    text-align: center;
}

button:hover {
    opacity: 0.7;
    /*border: 2px solid gray;*/
}

.bck-red {
    background-color: red;
}

.bck-green {
    background-color: green;
}

</style>
