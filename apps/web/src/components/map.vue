<template>
  <div class="chart-wrapper">
    <div class="map-header">
      <div class="map-tip">
        💡 提示：点击地图上的区域可查看该区域的人口结构数据
      </div>
    </div>
    <div 
      ref="chartContainer" 
      class="chart-container"
      :class="{ 'loading-overlay': loading }"
    ></div>
    <div v-if="loading" class="loading">加载中...</div>
    <div v-if="error" class="error">{{ error }}</div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import * as echarts from 'echarts';
import china from '@/data/china.json'; 

const props = defineProps({
  currentMapName: {
    type: String,
    default: 'china'
  }
});

const emit = defineEmits(['map-change', 'region-click']);

const chartContainer = ref(null);
let currentChart = null;
let currentMapName = ref('china');
const loading = ref(false);
const error = ref('');

// 获取GeoJSON数据
const getJson = async (adcode) => {
  try {
    const response = await fetch(`https://geo.datav.aliyun.com/areas_v3/bound/geojson?code=${adcode}_full`);
    if (!response.ok) throw new Error('网络请求失败');
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('获取地图数据失败:', error);
    error.value = '加载地图数据失败，请检查网络连接';
    return null;
  }
};

// 渲染中国地图
const renderChinaMap = async () => {
  if (!currentChart) return;
  
  loading.value = true;
  error.value = '';
  
  try {
    // const chinaGeoJson = await getJson('100000');
    // if (!chinaGeoJson) {
    //   throw new Error('无法加载中国地图数据');
    // }
    echarts.registerMap('china', china);
    
    // 处理 features 数据
    const features = china.features || [];
    const validFeatures = features.filter(feature => {
      const props = feature.properties;
      return props && props.name && !props.name.includes('南海');
    });
    
    // 生成区域数据（添加随机数值用于可视化）
    const regionData = validFeatures.map(feature => {
      const props = feature.properties;
      return {
        name: props.name,
        value: Math.floor(Math.random() * 70) + 30,
        adcode: props.adcode ? String(props.adcode) : '',
        level: props.level || 'province'
      };
    });
    
    // 配置地图选项
    currentChart.setOption({
      title: {
        show: true,
        text: '中国地图',
        left: 'center',
        top: 10,
        textStyle: { fontSize: 16, fontWeight: 'bold' }
      },
      tooltip: {
        trigger: 'item',
        formatter: (params) => {
          if (params.data) {
            return `${params.name}<br/>点击查看人口结构数据`;
          }
          return `${params.name}`;
        }
      },
      visualMap: {
        min: 0,
        max: 100,
        left: 'left',
        top: 'bottom',
        text: ['高', '低'],
        inRange: { color: ['#e8f5e9', '#66bb6a', '#2e7d32'] },
        show: false,
        calculable: true
      },
      series: [{
        name: '中国地图',
        type: 'map',
        map: 'china',
        roam: true,  // 允许缩放和平移
        zoom: 1.2,
        scaleLimit: { min: 0.8, max: 3 },
        label: {
          show: true,
          fontSize: 10,
          formatter: '{b}',
          color: '#333'
        },
        emphasis: {
          label: { show: true, fontWeight: 'bold' },
          itemStyle: { areaColor: '#ffd700', borderWidth: 1 }
        },
        select: {
          label: { show: true },
          itemStyle: { areaColor: '#ff9800' }
        },
        data: regionData
      }]
    });
    
    currentMapName.value = 'china';
    
    // 触发父组件事件
    emit('map-change', { name: '中国', adcode: '100000', level: 'country' });
  } catch (err) {
    console.error('初始化中国地图失败:', err);
    error.value = '初始化地图失败：' + err.message;
  } finally {
    loading.value = false;
  }
};

// 处理区域点击（只返回区域信息，不下钻）
const handleRegionClick = (params) => {
  if (!params.data) return;
  
  // 获取点击的区域信息
  const regionInfo = {
    name: params.name,
    adcode: params.data.adcode ? String(params.data.adcode) : '',
    value: params.data.value,
    level: params.data.level || 'province'
  };
  
  // console.log('点击区域:', regionInfo);
  
  // 触发事件，将区域名称返回给父组件
  emit('region-click', regionInfo);
  // 同时触发 map-change 事件
  emit('map-change', { 
    name: regionInfo.name, 
    adcode: regionInfo.adcode, 
    level: regionInfo.level 
  });
};

// 初始化图表
const initChart = () => {
  if (!chartContainer.value) return;
  
  if (currentChart) {
    currentChart.dispose();
  }
  
  currentChart = echarts.init(chartContainer.value);
  
  // 添加点击事件
  currentChart.on('click', handleRegionClick);
  
  // 渲染中国地图
  renderChinaMap();
};

// 清理资源
// const cleanup = () => {
//   if (currentChart) {
//     currentChart.off('click', handleRegionClick);
//     currentChart.dispose();
//     currentChart = null;
//   }
// };

// 窗口适配
let resizeObserver = null;

onMounted(() => {
  initChart();
  
  // 监听窗口大小变化
  const handleResize = () => {
    if (currentChart) {
      currentChart.resize();
    }
  };
  window.addEventListener('resize', handleResize);
  
  // 保存清理函数
  // const originalCleanup = cleanup;
  // cleanup = () => {
  //   window.removeEventListener('resize', handleResize);
  //   originalCleanup();
  // };
});

onUnmounted(() => {
    if (handleResize) {
      window.removeEventListener('resize', handleResize);
    }
    if (currentChart) {
      currentChart.dispose();
      currentChart = null;
    }
});

// 暴露方法给父组件
defineExpose({
  refreshMap: renderChinaMap
});
</script>

<style scoped>
.chart-wrapper {
  width: 100%;
  height: 100%;
  position: relative;
  display: flex;
  flex-direction: column;
}

.map-header {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  padding: 12px 16px;
  background: #f8f9fa;
  border-bottom: 1px solid #e9ecef;
}

.map-tip {
  font-size: 12px;
  color: #6c757d;
  background: #f1f3f5;
  padding: 6px 12px;
  border-radius: 20px;
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.chart-container {
  flex: 1;
  width: 500px;
  height: 300px;
  transition: opacity 0.3s ease;
}

.chart-container.loading-overlay {
  opacity: 0.6;
}

.loading {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: rgba(0, 0, 0, 0.7);
  color: white;
  padding: 10px 20px;
  border-radius: 8px;
  z-index: 10;
  font-size: 14px;
}

.error {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: rgba(220, 53, 69, 0.9);
  color: white;
  padding: 12px 24px;
  border-radius: 8px;
  z-index: 10;
  font-size: 14px;
}
</style>