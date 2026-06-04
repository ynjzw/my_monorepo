// China.vue - 父组件
<template>
  <div class="dashboard">
    <div class="map-section">
      <Map 
        ref="mapRef"
        :currentMapName="currentMapName"
        @map-change="handleMapChange"
        @region-click="handleRegionClick"
      />
    </div>
    <div class="funnel-section">
      <Funnel :data="funnelData" />
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, onUnmounted } from 'vue';
import Map from './map.vue';
import Funnel from './funnel.vue';
import { population_structure } from '@/api/simple_api';

const mapRef = ref(null);
const currentMapName = ref('全国');
const funnelData = ref([]);
const fData = ref([]);

// 根据区域生成漏斗图数据
const generateFunnelData = async (regionName) => {
  // 模拟不同区域的数据
  fData.value = await population_structure();
  regionName.includes(fData.value)
  const mockDataMap = {
    'china': [
      { name: '14岁以下人口比例', value: fData.value[0]['population_radio_under_14'] },
      { name: '15岁到64岁人口比例', value: fData.value[0]['population_radio_between_15_and_64'] },
      { name: '65岁以上人口比例', value: fData.value[0]['population_radio_above_65'] }
    ],
    'default': [
      { name: '一级指标', value: 100 },
      { name: '二级指标', value: 82 },
      { name: '三级指标', value: 67 },
      { name: '四级指标', value: 51 },
      { name: '五级指标', value: 38 }
    ]
  };
  
  // 根据区域名称返回特定数据
  if (regionName.includes('北京') || regionName.includes('上海') || regionName.includes('广东')) {
    return [
      { name: '高端用户', value: 45 },
      { name: '中端用户', value: 68 },
      { name: '普通用户', value: 82 },
      { name: '潜在用户', value: 94 }
    ];
  }
  
  return mockDataMap;
};

// 处理地图变更
const handleMapChange = ({ name, adcode, level }) => {
  currentMapName.value = name;
  const newFunnelData = generateFunnelData(name);
  funnelData.value = [...newFunnelData];
};

// 处理区域点击（用于额外逻辑）
const handleRegionClick = (regionInfo) => {
  // console.log('点击区域详情:', regionInfo);
  // 可以在这里添加额外的业务逻辑
};

onMounted(() => {
  // 初始化漏斗图数据
  funnelData.value = generateFunnelData('全国');
});

onUnmounted(() => {
  // 清理工作
  
});
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