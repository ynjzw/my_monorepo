<template>
  <div class="map" >
      <button v-if="currentMapName !== 'china'" @click="initChinaMap" class="drill-btn">
        返回全国地图 (按ESC键)
      </button>
      <div class="map-tip">💡 提示：点击地图区域下钻，按ESC键返回上一级</div>
     <map ref="mapRef" class="map-container" ></map>
    <Funnel :data="extract_triples(mapRef.value)" :link="mapRef.value"></Funnel>
  </div>
</template>
<script setup>
import { ref, onMounted } from 'vue';
import * as echarts from 'echarts';
import Funnel from '../components/funnel.vue';
import map from '../components/map.vue';

const mapRef = ref(null);

let currentChart = null;
let currentMapName = 'china';

// 获取GeoJSON数据
const getJson = async (adcode) => {
    try {
        const response = await fetch(`https://geo.datav.aliyun.com/areas_v3/bound/geojson?code=${adcode}_full`);
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('获取地图数据失败:', error);
        return null;
    }
};
// 添加上钻功能
const addUpDrill = () => {
    // 监听键盘事件，按ESC键返回上一级
    window.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && currentMapName !== 'china') {
            // 返回中国地图
            initChinaMap();
        }
    });
};

// 渲染地图
const renderMap = async (name, adcode) => {
    if (!currentChart) return;
    
    // 获取区域GeoJSON数据
    const geoJson = await getJson(adcode);
    if (!geoJson) {
        alert('无法加载该区域地图数据');
        return;
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
            value: Math.floor(Math.random() * 100), // 示例数据
            adcode: props.adcode,
            level: props.level
        };
    });
    
    // 更新图表配置
    currentChart.setOption({
        title: {
            show: true,
            text: name,
            left: 'center',
            top: 10,
            textStyle: { fontSize: 16 }
        },
        visualMap: {
            min: 0,
            max: 100,
            left: 'left',
            top: 'bottom',
            text: ['高', '低'],
            inRange: { color: ['#e0ffe0', '#00b050', '#006400'] },
            show: true,
            calculable: true
        },
        series: [{
            name: name,
            type: 'map',
            map: mapName,
            roam: true,
            zoom: 1.2,
            label: {
                show: true,
                fontSize: 10,
                formatter: '{b}'
            },
            emphasis: {
                label: { show: true },
                itemStyle: { areaColor: '#ffd700' }
            },
            data: regionData
        }]
    }, true); // 第二个参数true表示完全替换配置
    
    currentMapName = name;
};

// 点击下钻处理
const handleMapClick = async (params) => {
    if (!params.data) return;
    
    const { adcode, name, level } = params.data;
    console.log('点击区域:', { adcode, name, level });
    
    // district级别不再下钻
    if (level === 'district') {
        alert('当前为区县级区域，无法继续下钻');
        return;
    }
    
    // 检查是否有子区域数据（省级下钻到市级，市级下钻到区县级）
    // 通过尝试获取子区域数据来判断
    const testData = await getJson(adcode);
    if (testData && testData.features && testData.features.length > 0) {
        await renderMap(name, adcode);
    } else {
        alert('该区域暂无更详细的地图数据');
    }
};
// 初始化中国地图
const initChinaMap = async () => {
    if (!currentChart) return;
    
    const chinaGeoJson = await getJson('100000');
    if (!chinaGeoJson) return;
    
    echarts.registerMap('china', chinaGeoJson);
    
    const features = chinaGeoJson.features || [];
    const allRegionData = features.map(feature => {
        const props = feature.properties;
        return {
            name: props.name,
            value: Math.floor(Math.random() * 100), // 示例随机数据
            adcode: props.adcode,
            level: props.level
        };
    });
    
    currentChart.setOption({
        title: {
            show: true,
            text: '中国地图',
            left: 'center',
            top: 10,
            textStyle: { fontSize: 16 }
        },
        tooltip: { 
            trigger: 'item',
            formatter: '{b}<br/>数值：{c}'
        },
        visualMap: {
            min: 0,
            max: 100,
            left: 'left',
            top: 'bottom',
            text: ['高', '低'],
            inRange: { color: ['#e0ffe0', '#00b050', '#006400'] },
            show: true,
            calculable: true
        },
        series: [{
            name: '中国地图',
            type: 'map',
            map: 'china',
            roam: true,
            zoom: 1.2,
            label: {
                show: true,
                fontSize: 10,
                formatter: '{b}'
            },
            emphasis: {
                label: { show: true },
                itemStyle: { areaColor: '#ffd700' }
            },
            data: allRegionData
        }]
    });
    
    currentMapName = 'china';
};

onMounted(async () => {
      // 初始化图表
    currentChart = echarts.init(mapRef.value);
    
    // 初始化中国地图
    await initChinaMap();
    
    // 添加下钻点击事件
    currentChart.on('click', handleMapClick);
    
    // 添加上钻功能
    addUpDrill();
    
    // 窗口适配
    window.addEventListener('resize', () => {
        currentChart && currentChart.resize();
    });
});
</script>
<style scoped> 
.map{
    width: 1000px;
    height: 600px;
}
.map-container{
    width: 1000px;
    height: 600px;
}

</style>