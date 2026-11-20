<script setup>

import { ref, onMounted, onBeforeUnmount } from 'vue';
import * as echarts from 'echarts';

const chartContainer = ref(null);
let myChart = null;

const roundDatas = (num, size, starname, color, mark = 0) => {
  const datas = Array.from({ length: num }, (_, index) => ({
    name: `circle${index}`
  }));
  const validMark = ((mark % num) + num) % num;

  datas[validMark] = {
    name: `circle${validMark}`,
    value: starname,
    symbolSize: size,
    itemStyle: { color },
    label: {
      show: true,
      formatter: starname,
      position: 'top'
    }
  };
  return datas;
};

const linkDatas = (num) => {
  if (num < 2) return [];
  return Array.from({ length: num }, (_, index) => ({
    source: `circle${index}`,
    target: `circle${(index + 1) % num}`
  }));
};

const starSeries = (circlesize, data, links, rotateLabel) => ({
  type: 'graph',
  layout: 'circular',
  circular: { rotateLabel },
  symbol: 'circle',
  symbolSize: 1,
  width: circlesize,
  height: circlesize,
  data,
  links
});

const handleResize = () => {
  if (myChart) {
    myChart.resize();
  }
};

onMounted(async()=>{
  if (!chartContainer.value) return;
  myChart = echarts.init(chartContainer.value);
  const option = {
      backgroundColor: '#1d1626',
      series: [
          starSeries('0%',  roundDatas(1,  40, '我', '#ef4136'), linkDatas(1), false),
          starSeries('15%', roundDatas(30, 15, '父母', '#72baa7',5), linkDatas(30), false),
          starSeries('15%', roundDatas(30, 15, '兄弟姐妹', '#72baa7',15), linkDatas(30), false),
          starSeries('15%', roundDatas(30, 15, '配偶', '#72baa7',25), linkDatas(30), false),
          starSeries('25%', roundDatas(40, 15, '朋友', '#c88400',10), linkDatas(40), false),
          starSeries('25%', roundDatas(40, 15, '同事', '#c88400',50), linkDatas(40), false),
          starSeries('25%', roundDatas(40, 15, '亲戚', '#c88400',100), linkDatas(40), false),
          starSeries('35%', roundDatas(50, 15, '陌生人', '#00BFFF',55), linkDatas(50), false),
          
      ]
  }
  myChart.setOption(option);
  window.addEventListener('resize', handleResize);
});

onBeforeUnmount(() => {
  if (myChart) {
    myChart.dispose();
    myChart = null;
  }
  window.removeEventListener('resize', handleResize);
});

</script>

<template>
  <div class="page-layout">
    <main class="page-content">
      <div class="chart-wrapper">
        <div
          ref="chartContainer"
          class="chart-container"
          id="main"
        ></div>
      </div>
    </main>
  </div>
</template>
<style scoped>
.page-layout {
  display: flex;
  height: calc(100vh - 34px);
  height: calc(100dvh - 34px);
  background: #fff;
}

.page-content {
  display: flex;
  flex-direction: column;
  flex: 1;
  min-width: 0;
  min-height: 0;
}

.chart-wrapper {
  flex: 1;
  width: 100%;
  min-height: 0;
  position: relative;
}

.chart-container {
  width: 100%;
  height: 100%;
  min-height: 0;
}

</style>