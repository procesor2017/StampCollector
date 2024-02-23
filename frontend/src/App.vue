<template>
  <div id="app">
    <div class="leftMenu">
      <router-link to="/">Home</router-link>
      <router-link to="/emissions">Emissions</router-link>
    </div>
    <div class="content">
      <router-view />
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'App',
});
</script>

<style>
body {
  margin: 0;
  font-family: Avenir, Helvetica, Arial, sans-serif;
  display: flex;
}

.leftMenu {
  width: 200px;
  background-color: #333;
  color: white;
  padding: 20px;
  box-sizing: border-box;
}

.leftMenu a {
  display: block;
  margin-bottom: 10px;
  color: white;
  text-decoration: none;
}

.leftMenu a:hover {
  text-decoration: underline;
}

.content {
  flex-grow: 1;
  padding: 20px;
}
</style>
