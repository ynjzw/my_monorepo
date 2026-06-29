<template>
    <div class="container">    
      <div class="charts-wrapper">
        <div class="chart-item">
            <xxx 
                :data="data"
                :link="link"
                @chart-ready="handleChartReady" 
                @error="handleError"
            />
        </div>
      </div>
    </div>
</template>
<script setup>
import { onMounted } from 'vue';
import xxx from '@/components/graph.vue';

const data=ref([])
const link=ref([])

// 处理图表就绪
const handleChartReady = (chart) => {
  // console.log('图表已就绪:', chart)
  // 可以在这里对图表进行额外配置
}

// 处理错误
const handleError = (error) => {
  // console.error('图表错误:', error)
}

onMounted(()=>{
    
})
</script>
<style scoped>
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