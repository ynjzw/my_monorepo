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
const loading = ref(false)
const error = ref(null)

onMounted( () => {
    var chartDom = document.getElementById('main');
    var myChart = echarts.init(chartDom);
    var option;

    const data = [
        {
            fixed: true,
            x: myChart.getWidth() / 2,
            y: myChart.getHeight() / 2,
            symbolSize: 20,
            id: '-1'
        }
    ];
    const edges = [];
    option = {
        series: [
            {
            type: 'graph',
            layout: 'force',
            animation: false,
            data: data,
            force: {
                // initLayout: 'circular'
                // gravity: 0
                repulsion: 100,
                edgeLength: 5
            },
            edges: edges
            }
        ]
    };
    setInterval(function () {
        data.push({
            id: data.length + ''
        });
        //var source = Math.round((data.length - 1) * Math.random());
        //var target = Math.round((data.length - 1) * Math.random());
        //if (source !== target) {
        //    edges.push({
        //    source: source,
        //    target: target
        //    });
        //}
        myChart.setOption({
            series: [
            {
                roam: true,
                data: data,
                edges: []
            }
            ]
        });
    // console.log('nodes: ' + data.length);
    // console.log('links: ' + data.length);
    }, 1000);

    option && myChart.setOption(option);
})
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