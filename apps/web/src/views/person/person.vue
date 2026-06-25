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
// 准备数据

</script>

<template>
  <div class="chart-wrapper">
    <div 
      ref="chartContainer" 
      class="chart-container"
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