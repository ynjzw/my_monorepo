<template>
    <div class="chart-wrapper">
        <div 
          ref="chartContainer" 
          class="chart-container"
        ></div>
        <div v-if="loading" class="loading">加载中...</div>
        <div v-if="error" class="error">{{ error }}</div>
    </div>
</template>

<script setup>
import { onMounted } from 'vue'; // 1. 引入钩子
import * as echarts from 'echarts';
import { get_base_nodes,get_maslow_needs } from '../api/index';

const props = defineProps({
  data: {
    type: Array,
    default: () => []  // 提供默认值
  }
})
const emit = defineEmits(['chart-ready','data-loaded', 'error', 'node-click']);

// 响应式变量
const chartContainer = ref(null);
const myChart = ref(null);
const seriesData = ref([]);
const error = ref(null);
const loading = ref(false);
onMounted(() => {
  if (!chartContainer.value) return;
  if (myChart.value) {
    myChart.value.dispose();
  }
    // 创建新图表实例
  myChart.value = echarts.init(chartContainer.value);
  var option;
  option = {
      baseOption: {
          timeline: {
              show: true,
              axisType: 'category',
              autoPlay: false,
              playInterval: 1500,
              data: ['x', '二月', '三月']
          },
          title: {
              text: '一月到三月ABC商品销售情况',
              subtext: '2021.5.30'
          },
          // 其他基础配置
      },
      options: [
          {
              title: { text: '一月份统计值' },
              series: [
              {
                type: 'graph',
                layout: 'none',
                symbolSize: 50,
                roam: true,
                label: {
                    show: true
                },
                edgeSymbol: ['circle', 'arrow'],
                edgeSymbolSize: [4, 10],
                edgeLabel: {
                    fontSize: 20
                },
                data: [
                    {
                        name: 'Node 1',
                        x: 300,
                        y: 300
                    },
                    {
                        name: 'Node 2',
                        x: 800,
                        y: 300
                    },
                    {
                        name: 'Node 3',
                        x: 550,
                        y: 100
                    },
                    {
                        name: 'Node 4',
                        x: 550,
                        y: 500
                    }
                ],
                // links: [],
                links: [
                    {
                        source: 0,
                        target: 1,
                        symbolSize: [5, 20],
                        label: {
                            show: true
                        },
                        lineStyle: {
                            width: 5,
                            curveness: 0.2
                        }
                    },
                    {
                        source: 'Node 2',
                        target: 'Node 1',
                        label: {
                            show: true
                        },
                        lineStyle: {
                            curveness: 0.2
                        }
                    },
                    {
                        source: 'Node 1',
                        target: 'Node 3'
                    },
                    {
                        source: 'Node 2',
                        target: 'Node 3'
                    },
                    {
                        source: 'Node 2',
                        target: 'Node 4'
                    },
                    {
                        source: 'Node 1',
                        target: 'Node 4'
                    }
                ],
                lineStyle: {
                    opacity: 0.9,
                    width: 2,
                    curveness: 0
                }
            }
              ]
          },
          {
              title: { text: '二月份统计值' },
              series: [{ data: [53, 78, 99] }]
          },
          {
              title: { text: '三月份统计值' },
              series: [{ data: [94, 80, 66] }]
          }
      ]
  };
  option && myChart.setOption(option);
});
</script>