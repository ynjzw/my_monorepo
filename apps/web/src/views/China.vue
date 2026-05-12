<template>
  <div class="map" >
     <div ref="mapRef" class="map-container" ></div>
  </div>
</template>
<script setup>
import { ref, onMounted } from 'vue';
import * as echarts from 'echarts';
import china from '@/data/china.json'; // 本地中国地图数据
import {useRouter} from 'vue-router'

const router = useRouter();
const mapRef = ref(null);

onMounted(async () => {
  const chart = echarts.init(mapRef.value);
  // 动态加载中国地图geoJSON
  // const geoJson = await fetch('https://geo.datav.aliyun.com/areas_v3/bound/100000_full.json').then(res => res.json());
  echarts.registerMap('china', china);
  const features = china.features || [];
  const allRegionData = features.map(feature => {
    const props = feature.properties;
    return {
      name: props.name,
      value: 0,  // 默认值，后续可覆盖
      adcode: props.adcode,
      level: props.level
    };
  });
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
      map: 'china',
      roam: true,
      label: { show: true },
      data: allRegionData // 可填充省份数据
    }]
  });
  // 节点点击事件
  chart.on('click', function (params) {
    if (params.data){
      const geoJson = await fetch('https://geo.datav.aliyun.com/areas_v3/bound/' + params.data.adcode + '_full.json').then(res => res.json());
    }
  })
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