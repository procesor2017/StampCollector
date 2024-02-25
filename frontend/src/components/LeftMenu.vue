<template>
  <div class="leftMenu">
    <a-menu :theme="menuTheme" :mode="menuMode" :default-selected-keys="[selectedMenuKey]">
      <a-menu-item key="home">
        <router-link to="/">Home</router-link>
      </a-menu-item>
      <a-menu-item key="emissions">
        <router-link to="/emissions">Emissions</router-link>
      </a-menu-item>
    </a-menu>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { Menu } from 'ant-design-vue';
import { useRouter } from 'vue-router';

export default defineComponent({
  name: 'LeftMenu',
  components: {
    'a-menu': Menu,
    'a-menu-item': Menu.Item,
  },
  setup() {
    const router = useRouter();
    const selectedMenuKey = router.currentRoute.value.name || 'home';

    return {
      selectedMenuKey,
      menuTheme: 'dark',
      menuMode: 'vertical',
    };
  },
});
</script>

<style scoped>
.leftMenu {
  width: 200px;
  background-color: #333; 
  color: white;
  height: 100vh;
}

.leftMenu a {
  text-decoration: none;
}
</style>
