<template>
  <div class="map" >
     <div ref="mapRef" class="map-container" ></div>
  </div>
</template>
<script setup>
import { ref, onMounted } from 'vue';
import * as echarts from 'echarts';
import china from '@/data/geojson.json'; // 本地中国地图数据

const mapRef = ref(null);

onMounted(async () => {
  const chart = echarts.init(mapRef.value);
  // 动态加载中国地图geoJSON
  const geoJson = await fetch('https://geo.datav.aliyun.com/areas_v3/bound/100000_full.json').then(res => res.json());
  echarts.registerMap('china', geoJson);
  chart.setOption({
    tooltip: { trigger: 'item' },
    visualMap: {
      min: 0,
      max: 100,
      left: 'left',
      top: 'bottom',
      text: ['高','低'],
      inRange: { color: ['#e0ffe0', '#00b050', '#006400'] }, // 绿色渐变
      show: true
    },
    series: [{
      name: '中国地图',
      type: 'map',
      map: 'china',
      roam: true,
      label: { show: true },
      data: [] // 可填充省份数据
    }]
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