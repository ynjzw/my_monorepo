<template>
  
    <input v-model="ss"/>

    <button @click="test1()" >ss</button><br>
    <div class="tab-nav">
      <button 
        v-for="tab in colorN" 
        @click="active(tab)"
        :style="{ backgroundColor: tab }"
      >
        {{ tab }}
      </button>
    </div> 

    <kkk :data="circleData"
      :file_name="tt"
      :color="color"
      ref="chartRef"
      theme="auto"
      height="400px"
      @chart-ready="handleChartReady"
      @node-click="handleNodeClick"
      @data-loaded="handleDataLoaded"
      @error="handleError"
      >
    </kkk>

</template>
<script setup>
import CirclePackingChart from '../components/CirclePackingChart.vue';
import kkk from '../components/circle.vue';
import { onMounted,ref } from 'vue';
import axios from 'axios';
const ss=ref('/src/data/test.json')
const tt=ref('')
const color=ref('')
const xx=ref({})
const circleData=ref(null)
const colorN=['#5470c6', '#fac858', '#ee6666', '#73c0de', '#3ba272', '#fc8452', '#9a60b4', '#ea7ccc']

const test1 = async () => {
  const path='http://localhost:5173' + ss.value + '?t=1782032371436'
  tt.value = ss.value.split('/').pop().split('.')[0];
  const response = await axios.get(path)
  circleData.value = response.data;
  
  // console.log(circleData.value)
}
onMounted(()=>{
  for (let j = 1; j <= 400; j++) {
      xx.value[`${j}`]={"$count":10}
  }
  circleData.value=xx.value
})
const active=(tab)=>{
  // console.log(tab)
  color.value=tab
}

const handleChartReady = (chart) => {
  // console.log('图表已就绪:', chart)
}

// 处理节点点击
const handleNodeClick = (params) => {
  // console.log('点击了节点:', params)
  
}

// 处理数据加载完成
const handleDataLoaded = (data) => {
  // console.log('数据加载完成:', data)
}

// 处理错误
const handleError = (error) => {
  console.error('图表错误:', error)
}

</script>