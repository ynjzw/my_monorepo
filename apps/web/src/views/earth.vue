<template>
  <div class="map" >
     <div ref="mapRef" class="map-container" ></div>
  </div>
</template>
<script setup>
import { ref, onMounted } from 'vue';
import * as echarts from 'echarts';
import earth from '@/data/earth.json'; // 本地中国地图数据

const mapRef = ref(null);

onMounted(async () => {
  const chart = echarts.init(mapRef.value);
  // 动态加载中国地图geoJSON
  const geoJson = await fetch('https://geo.datav.aliyun.com/areas_v3/bound/100000_full.json').then(res => res.json());
  echarts.registerMap('earth', earth);
  chart.setOption({
    tooltip: { trigger: 'item' },
    visualMap: {
      min: 0,
      max: 100,
      left: 'left',
      top: 'bottom',
      text: ['高','低'],
      inRange: { color: ['#e0ffe0', '#00b050', '#006400'] }, // 绿色渐变
      show: false
    },
    series: [{
      name: '中国地图',
      type: 'map',
      map: 'earth',
      roam: true,
      label: { show: false },
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