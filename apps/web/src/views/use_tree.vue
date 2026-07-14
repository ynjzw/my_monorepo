<template>
  
  <div class="container">    
      <div class="charts-wrapper">
        <div class="chart-item">
            <TreeChart 
                ref="treeRef"
                :data="myTreeData"
                height="400px"
                theme="auto"
                @click="handleNodeClick"
                @ready="onChartReady"
            />
        </div>
      </div>
    </div>
</template>

<script setup>
import TreeChart from '@/components/tree.vue'
import { ref } from 'vue'

const treeRef = ref(null)

const myTreeData = {
  name: '我',
  symbol:'image:///src/images/supply_chain/erp.png?t=*',
  value:100,
  symbolSize: 100,
  children: [
    { name: '爸爸', value: 10 , children: [
      { name: '爷爷', value: 10 },
      { name: '奶奶', value: 10 }
    ]},
    { name: '妈妈', value: 10, children: [
      { name: '外公', value: 10 },
      { name: '外婆', value: 10 }
    ]}
  ]
}

const customOptions = {
  title: { text: '血缘关系' },
  series: [{
    symbolSize: 12,
    label: { fontSize: 14 }
  }]
}

const handleNodeClick = (params) => {
  // console.log('点击节点:', params.data.name)
}

const onChartReady = (chart) => {
  // console.log('图表已准备就绪')
}
</script>
<style>
.container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  text-align: center;
}

.loading {
  padding: 40px;
  text-align: center;
  font-size: 16px;
  color: #909399;
}

.charts-wrapper {
  display: grid;
  grid-template-columns: repeat(2, 1fr); /* 两列等宽，完美并列 */
  gap: 24px;
}

.chart-item {
  flex: 1 1 calc(50% - 10px); /* 计算宽度，减去gap的一半 */
  min-width: 500px;
  height: 500px;
  border: 1px solid #ebeef5;
  border-radius: 4px;
  overflow: hidden;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

/* 响应式设计 */
@media screen and (max-width: 768px) {
  .chart-item {
    flex: 1 1 100%;
    height: 400px;
  }
}
</style>