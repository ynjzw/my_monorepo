<script setup>
import { onMounted, ref } from 'vue';
import circle from '@/components/circle.vue';
import graph from '@/components/graph.vue';


const rational_data = ref([])
const emotional_data = ref({})
const link = ref([])
const isLoading = ref(true)

// 处理图表就绪
const handleChartReady = (chart) => {
  // console.log('图表已就绪:', chart)
  // 可以在这里对图表进行额外配置
}

// 处理错误
const handleError = (error) => {
  // console.error('图表错误:', error)
}

// 加载数据
const loadData = () => {
  isLoading.value = true
  try {    
    rational_data = [
          {"name": "观察", "value": "观察"},
          {"name": "记忆", "value": "记忆"},
          {"name": "分析", "value": "分析"},
          {"name": "推理", "value": "推理"}
        ];
    link = [
              {"source": "观察", "target": "记忆"},
              {"source": "记忆", "target": "分析"},
              {"source": "分析", "target": "推理"},
              {"source": "推理", "target": "观察"}
            ]
    emotional_data = {
                        "$count": 100,
                        "喜": { "$count": 50 },
                        "怒": { "$count": 50 },
                        "惧": { "$count": 50 },
                        "悲": { "$count": 50 }
                      }
    
  } catch (error) {
    console.error('数据加载失败:', error)
  } finally {
    isLoading.value = false
  }
}

onMounted(async() => {
  await loadData()
})
</script>

<template>
  <div class="container">
    
    <div class="charts-wrapper">
      <div class="chart-item">
        <graph 
          :data="rational_data"
          :link="link" 
          @chart-ready="handleChartReady" 
          @error="handleError"
        />
      </div>
      <div class="chart-item">
        <circle 
          :data="emotional_data" 
          @chart-ready="handleChartReady" 
          @error="handleError"
        />
      </div>
    </div>
  </div>
</template>

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