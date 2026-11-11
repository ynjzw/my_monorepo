<template>
    <div class="workspace">
        <Navbar
            :sidebar-collapsed="sidebarCollapsed"
            @toggle-sidebar="sidebarCollapsed = !sidebarCollapsed"
        />
        <div class="workspace-body">
            <Sidebar :collapsed="sidebarCollapsed" />
            <main class="main-content">
                <div class="page-heading">
                    <div>
                        <p class="eyebrow">供应链管理</p>
                        <h1>供应链关系图</h1>
                        <p class="page-description">查看供应、生产、仓储与分销环节的关联关系</p>
                    </div>
                    <span class="live-badge"><span></span>关系总览</span>
                </div>
                <section class="chart-card" aria-label="供应链关系图">
                    <div class="chart-heading">
                        <div>
                            <h2>供应网络</h2>
                            <p>拖动节点查看网络结构，滚轮缩放图表</p>
                        </div>
                        <span class="node-count">{{ nodes.length }} 个节点</span>
                    </div>
                    <div ref="mapRef" class="map-container"></div>
                </section>
            </main>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import * as echarts from 'echarts'
import Navbar from '../components/Navbar.vue'
import Sidebar from '../components/Sidebar.vue'

const colorPalette = [
    '#5470c6', '#fac858', '#ee6666', '#73cede', '#3ba272',
    '#fc8452', '#9a60b4', '#ea7ccc', '#73c0de', '#7ec0de'
]

const mapRef = ref(null)
const sidebarCollapsed = ref(false)
const nodeNames = ['原料供应', '零部件', '制造中心', '质检中心', '区域仓库', '干线物流', '城市配送', '零售终端']
const nodes = nodeNames.map((name, index) => ({
    id: String(index),
    name,
    symbolSize: 42,
    itemStyle: { color: colorPalette[index % colorPalette.length] }
}))
const links = [
    { source: '0', target: '1' },
    { source: '1', target: '2' },
    { source: '2', target: '3' },
    { source: '3', target: '4' },
    { source: '4', target: '5' },
    { source: '5', target: '6' },
    { source: '6', target: '7' },
    { source: '0', target: '2' },
    { source: '2', target: '4' }
]
let chart = null

const resizeChart = () => chart?.resize()

onMounted(() => {
    chart = echarts.init(mapRef.value)
    chart.setOption({
        tooltip: { trigger: 'item' },
        series: [
            {
                type: 'graph',
                layout: 'force',
                data: nodes,
                links,
                roam: true,
                draggable: true,
                label: { show: true, position: 'right', fontSize: 12 },
                force: {
                    repulsion: 180,
                    edgeLength: 110,
                    gravity: 0.12,
                    friction: 0.1
                },
                lineStyle: { color: 'source', curveness: 0.12, opacity: 0.55 }
            }
        ]
    })
    window.addEventListener('resize', resizeChart)
})

onUnmounted(() => {
    window.removeEventListener('resize', resizeChart)
    chart?.dispose()
    chart = null
})
</script>

<style scoped>
.workspace {
    position: fixed;
    inset: 0;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    background: #f6f8fb;
    color: #172033;
    font-family: Inter, "PingFang SC", "Microsoft YaHei", sans-serif;
}

.workspace-body {
    display: flex;
    flex: 1;
    min-height: 0;
}

.main-content {
    flex: 1;
    min-width: 0;
    overflow: auto;
    padding: 34px 40px;
}

.page-heading {
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
    gap: 20px;
    margin: 0 auto 26px;
    max-width: 1400px;
}

.eyebrow {
    margin: 0 0 8px;
    color: #2563eb;
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 0.08em;
}

.page-heading h1 {
    margin: 0;
    color: #172033;
    font-size: 26px;
    font-weight: 700;
    line-height: 1.3;
}

.page-description {
    margin: 8px 0 0;
    color: #8491a4;
    font-size: 14px;
}

.live-badge,
.node-count {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 7px 12px;
    border: 1px solid #e5eaf1;
    border-radius: 20px;
    background: #fff;
    color: #64748b;
    font-size: 12px;
    white-space: nowrap;
}

.live-badge span {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: #3b82f6;
}

.chart-card {
    max-width: 1400px;
    margin: 0 auto;
    padding: 22px 24px 16px;
    border: 1px solid #e9edf3;
    border-radius: 14px;
    background: #fff;
    box-shadow: 0 4px 18px rgb(15 23 42 / 3%);
}

.chart-heading {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 16px;
}

.chart-heading h2 {
    margin: 0;
    color: #263248;
    font-size: 15px;
    font-weight: 600;
}

.chart-heading p {
    margin: 5px 0 0;
    color: #94a3b8;
    font-size: 12px;
}

.map-container {
    width: 100%;
    height: max(360px, calc(100vh - 285px));
    min-height: 360px;
}

@media (max-width: 700px) {
    .main-content {
        padding: 24px 16px;
    }

    .page-heading h1 {
        font-size: 22px;
    }

    .page-description {
        max-width: 260px;
        line-height: 1.6;
    }

    .chart-card {
        padding: 18px 14px 12px;
    }

    .map-container {
        height: max(360px, calc(100vh - 300px));
    }
}
</style>