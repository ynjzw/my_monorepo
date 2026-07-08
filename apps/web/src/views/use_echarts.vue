<template>
    <div class="container">    
      <div class="tab-nav">
        <button 
          v-for="tab in tabs" 
          :key="tab.name"
          @click="currentTab = tab.component"
          :class="{ active: currentTab === tab.component }"
        >
          {{ tab.label }}
        </button>
      </div> 
      <div class="charts-wrapper">
        <div class="chart-item">
          <KeepAlive>
            <component :is="currentTab" :data="data" :link="link"/>
          </KeepAlive>
            
        </div>
      </div>
    </div>
</template>
<script setup>
import { onMounted,ref } from 'vue';
import xxx from '@/components/graph.vue';
import yyy from '@/components/circle.vue';
import zzz from '@/components/tree.vue';

const tabs = [
  { name: '节点图', label: '节点图', component: xxx },
  { name: '圆图', label: '圆图', component: yyy },
  { name: '树图', label: '树图', component: zzz },
]
const currentTab = ref(tabs[0].component)
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
  height: 100%;           /* 占满视口高度 */
  display: flex;
  flex-direction: column;
  align-items: center;     /* 水平居中 */
  justify-content: center; /* 垂直居中 */
  padding: 20px;
  box-sizing: border-box;
}

.charts-wrapper {
  width: 100%;
  max-width: 900px;        /* 限制最大宽度 */
  display: flex;
  justify-content: center;
}

.chart-item {
  width: 100%;
  height: 100%;
  border: 1px solid #ebeef5;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.08);
}

.loading {
  padding: 40px;
  text-align: center;
  font-size: 16px;
  color: #909399;
}

/* 响应式设计 */
@media screen and (max-width: 768px) {
  .chart-item {
    flex: 1 1 100%;
    height: 400px;
  }
}
</style>