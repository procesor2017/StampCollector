<template>
  <div id="app">
    <left-menu />
    <div class="content">
      <router-view />
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import LeftMenu from '@/components/LeftMenu.vue'; // Zkontrolujte cestu k vašemu LeftMenu komponentu

export default defineComponent({
  name: 'App',
  components: {
    LeftMenu,
  },
});
</script>

<style>
#app {
  display: flex;
}

.content {
  flex-grow: 1;
  padding: 20px;
}
</style>
