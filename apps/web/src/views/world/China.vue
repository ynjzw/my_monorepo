<template>
  <div class="dashboard">
    <div class="map-section">
      <Map 
        ref="mapRef"        
        @map-change="handleMapChange"
        @region-click="handleRegionClick"
      />
    </div>
    
    <div class="funnel-section">
      <div class="tab-nav">
        <button 
          v-for="tab in tabs" 
          :key="tab.name"
          @click="currentTab = tab.component"
          :class="{ active: currentTab === tab.component }"
        >
          {{ tab.label }}
        </button>
      </div> 
      <Funnel ref="funnelRef" :data="funnelData" :title="funnelTitle"></Funnel>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import Map from '@/components/map.vue';
import Funnel from '@/components/funnel.vue';
import { population_structure } from '@/api/simple_api';

const tabs = [
  { name: 'tabA', label: '人口结构', component: Funnel },
  { name: 'tabB', label: '收入结构', component: Funnel }
]
const currentTab = ref(tabs[0].component)

const mapRef = ref(null);
const funnelRef = ref(null);
const currentMapName = ref('');
const funnelData = ref([]);
const funnelTitle = ref('人口结构分布图');
const funnelLoading = ref(false);
const data = ref([]);

// 根据区域名称获取人口结构数据
const fetchPopulationStructure = async (regionName) => {
  funnelLoading.value = true;
  
  const response = await population_structure();
    
    // 查找匹配的区域数据
  let regionData = null;
  
  if (Array.isArray(response) && response.length > 0) {
    
      regionData = response.find(item => 
        item.region_name?.includes(regionName) || 
        regionName.includes(item.region_name)
      );
    
  }
  // console.log(regionData)
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
      funnelTitle.value = `${regionName} - 2020年人口结构分布`;
      return;
    }
  }
  
  
  funnelTitle.value = `${regionName} - 人口结构分布`;
  await console.log(funnelData.value)
};

// 处理地图变更
const handleMapChange = ({ name, adcode, level }) => {
  // currentMapName.value = name;
  // fetchPopulationStructure(name);
};

// 处理区域点击
const handleRegionClick = (regionInfo) => {
  
  const { name, adcode, level } = regionInfo;
  fetchPopulationStructure(name);
};

// 初始化加载全国数据
onMounted(async ()=>{
  // data.value = await population_structure()
  // console.log(data.value);
  await fetchPopulationStructure('全国')
})
</script>

<style scoped>
.dashboard {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  padding: 20px;
  background: #f5f7fa;
}

.map-section {
  flex: 2;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.funnel-section {
  flex: 1;
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