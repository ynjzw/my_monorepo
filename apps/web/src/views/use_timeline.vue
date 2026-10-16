<template>
  <div class="container">
    <div class="charts-wrapper">
      <div class="chart-item">
        <timeline
          ref="treeRef"
          :title_list="title1"
          :option_list="option"
          @click="handleNodeClick"
          @ready="onChartReady"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import timeline from '@/components/timeline.vue'
import {titleList, optionList} from '@/data/data.js'
import { ref } from 'vue'

const treeRef = ref(null)

// 时间轴标题
const title1 = titleList
const images = ['cell', 'tissue'] // 对应的图片文件名数组

// 每个时间点对应的 option
const option = title1.map((title0, i) => ({
  title: { text: title0 },
  series: optionList[i],
}))

const handleNodeClick = (params) => {
  // console.log('点击节点:', params.data.name)
}

const onChartReady = (chart) => {
  // console.log('图表已准备就绪')
}
</script>

<style scoped>
.container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  text-align: center;
}

.charts-wrapper {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24px;
}

.chart-item {
  min-width: 1000px;
  height: 500px;
  border: 1px solid #ebeef5;
  border-radius: 4px;
  overflow: hidden;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

@media screen and (max-width: 768px) {
  .chart-item {
    min-width: 100%;
    height: 400px;
  }
}
</style>