<template>
  <div>
    <h1>Emissions with Stamps</h1>
    <a-collapse accordion>
      <a-collapse-panel
        v-for="emission in emissions"
        :key="emission.id"
        :header="emission.name"
      >
        <a-card v-for="stamp in emission.stamps" :key="stamp.id">
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
/* Styly pro EmissionPage zde */
</style>
