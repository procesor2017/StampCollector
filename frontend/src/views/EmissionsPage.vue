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
          <router-link
            v-for="stamp in emission.stamps"
            :key="stamp.id"
            :to="{ name: 'Stamp', params: { stamp_id: stamp.id } }"
          >
            <a-card class="custom-card">
              <div class="custom-image-container">
                <img :src="getAbsolutePath(stamp.photo_path_basic)" alt="Stamp Image" />
              </div>
              <div class="custom-card-info">
                <p class="stamp-name">{{ stamp.name }}</p>
                <p class="stamp-catalog-number">Cat. Number: {{ stamp.catalog_number }}</p>
              </div>
            </a-card>
          </router-link>
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
      return require('@/assets/' + relativePath);
    },
  },
};
</script>

<style scoped>
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
  width: 200px;
  margin: 16px;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-decoration: none;
  color: #333; /* Barva textu */
}

.custom-card:hover {
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.2); /* Efekt stínu při najetí myší */
}

.custom-image-container {
  width: 164px;
  height: 196px;
  overflow: hidden;
}

.custom-image-container img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.custom-card-info {
  text-align: center;
}

.stamp-name {
  font-weight: bold;
  margin: 8px 0;
}

.stamp-catalog-number {
  margin: 4px 0;
}
</style>
