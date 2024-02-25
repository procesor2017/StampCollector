<template>
    <div>
      <UpperSection :stampData="stampData" />
      <LowerSection :stampTypes="stampTypes" />
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import UpperSection from '../components/UpperSection.vue';
  import LowerSection from '../components/LowerSection.vue';
  
  export default {
    data() {
      return {
        stampData: {},
        stampTypes: [],
      };
    },
    mounted() {
      const stampId = this.$route.params.stamp_id;
      this.fetchStampData(stampId);
      this.fetchStampTypes(stampId);
    },
    methods: {
      async fetchStampData(stampId) {
        try {
          const response = await axios.get(`/stamp/${stampId}/types/`);
          this.stampData = response.data[0];
        } catch (error) {
          console.error('Error fetching stamp data:', error);
        }
      },
      async fetchStampTypes(stampId) {
        try {
          const response = await axios.get(`/stamp/${stampId}/types/`);
          this.stampTypes = response.data;
        } catch (error) {
          console.error('Error fetching stamp types:', error);
        }
      },
    },
    components: {
      UpperSection,
      LowerSection,
    },
  };
  </script>
  
  <style scoped>
  /* Přidejte styly, pokud jsou potřeba */
  </style>
  