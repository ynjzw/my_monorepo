<script setup>
import { onMounted, ref } from 'vue';
import rational from '@/components/rational.vue';
import emotional from '@/components/emotional.vue';


const rational_data = ref([])
const emotional_data = ref({})
const link = ref([])
const isLoading = ref(true)

// 处理图表就绪
const handleChartReady = (chart) => {
  console.log('图表已就绪:', chart)
  // 可以在这里对图表进行额外配置
}

// 处理错误
const handleError = (error) => {
  console.error('图表错误:', error)
}

// 加载数据
const loadData = async () => {
  isLoading.value = true
  try {
    
    emotional_data.value = {
                              "$count": 200,
                              "快乐": { "$count": 40 },
                              "愤怒": { "$count": 35 },
                              "恐惧": { "$count": 35 },
                              "悲伤": { "$count": 40 }
                            };
    rational_data.value = [
                            {"name": "原因", "value": "原因", "symbolSize": 20,
                              itemStyle: {
                                color: 'green'
                              }
                            },
                            {"name": "手段", "value": "手段", "symbolSize": 20},
                            {"name": "目的", "value": "目的", "symbolSize": 20},
                            {"name": "问题", "value": "问题", "symbolSize": 20},
                            {"name": "效果", "value": "效果", "symbolSize": 20}
                          ]
    link.value = [
                  {"source": "原因", "target": "手段"},
                  {"source": "原因", "target": "目的"},
                  {"source": "原因", "target": "问题"},
                  {"source": "原因", "target": "效果"},
                  {"source": "手段", "target": "目的"},
                  {"source": "手段", "target": "问题"},
                  {"source": "手段", "target": "效果"},
                  {"source": "目的", "target": "问题"},
                ]
    //console.log(linkData)
  } catch (error) {
    console.error('数据加载失败:', error)
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  loadData()
})
</script>

<template>
  <div class="container">
    
    <div class="charts-wrapper">
      <div class="chart-item">
        <rational 
          :data="rational_data" 
          :link="link"
          @chart-ready="handleChartReady" 
          @error="handleError"
        />
      </div>
      <div class="chart-item">
        <emotional 
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