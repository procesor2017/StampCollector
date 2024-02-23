<template>
  <div>
    <h1>Emission Page</h1>
    <ul>
      <li v-for="emission in emissions" :key="emission.id">{{ emission.name }}</li>
    </ul>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { EmissionResponse } from '../..//types/types';
import axios from 'axios';

export default defineComponent({
  name: 'EmissionPage',
  data() {
    return {
      emissions: [] as EmissionResponse[],
    };
  },
  mounted() {
    this.fetchEmissions();
  },
  methods: {
    async fetchEmissions() {
      try {
        const response = await axios.get('/emissions');
        this.emissions = response.data;
      } catch (error) {
        console.error('Error fetching emissions:', error);
      }
    },
  },
});
</script>

<style scoped>
/* Styly pro EmissionPage zde */
</style>
