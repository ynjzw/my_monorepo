<template>
    <div class="container">    
      <div class="charts-wrapper">
        <div class="chart-item">
            <xxx 
                :data="data"
                :link="link"
                :layout="layout"
                @chart-ready="handleChartReady" 
                @error="handleError"
            ></xxx>
        </div>
      </div>
    </div>
</template>
<script setup>
import { onMounted,ref } from 'vue';
import xxx from '@/components/graph.vue';
import { get_supply_chain,getLink ,population_structure,get_new_structure} from '../api/simple_api';

const data=ref([])
const link=ref([])
const layout=ref('force')
// 处理图表就绪
const handleChartReady = (chart) => {
  // console.log('图表已就绪:', chart)
  // 可以在这里对图表进行额外配置
}

// 处理错误
const handleError = (error) => {
  // console.error('图表错误:', error)
}

onMounted(async()=>{
    data.value=await get_supply_chain()
    // console.log("hhh:"+data.value)
})
</script>
<style scoped>
.container {
  width: 100%;
  height: 100%;           /* 占满视口高度 */
  display: flex;
  flex-direction: column;
  align-items: center;     /* 水平居中 */
  justify-content: center; /* 垂直居中 */
  padding: 20px;
  box-sizing: border-box;
}

.loading {
  padding: 40px;
  text-align: center;
  font-size: 16px;
  color: #909399;
}

.charts-wrapper {
  width: 100%;
  max-width: 1000px;        /* 限制最大宽度 */
  display: flex;
  justify-content: center;
}

.chart-item {
  width: 50%;
  height: 50%;
  border: 1px solid #ebeef5;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.08);
}

/* 响应式设计 */
@media screen and (max-width: 768px) {
  .chart-item {
    flex: 1 1 100%;
    height: 400px;
  }
}
</style>