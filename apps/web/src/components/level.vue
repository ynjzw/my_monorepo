<script setup>
import { onMounted, ref } from 'vue';
import * as echarts from 'echarts';

const props=defineProps({
  data: {
    type: Array,
    default: []
  },
  msg: {
    type: String,
    default: ''
  }
})

const test=()=>{
  const chartDom = document.getElementById('main');  
  
  const myChart = echarts.getInstanceByDom(chartDom);

  if (myChart) {
    myChart.dispose();
  }
      
  const option = {
              series: [
                  {
                  type: 'graph',
                  layout: 'none',
                  symbolSize: 50,
                  roam: true,
                  label: {
                      show: true
                  },
                  data: props.data,
                  links: [],
                  // links: links,
                  lineStyle: {
                      opacity: 0.9,
                      width: 2,
                      curveness: 0
                  }
                  }
              ]
    };
    myChart.setOption(option);
}

onMounted(async ()=>{    
    await test();
})

</script>

<template>
    <div id="main" ></div>
</template>