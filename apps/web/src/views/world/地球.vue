<template>
  <div class="map" >
     <div ref="mapRef" class="map-container" ></div>
  </div>
</template>
<script setup>
import { ref, onMounted } from 'vue';
import * as echarts from 'echarts';
import {useRouter} from 'vue-router'
import earth from '@/data/earth.json'; // 本地中国地图数据
import { extract_triples } from '@/api';

const router = useRouter();
const mapRef = ref(null);

onMounted(async () => {
  const chart = echarts.init(mapRef.value);
  // 动态加载中国地图geoJSON
  // const geoJson = await fetch('https://geo.datav.aliyun.com/areas_v3/bound/100000_full.json').then(res => res.json());
  echarts.registerMap('earth', earth);
  const features = earth.features || [];
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
      inRange: { color: ['#e8f5e9', '#4caf50', '#2e7d32'] }, 
      show: true
    },
    series: [{
      name: '地球地图',
      type: 'map',
      map: 'earth',
      roam: true,
      label: { show: false },
      data: allRegionData // 可填充省份数据
    }]
  });
  chart.on('click', function (params) {
    if (params.data){
      // const { adcode, name, level } = params.data;
      // console.log(params)
      // const geoJson = fetch('https://geo.datav.aliyun.com/areas_v3/bound/' + params.data.adcode + '_full.json').then(res => res.json());
      // console.log(geoJson)
      router.push(params.data.name)
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