<script setup>

import { ref, onMounted, onBeforeUnmount, watch, nextTick } from 'vue';
import * as echarts from 'echarts';
import * as d3 from 'd3-hierarchy';
const tabs=['人际网络','健康','收入/支出/储蓄']
const data = {
                "$count": 100,
                "人际网络": { 
                  "$count": 10
                },
                "健康": { 
                  "$count": 10
                },
                "收入/支出/储蓄": { 
                  "$count": 10
                }
              };

const chartContainer = ref(null);
const myChart = ref(null);
const seriesData = ref([]);
const maxDepth = ref(0);
const displayRoot = ref(null);
const currentDepth = ref(0);
const error = ref(null);
const loading = ref(false);
const handleResize = () => {
  if (myChart.value) {
    myChart.value.resize();
  }
};
// 准备数据
onMounted(async()=>{
  var ROOT_PATH = 'https://echarts.apache.org/examples';

  var chartDom = document.getElementById('main');
  var myChart = echarts.init(chartDom);
  var option;

  $.get(
    ROOT_PATH + '/data/asset/geo/Veins_Medical_Diagram_clip_art.svg',
    function (svg) {
      echarts.registerMap('organ_diagram', { svg: svg });
      option = {
        tooltip: {},
        geo: {
          left: 10,
          right: '50%',
          map: 'organ_diagram',
          selectedMode: 'multiple',
          emphasis: {
            focus: 'self',
            itemStyle: {
              color: null
            },
            label: {
              position: 'bottom',
              distance: 0,
              textBorderColor: '#fff',
              textBorderWidth: 2
            }
          },
          blur: {},
          select: {
            itemStyle: {
              color: '#b50205'
            },
            label: {
              show: false,
              textBorderColor: '#fff',
              textBorderWidth: 2
            }
          }
        },
        grid: {
          left: '60%',
          top: '20%',
          bottom: '20%'
        },
        xAxis: {},
        yAxis: {
          data: [
            'heart',
            'large-intestine',
            'small-intestine',
            'spleen',
            'kidney',
            'lung',
            'liver'
          ]
        },
        series: [
          {
            type: 'bar',
            emphasis: {
              focus: 'self'
            },
            data: [121, 321, 141, 52, 198, 289, 139]
          }
        ]
      };
      myChart.setOption(option);
      myChart.on('mouseover', { seriesIndex: 0 }, function (event) {
        myChart.dispatchAction({
          type: 'highlight',
          geoIndex: 0,
          name: event.name
        });
      });
      myChart.on('mouseout', { seriesIndex: 0 }, function (event) {
        myChart.dispatchAction({
          type: 'downplay',
          geoIndex: 0,
          name: event.name
        });
      });
    }
  );

  option && myChart.setOption(option);
})

</script>

<template>
  <div class="chart-wrapper">
    <div 
      ref="chartContainer" 
      class="chart-container"
      id="main"
    ></div>
    <div v-if="loading" class="loading">加载中...</div>
    <div v-if="error" class="error">{{ error }}</div>
  </div>
</template>
<style scoped>
.chart-wrapper {
  width: 100%;
  height: 100%;
  position: relative;
}

.chart-container {
  width: 100%;
  height: 100%;
  min-height: 400px; /* 设置最小高度 */
}

.loading, .error {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
  padding: 20px;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 4px;
  z-index: 10;
}

</style>