<template>
  <div class="leftMenu">
    <router-link to="/">Home</router-link>
    <router-link to="/emissions">Emissions</router-link>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'LeftMenu',
});
</script>

<style scoped>
/* Styl pro komponent LeftMenu.vue */
.leftMenu {
  width: 200px;
  background-color: #f0f0f0;
  padding: 10px;
  height: 100vh;
}

.leftMenu a {
  display: block;
  margin-bottom: 10px;
  text-decoration: none;
  color: #333;
  font-weight: bold;
}
</style>
