<template>
  <div class="map">
    <div ref="mapRef" class="map-container"></div>
  </div>
</template>
<script setup>
import { ref, onMounted, onUnmounted, nextTick } from 'vue';
import * as echarts from 'echarts';

// ... 颜色、常量配置保持不变 ...
const colorPalette = [
  '#5470c6', '#fac858', '#ee6666', '#73c0de', '#73cede',
  '#3ba272', '#fc8452', '#9a60b4', '#ea7ccc', '#7ec0de'
];

const mapRef = ref(null);
let chart = null;
let intervalId = null;
let growthFactor = 0;
const change = 1; // 初始增量为0，后续通过定时器更新
const size = [50, 10];
const diff = ['xxx', 'yyy', 'zzz', 'xzy'];
// 预生成节点和连线（只生成一次）
const generateStaticData = () => {
  const nodes = [];

  // 生成节点
  for (let j = 1; j <= 2; j++) {
    for (let i = 1; i <= Math.pow(10, j); i++) {
      // ★ 核心改动：节点大小 = 基础大小 + change（随时间递增）
      const baseSize = size[j - 1] || 10;
      nodes.push({
        id: `${j * 100 + i}`,
        name: diff[j - 1],
        x: (i % 10) * 100 + Math.random() * 100,
        y: j * 100 + Math.random() * (i % 10) * 10,
        value: diff[j - 1] + ':' + (Math.random() + j * 10).toFixed(2),
        symbolSize: baseSize + change, // ✅ 关键改动
        symbol: 'circle',
        itemStyle: { color: colorPalette[i % 10] }
      });
    }
  }

  // 中心节点
  nodes.push({
    id: '1001',
    name: '国家',
    x: 500,
    y: -200,
    value: '国家',
    symbolSize: 101 + change, // ✅ 也同步变大
    symbol: 'circle',
    itemStyle: { color: 'purple' }
  });

  // 生成连线（保持不变）
  const links = [];
  for (let i = 0; i < Math.pow(10, 2); i++) {
    links.push({
      source: `${200 + i}`,
      target: `${100 + (i % 10)}`,
      symbol: ['none', 'arrow'],
      label: { show: false, fontSize: 20 },
      lineStyle: { width: 1, color: colorPalette[i % 10] }
    });
    links.push({
      source: '1001',
      target: `${200 + i}`,
      symbol: ['none', 'arrow'],
      label: { show: false, fontSize: 20 },
      lineStyle: { width: 1, curveness: 0.2 }
    });
  }
  for (let i = 1; i <= 10; i++) {
    links.push({
      source: `${200 + i * 10}`,
      target: '110',
      symbol: ['none', 'arrow'],
      lineStyle: { width: 2, color: colorPalette[0] }
    });
  }
  for (let i = 0; i < 10; i++) {
    links.push({
      source: nodes[i].id,
      target: '1001',
      symbol: ['none', 'arrow'],
      symbolSize: 20,
      label: { show: false, fontSize: 20, color: nodes[i].itemStyle.color },
      lineStyle: { color: nodes[i].itemStyle.color, width: 5, curveness: 0.2, type: 'dotted' }
    });
    links.push({
      source: '1001',
      target: nodes[i].id,
      symbol: ['none', 'arrow'],
      symbolSize: 20,
      label: { show: false, fontSize: 20, color: nodes[i].itemStyle.color },
      lineStyle: { color: nodes[i].itemStyle.color, width: 5, curveness: 0.2, type: 'dashed' }
    });
  }
  return { nodes, links };
};

// 更新节点大小（增量更新）
const updateNodeSizes = (factor) => {
  if (!chart) return;

  const option = chart.getOption();
  const series = option.series || [];
  if (series.length === 0) return;

  const currentNodes = series[0].data || [];
  // ★ 只更新每个节点的 symbolSize
  const updatedNodes = currentNodes.map((node, index) => {
    // 根据节点类型计算新大小
    const isCenter = node.id === '1001';
    const baseSize = isCenter ? 101 : (index < 100 ? 50 : 10);
    return {
      ...node,
      symbolSize: baseSize + factor,
    };
  });

  
};
onMounted(async () => {
  await nextTick();
  chart = echarts.init(mapRef.value);

  // 首次渲染完整数据
  const { nodes, links } = generateStaticData();
  chart.setOption({
    title: { text: 'ttt', textStyle: { color: 'pink' } },
    animation: true,
    animationDuration: 5000,
    animationEasing: 'cubicOut',
    series: [{
      type: 'graph',
      layout: 'none',
      data: nodes,
      links:links,
      roam: true,
      draggable: true,
      label: { show: false, position: 'bottom', fontSize: 12 },
      force: {
        repulsion: 100,
        edgeLength: 150,
        gravity: 0.3,
        friction: 0.1
      }
    }]
  });

});

onUnmounted(() => {
  if (intervalId) clearInterval(intervalId);
  if (chart) { chart.dispose(); chart = null; }
});
</script>
<style scoped>
.map {
  width: 1000px;
  height: 600px;
}
.map-container {
  width: 1000px;
  height: 600px;
}
</style>