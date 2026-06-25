<template>
  
    <input v-model="ss"/>
    <button @click="test1()">ss</button>      
<!--       
    <CirclePackingChart :data="circleData"
      ref="chartRef"
      theme="auto"
      height="400px"
      @chart-ready="handleChartReady"
      @node-click="handleNodeClick"
      @data-loaded="handleDataLoaded"
      @error="handleError"></CirclePackingChart> -->

      <kkk :data="circleData"
      ref="chartRef"
      theme="auto"
      height="400px"
      @chart-ready="handleChartReady"
      @node-click="handleNodeClick"
      @data-loaded="handleDataLoaded"
      @error="handleError"></kkk>

</template>
<script setup>
import CirclePackingChart from '../components/CirclePackingChart.vue';
import kkk from '../components/circle.vue';
import { onMounted,ref } from 'vue';
import axios from 'axios';
const ss=ref('/src/data/test.json')
const circleData=ref(null)

const test1 = async () => {
  const path='http://localhost:5173' + ss.value + '?t=1782032371436'
  
  const response = await axios.get(path)
  circleData.value = response.data;
  // console.log(circleData.value)
}

const handleChartReady = (chart) => {
  console.log('图表已就绪:', chart)
}

// 处理节点点击
const handleNodeClick = (params) => {
  console.log('点击了节点:', params)
  
}

// 处理数据加载完成
const handleDataLoaded = (data) => {
  console.log('数据加载完成:', data)
}

// 处理错误
const handleError = (error) => {
  console.error('图表错误:', error)
}

</script>