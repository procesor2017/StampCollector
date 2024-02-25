<template>
  <div>
    <h1>Emissions with Stamps</h1>
    <a-collapse accordion>
      <a-collapse-panel
        v-for="emission in emissions"
        :key="emission.id"
        :header="emission.name"
      >
        <a-card class="custom-card" v-for="stamp in emission.stamps" :key="stamp.id">
          <div v-if="!stamp.photo_path_basic">
            <a-empty />
          </div>
          <div v-else>
            <CustomImage :src="stamp.photo_path_basic" />
          </div>
          <p>{{ stamp.name }}</p>
          <p>{{ stamp.catalog_number }}</p>
        </a-card>
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
  },
};
</script>

<style scoped>
.default-image-warning {
  color: red;
}

.custom-card {
  width: 300px; 
  height: 400px; 
}

</style>
