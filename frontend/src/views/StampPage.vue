<!-- StampPage.vue -->
<template>
  <div>
    <UpperSection :stampData="stampData" />
    <LowerSection :stampTypes="stampTypes" />
    <SaleSection :saleData="saleData" />
  </div>
</template>

<script>
import axios from 'axios';
import UpperSection from '../components/UpperSection.vue';
import LowerSection from '../components/LowerSection.vue';
import SaleSection from '../components/SaleSection.vue';

export default {
  data() {
    return {
      stampData: {},
      stampTypes: [],
      saleData: [],
    };
  },
  mounted() {
    const stampId = this.$route.params.stamp_id;
    this.fetchStampData(stampId);
    this.fetchStampTypes(stampId);
    this.fetchSaleData(stampId);
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
    async fetchSaleData(stampId) {
      try {
        const response = await axios.get(`/stamp/${stampId}/types/sale`);
        this.saleData = response.data;
      } catch (error) {
        console.error('Error fetching sale data:', error);
      }
    },
  },
  components: {
    UpperSection,
    LowerSection,
    SaleSection,
  },
};
</script>

<style scoped>
/* Přidejte styly, pokud jsou potřeba */
</style>
