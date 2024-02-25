<template>
    <a-card>
      <a-table :dataSource="stampTypes" :columns="columns" />
    </a-card>
  </template>
  
  <script>
  export default {
    props: {
      stampTypes: Array,
    },
    computed: {
      columns() {
        if (this.stampTypes.length === 0) {
          return [];
        }
  
        return Object.keys(this.stampTypes[0]).map((key) => ({
          title: key,
          dataIndex: key,
          key,
        }));
      },
    },
  };
  </script>
  
  <style scoped>
  /* Přidejte styly, pokud jsou potřeba */
  </style>
  