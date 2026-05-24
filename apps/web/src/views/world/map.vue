// map.vue - 地图组件（完善版）
<template>
  <div class="chart-wrapper">
    <div class="map-header">
      <button 
        v-if="currentMapName !== 'china'" 
        @click="initChinaMap" 
        class="drill-btn"
      >
        ← 返回全国地图
      </button>
      <div class="map-tip">
        💡 提示：点击地图区域下钻，按 ESC 键返回上一级
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
import { ref, onMounted, onUnmounted, watch } from 'vue';
import * as echarts from 'echarts';

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
let currentAdcode = ref('100000');
let historyStack = ref([]); // 历史记录栈，用于支持返回
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

// 添加上钻功能（键盘ESC）
const setupKeyboardDrill = () => {
  const handleKeyDown = (e) => {
    if (e.key === 'Escape' && currentMapName.value !== 'china') {
      initChinaMap();
    }
  };
  window.addEventListener('keydown', handleKeyDown);
  return () => window.removeEventListener('keydown', handleKeyDown);
};

// 渲染地图
const renderMap = async (name, adcode, level) => {
  if (!currentChart) return;
  
  loading.value = true;
  error.value = '';
  
  try {
    const geoJson = await getJson(adcode);
    if (!geoJson || !geoJson.features || geoJson.features.length === 0) {
      alert('无法加载该区域地图数据');
      return false;
    }
    
    // 注册新地图
    const mapName = `map_${adcode}`;
    echarts.registerMap(mapName, geoJson);
    
    // 准备数据
    const features = geoJson.features || [];
    const regionData = features.map(feature => {
      const props = feature.properties;
      return {
        name: props.name,
        value: Math.floor(Math.random() * 60) + 20, // 随机数据20-80
        adcode: props.adcode,
        level: props.level
      };
    });
    
    // 动态计算visualMap的配色
    const visualMapConfig = level === 'country' ? {
      min: 0,
      max: 100,
      inRange: { color: ['#e8f5e9', '#4caf50', '#2e7d32'] }
    } : {
      min: 0,
      max: 100,
      inRange: { color: ['#e3f2fd', '#2196f3', '#1565c0'] }
    };
    
    // 更新图表配置
    currentChart.setOption({
      title: {
        show: true,
        text: name,
        left: 'center',
        top: 10,
        textStyle: { fontSize: 16, fontWeight: 'bold' }
      },
      tooltip: {
        trigger: 'item',
        formatter: (params) => {
          if (params.data) {
            return `${params.name}<br/>数值：${params.value}<br/>点击查看详情`;
          }
          return `${params.name}`;
        }
      },
      visualMap: {
        ...visualMapConfig,
        left: 'left',
        top: 'bottom',
        text: ['高', '低'],
        show: true,
        calculable: true,
        seriesIndex: 0
      },
      series: [{
        name: name,
        type: 'map',
        map: mapName,
        roam: true,
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
    }, true);
    
    currentMapName.value = name;
    currentAdcode.value = adcode;
    
    // 触发父组件事件
    emit('map-change', { name, adcode, level });
    return true;
  } catch (err) {
    console.error('渲染地图失败:', err);
    error.value = '渲染地图失败';
    return false;
  } finally {
    loading.value = false;
  }
};

// 点击下钻处理
const handleMapClick = async (params) => {
  if (!params.data) return;
  
  const { adcode, name, level } = params.data;
  console.log('点击区域:', { adcode, name, level });
  
  // 触发父组件的区域点击事件
  emit('region-click', { adcode, name, level });
  
  // district级别（区县级）不再下钻
  if (level === 'district') {
    alert('当前为区县级区域，无法继续下钻');
    return;
  }
  
  // 保存当前状态到历史栈
  historyStack.value.push({
    name: currentMapName.value,
    adcode: currentAdcode.value
  });
  
  // 检查是否有子区域数据
  const testData = await getJson(adcode);
  if (testData && testData.features && testData.features.length > 0) {
    await renderMap(name, adcode, level);
  } else {
    alert('该区域暂无更详细的地图数据');
    // 如果失败，从历史栈中移除刚才添加的记录
    historyStack.value.pop();
  }
};

// 初始化中国地图
const initChinaMap = async () => {
  if (!currentChart) return;
  
  loading.value = true;
  error.value = '';
  
  try {
    // 清空历史栈
    historyStack.value = [];
    
    const chinaGeoJson = await getJson('100000');
    if (!chinaGeoJson) return;
    
    echarts.registerMap('china', chinaGeoJson);
    
    const features = chinaGeoJson.features || [];
    // 过滤掉一些特殊区域（如南海诸岛等）
    const validFeatures = features.filter(f => 
      f.properties && f.properties.name && !f.properties.name.includes('南海')
    );
    
    const allRegionData = validFeatures.map(feature => {
      const props = feature.properties;
      return {
        name: props.name,
        value: Math.floor(Math.random() * 70) + 30, // 随机数据30-100
        adcode: props.adcode,
        level: props.level || 'province'
      };
    });
    
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
        formatter: '{b}<br/>数值：{c}<br/>点击查看详情'
      },
      visualMap: {
        min: 0,
        max: 100,
        left: 'left',
        top: 'bottom',
        text: ['高', '低'],
        inRange: { color: ['#e8f5e9', '#66bb6a', '#2e7d32'] },
        show: true,
        calculable: true
      },
      series: [{
        name: '中国地图',
        type: 'map',
        map: 'china',
        roam: true,
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
          itemStyle: { areaColor: '#ffd700' }
        },
        select: {
          label: { show: true },
          itemStyle: { areaColor: '#ff9800' }
        },
        data: allRegionData
      }]
    });
    
    currentMapName.value = 'china';
    currentAdcode.value = '100000';
    
    // 触发父组件事件
    emit('map-change', { name: '中国', adcode: '100000', level: 'country' });
  } catch (err) {
    console.error('初始化中国地图失败:', err);
    error.value = '初始化地图失败';
  } finally {
    loading.value = false;
  }
};

// 返回上一级（如果历史记录存在）
const goBack = () => {
  if (historyStack.value.length === 0) {
    initChinaMap();
    return;
  }
  
  const prev = historyStack.value.pop();
  if (prev && prev.adcode !== currentAdcode.value) {
    renderMap(prev.name, prev.adcode, 'province');
  }
};

// 清理资源
const cleanup = () => {
  if (currentChart) {
    currentChart.dispose();
    currentChart = null;
  }
};

// 暴露方法给父组件
defineExpose({
  cleanup,
  initChinaMap,
  goBack
});

let removeKeyboardListener = null;

onMounted(async () => {
  if (!chartContainer.value) return;
  
  // 初始化图表
  currentChart = echarts.init(chartContainer.value);
  
  // 初始化中国地图
  await initChinaMap();
  
  // 添加下钻点击事件
  currentChart.on('click', handleMapClick);
  
  // 添加上钻功能（键盘）
  removeKeyboardListener = setupKeyboardDrill();
  
  // 窗口适配
  const handleResize = () => {
    currentChart && currentChart.resize();
  };
  window.addEventListener('resize', handleResize);
  
  // 保存清理函数
  const originalCleanup = cleanup;
  cleanup = () => {
    originalCleanup();
    window.removeEventListener('resize', handleResize);
    if (removeKeyboardListener) removeKeyboardListener();
  };
});

onUnmounted(() => {
  cleanup();
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
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  background: #f8f9fa;
  border-bottom: 1px solid #e9ecef;
  flex-wrap: wrap;
  gap: 10px;
}

.drill-btn {
  background: #4caf50;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.3s ease;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.drill-btn:hover {
  background: #45a049;
  transform: translateY(-1px);
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15);
}

.drill-btn:active {
  transform: translateY(0);
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
  width: 100%;
  min-height: 500px;
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