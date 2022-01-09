<template>
  <div id="nav">
    <router-link class="home" :to="{name: 'Home'}"><i class="fa-solid fa-house-chimney"></i> Home</router-link> |
    <router-link :to="{name: 'Authors'}">Authors</router-link>
    <router-link :to="{name: 'Categories'}">Categories</router-link>
    <router-link :to="{name: 'Series'}">Series</router-link>
    <router-link :to="{name: 'Books'}">Books</router-link>
  </div>
  <router-view/>
</template>

<style>
:root {
    --color-btn:#d89417;
    --color-nav: rgb(45, 34, 83);
    --btn-radius: 5px;
    --font-fam: monospace;
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
}

/* Navbar ------------------------------------------------------------ Navbar */

#nav {
    background-color: var(--color-nav);
    overflow: hidden;
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
    background-color: rgb(212, 211, 211);
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
    padding: 3px;
    margin: 2px;
    cursor: pointer;
    border:none;
}

button:hover {
    opacity: 0.7;
    /*border: 2px solid gray;*/
}

.btn-del {
    background-color: red;
}

.btn-edit {
    background-color: green;
}

</style>
