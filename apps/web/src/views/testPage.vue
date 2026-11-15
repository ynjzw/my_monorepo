<script setup>
import { onMounted, ref } from 'vue';
import structure from '@/components/structure.vue';
import tree from '@/components/tree.vue';

const old_structure = ref([])
const new_structure = ref([])
const link = ref([])
const isLoading = ref(true)
const colorPalette = [
    '#5470c6', '#fac858', '#ee6666', '#73c0de', '#73cede', 
    '#3ba272', '#fc8452', '#9a60b4', '#ea7ccc','#7ec0de'
];     
// 处理图表就绪
const handleChartReady = (chart) => {
  // console.log('图表已就绪:', chart)
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
    // 并行加载数据    
    for(let i=1;i<4;i++){
      for(let j=Math.pow(10,i-1);j<Math.pow(10,i);j++){
        old_structure.value.push({
          id: `${i}`,
          name: `${i}`,
          x:(i % 10) * 100 + Math.random() * 100,
          y:j*100+Math.random()*10,
          symbolSize: i*10,
          symbol:'circle',
          itemStyle: {
              color: colorPalette[i]
          }
        })
        new_structure.value.push({
          id: `${i}`,
          name: `${i}`,
          symbolSize: i*10,
          symbol:'circle',
          itemStyle: {
              color: colorPalette[i]
          }
        })
        }
      }
    
    // console.log(link.value,new_structure.value,old_structure.value)
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
    <div v-if="isLoading" class="loading">加载数据中...</div>
    <div v-else class="charts-wrapper">
      <div class="chart-item">
        <structure 
          :data="old_structure" 
          :link="link"
          layout="none"
          @chart-ready="handleChartReady" 
          @error="handleError"
        />
      </div>
      <div class="chart-item">
        <structure 
          :data="new_structure" 
          :link="link"
          layout="circular"
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