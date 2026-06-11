<template>
  <div class="dashboard">
    <div class="map-section">
      <Map 
        ref="mapRef"
        
        @map-change="handleMapChange"
        @region-click="handleRegionClick"
      />
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import Map from './map.vue';
import Funnel from './funnel.vue';
import { population_structure } from '@/api/simple_api';

const mapRef = ref(null);
const currentMapName = ref('');
const funnelData = ref([]);
const funnelTitle = ref('人口结构分布图');
const funnelLoading = ref(false);

// 根据区域名称获取人口结构数据
const fetchPopulationStructure = async (regionName) => {
  funnelLoading.value = true;
  
  try {
    const response = await population_structure();
    
    // 查找匹配的区域数据
    let regionData = null;
    
    if (Array.isArray(response) && response.length > 0) {
      
        regionData = response.find(item => 
          item.region_name?.includes(regionName) || 
          regionName.includes(item.region_name)
        );
      
    }
    
    // 生成漏斗图数据
    if (regionData) {
      const funnelItems = [];
      
      if (regionData.population_radio_under_14 !== undefined) {
        funnelItems.push({
          name: '14岁以下人口比例',
          value: Number(regionData.population_radio_under_14) || 0
        });
      }
      
      if (regionData.population_radio_between_15_and_64 !== undefined) {
        funnelItems.push({
          name: '15-64岁人口比例',
          value: Number(regionData.population_radio_between_15_and_64) || 0
        });
      }
      
      if (regionData.population_radio_above_65 !== undefined) {
        funnelItems.push({
          name: '65岁以上人口比例',
          value: Number(regionData.population_radio_above_65) || 0
        });
      }
      
      if (funnelItems.length > 0) {
        funnelData.value = funnelItems;
        funnelTitle.value = `${regionName} - 人口结构分布`;
        return;
      }
    }
    
    // 默认数据
    funnelData.value = [
      { name: '14岁以下人口比例', value: 18.5 },
      { name: '15-64岁人口比例', value: 70.2 },
      { name: '65岁以上人口比例', value: 11.3 }
    ];
    funnelTitle.value = `${regionName} - 人口结构分布`;
    
  } catch (error) {
    console.error('获取人口结构数据失败:', error);
    funnelData.value = [];
    funnelTitle.value = `${regionName} - 数据加载失败`;
  } finally {
    funnelLoading.value = false;
  }
};

// 处理地图变更
const handleMapChange = ({ name, adcode, level }) => {
  // currentMapName.value = name;
  fetchPopulationStructure(name);
};

// 处理区域点击
const handleRegionClick = (regionInfo) => {
  const { name, adcode, level } = regionInfo;
  console.log('点击区域:', name, adcode, level);
  fetchPopulationStructure(name);
};

// 初始化加载全国数据

</script>

<style scoped>
.dashboard {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  padding: 20px;
  background: #f5f7fa;
  min-height: 100vh;
}

.map-section {
  flex: 2;
  min-width: 600px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.funnel-section {
  flex: 1;
  min-width: 320px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  padding: 16px;
}

@media (max-width: 1000px) {
  .dashboard {
    flex-direction: column;
  }
  
  .map-section,
  .funnel-section {
    min-width: auto;
  }
}
</style>