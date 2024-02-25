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
    data() {
      return {
        columns: [
          {
            title: 'Name',
            dataIndex: 'name',
            key: 'name',
          },
          {
            title: 'Typee',
            dataIndex: 'type',
            key: 'type',
          },
          {
            title: 'Color',
            dataIndex: 'color',
            key: 'color',
          },
          {
            title: 'Perf',
            dataIndex: 'perforation',
            key: 'perforation',
          },
          {
            title: 'Desk bug',
            dataIndex: 'plate_flaw',
            key: 'plate_flaw',
          },
          {
            title: 'Catalog price',
            dataIndex: 'catalog_price',
            key: 'catalog_price',
          },
        ],
      };
    },
  };
  </script>
  
  <style scoped>
  /* Přidejte styly, pokud jsou potřeba */
  </style>
  