<template>
  <div class="chart-wrapper">
    <div id="main"
    ></div>
    <div v-if="loading" class="loading">加载中...</div>
    <div v-if="error" class="error">{{ error }}</div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, watch, nextTick } from 'vue';
import * as echarts from 'echarts';
import {useRouter} from 'vue-router'
const router = useRouter();
const loading = ref(false)
const error = ref(null)
const roundDatas=(num, size, starname, color)=>{ 
    const datas = [];
    let i;
    for (i = 0; i < num; i++) {
        datas.push({
            name: 'circle' + i
        });
    }
    const mark = Math.floor(Math.random() * num);

    datas[mark] = {
        name: 'circle' + mark,
        value: starname,
        symbolSize: size,
        itemStyle: {
            color: color
        },
        label: {
            show: true,
            formatter: starname,
            position: 'top'
        }
    };
    return datas;
}
const linkDatas = (num) => {
    const ldatas = [];
    let i;
    for (i = 0; i < num; i++) {
        ldatas.push({
            source: 'circle' + i,
            target: 'circle' + (i + 1)
        });
    }
    ldatas.push({
        source: 'circle' + (i - 1),
        target: 'circle0'
    });
    return ldatas;
}
const starSeries=(circlesize, data, link, flag)=> {
    const star = {
        type: 'graph',
        layout: 'circular',
        circular: {
            rotateLabel: flag
        },
        symbol: 'circle',
        symbolSize: 1,
        width: circlesize,
        height: circlesize,
        data: data,
        links: link
    };
    return star;
}

onMounted(() => { 
  var chartDom = document.getElementById('main');
  var myChart = echarts.init(chartDom);
  var option;
  
  option = {
    //   backgroundColor: '#1d1626',
      series: [
          starSeries('0%', roundDatas(1, 40, '太阳', '#ef4136'), linkDatas(1), false),
          starSeries('15%', roundDatas(30, 15, '水星', '#72baa7'), linkDatas(30), false),
          starSeries('25%', roundDatas(40, 15, '金星', '#c88400'), linkDatas(40), false),
          starSeries('35%', roundDatas(50, 15, '地球', '#00BFFF'), linkDatas(50), false),
          starSeries('45%', roundDatas(60, 15, '火星', '#FF5809'), linkDatas(60), false),
          starSeries('55%', roundDatas(70, 20, '木星', '#e0861a'), linkDatas(70), false),
          starSeries('65%', roundDatas(80, 23, '土星', '#33a3dc'), linkDatas(80), false),
          starSeries('75%', roundDatas(90, 28, '天王星', '#8f4b4a'), linkDatas(90), false),
          starSeries('85%', roundDatas(100, 30, '海王星', '#afb4db'), linkDatas(100), false),
          starSeries('95%', roundDatas(110, 30, '冥王星\n(矮行星)', '#6f60aa'), linkDatas(110), false),
      ]
  }
  setInterval(function () { 
    option && myChart.setOption(option);
  },100)
  if (!myChart) return
  
  // 节点点击事件
  myChart.on('click', function (params) {
    // console.log(params.data.value)
    const value=params.data.value
    router.push(value)
  })
});
</script>

<style>
.loading {
  text-align: center;
  padding: 20px;
}
.error {
  color: red;
}
.chart-wrapper {
  width: 100%;
  height: 100%;
  position: relative;
}

#main {
  width: 100%;
  height: 100%;
  min-height: 400px; /* 设置最小高度 */
  min-width: 400px; 
}
</style>
