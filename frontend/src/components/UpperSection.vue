<template>
    <div class="upper-section">
      <a-card :style="{ width: '50%', margin: 'auto' }">
        <div class="div-container-stamp-types-info">
            <div class="div-photo-container">
                <div v-if="stampData.photo_path_basic && stampData.photo_path_basic !== 'None'">
                  <div class="custom-image-container">
                    <img :src="getAbsolutePath(stampData.photo_path_basic)" alt="Stamp Image" />
                  </div>
                </div>
                <div v-else>
                    <a-empty />
                </div>
            </div>
            <div class="divider"></div>
            <div class="left-main-div">
                <div class="information-div">Catalog number</div>
                <div class="information-div">Name</div>
                <div class="information-div">Emission</div>
                <div class="information-div">Country</div>
            </div>
            <div class="right-main-div">
                <div class="information-div">{{ upperSectionData['Catalog Number'] }}</div>
                <div class="information-div">{{ upperSectionData['Name'] }}</div>
                <div class="information-div">{{ upperSectionData['Emission ID'] }}</div>
                <div class="information-div">{{ upperSectionData['Country'] }}</div>
            </div>
        </div>
      </a-card>
    </div>
</template>
  
  <script>
  export default {
    props: {
      stampData: Object,
    },
    computed: {
      upperSectionData() {
        return {
          'Catalog Number': this.stampData.catalog_number,
          'Name': this.stampData.name,
          'Emission ID': this.stampData.emission_id,
          'Country': this.stampData.country,
        };
      },
    },
    methods: {
      getAbsolutePath(relativePath) {
        return require('@/assets/' + relativePath);
      },
    }
  };
  </script>
  

  <style scoped>
  .upper-section {
    text-align: center;
  }
  
  .div-container-stamp-types-info {
    display: flex;
    flex-wrap: wrap;
  }
  
  .div-photo-container {
    width: 100%;
    display: flex;
    justify-content: center;
  }
  
  .left-main-div,
  .right-main-div {
    flex: 0 0 48%;
    margin: 0.5%;
  }

  .divider {
    width: 100%;
    height: 1px;
    background-color: #ccc; /* Barva oddělovače */
    margin: 10px 0; /* Můžete přizpůsobit mezery okolo oddělovače */
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
  </style>