<template>
  <div>
    <h1>Emissions with Stamps</h1>
    <a-collapse accordion>
      <a-collapse-panel
        v-for="emission in emissions"
        :key="emission.id"
        :header="emission.name"
        class="custom-collapse-panel"
      >
        <div class="custom-card-container">
          <a-card
            class="custom-card"
            v-for="stamp in emission.stamps"
            :key="stamp.id"
          >
            <router-link :to="{ name: 'Stamp', params: { stamp_id: stamp.id } }">
              <div v-if="!stamp.photo_path_basic">
                <a-empty />
              </div>
              <div v-else>
                <img :src=getAbsolutePath(stamp.photo_path_basic) />
              </div>
              <p>{{ stamp.name }}</p>
              <p>{{ stamp.catalog_number }}</p>
            </router-link>
          </a-card>
        </div>
      </a-collapse-panel>
    </a-collapse>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      emissions: [],
      image: require('@/assets/images/austria/1850-1918/1Kr1850.png')
    };
  },
  mounted() {
    this.fetchEmissionsWithStamps();
  },
  methods: {
    async fetchEmissionsWithStamps() {
      try {
        const response = await axios.get('/emissions-with-stamps/');
        this.emissions = response.data;
      } catch (error) {
        console.error('Error fetching emissions with stamps:', error);
      }
    },
    getAbsolutePath(relativePath) {
      return require(`../assets/${relativePath}`)
    },
  },
};
</script>

<style scoped>
.default-image-warning {
  color: red;
}

.custom-collapse-panel {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.custom-card-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
}

.custom-card {
  width: 300px;
  height: 400px;
  margin: 0 16px 16px 0; /* Okraj mezi kartami, můžete upravit podle potřeby */
}
</style>
