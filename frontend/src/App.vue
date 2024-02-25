<template>
  <div id="app">
    <left-menu />
    <a-layout class="content">
      <a-layout-content style="padding: 20px; box-sizing: border-box;">
        <router-view />
      </a-layout-content>
    </a-layout>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import LeftMenu from '@/components/LeftMenu.vue';
import { Layout } from 'ant-design-vue';

export default defineComponent({
  name: 'App',
  components: {
    LeftMenu,
    'a-layout': Layout,
    'a-layout-content': Layout.Content,
  },
});
</script>

<style scoped>
#app {
  display: flex;
}

.content {
  flex-grow: 1;
}
</style>
