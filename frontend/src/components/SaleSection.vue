<template>
    <div>
      <h2>Sale Information</h2>
      <a-table :columns="columns" :dataSource="saleData" />
    </div>
  </template>
  
  <script>
  export default {
    props: {
      saleData: Array, // Asi pole?
    },
    data() {
      return {
        columns: [
          {
            title: 'Sale Date',
            dataIndex: 'sale_date',
            key: 'sale_date',
          },
          {
            title: 'Auction Name',
            dataIndex: 'name_of_auction',
            key: 'name_of_auction',
          },
          {
            title: 'Price',
            dataIndex: 'price',
            key: 'price',
          },
          {
            title: 'Auction URL',
            dataIndex: 'url_on_auction',
            key: 'url_on_auction',
            scopedSlots: { customRender: 'url' },
          },
        ],
      };
    },
  };
  </script>
  
  <style scoped>
  /* Přidejte styly, pokud jsou potřeba */
  </style>
  