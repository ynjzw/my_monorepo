<template>
  <div class="bindNurseToRoom-container">
    <!-- 时间轴-绑定元素 -->
    <div ref="timelineRef" id="visualization" class="timeline-vertical"></div>
  </div>
</template>

<script>
import { onMounted, ref, onBeforeUnmount, nextTick } from 'vue';
import "vis-timeline/styles/vis-timeline-graph2d.min.css";
import { DataSet } from 'vis-data';
import { Timeline } from "vis-timeline";
import moment from 'moment';
import "moment/dist/locale/zh-cn.js";

// 设置moment语言为中文
moment.locale('zh-cn');

export default {
  name: 'VerticalTimeline',
  setup() {
    const timelineRef = ref(null);
    let timeline = null;
    let items = null;
    let groups = null;

    // 初始化数据 - 护士排班和医疗事件
    const initData = () => {
      // 当前日期
      const today = moment().format('YYYY-MM-DD');
      
      // 创建items数据集
      items = new DataSet([
        // 护士排班 - 早班
        {
          id: 1,
          content: '早班护士 张三',
          start: moment(`${today} 07:00`).toDate(),
          end: moment(`${today} 15:00`).toDate(),
          group: 1,
          className: 'nurse-shift morning-shift',
          title: '早班护士: 张三\n工作时间: 07:00 - 15:00'
        },
        // 护士排班 - 晚班
        {
          id: 2,
          content: '晚班护士 李四',
          start: moment(`${today} 15:00`).toDate(),
          end: moment(`${today} 23:00`).toDate(),
          group: 1,
          className: 'nurse-shift evening-shift',
          title: '晚班护士: 李四\n工作时间: 15:00 - 23:00'
        },
        // 护士排班 - 夜班
        {
          id: 3,
          content: '夜班护士 王五',
          start: moment(`${today} 23:00`).toDate(),
          end: moment(`${today} 23:59:59`).toDate(),
          group: 1,
          className: 'nurse-shift night-shift',
          title: '夜班护士: 王五\n工作时间: 23:00 - 24:00'
        },
        // 护士排班 - 凌晨班
        {
          id: 4,
          content: '凌晨护士 赵六',
          start: moment(`${today} 00:00`).toDate(),
          end: moment(`${today} 07:00`).toDate(),
          group: 1,
          className: 'nurse-shift midnight-shift',
          title: '凌晨护士: 赵六\n工作时间: 00:00 - 07:00'
        },
        // 医疗事件 - 查房
        {
          id: 5,
          content: '主任查房',
          start: moment(`${today} 09:00`).toDate(),
          end: moment(`${today} 10:30`).toDate(),
          group: 2,
          className: 'medical-event rounds-event',
          title: '主任查房\n时间: 09:00 - 10:30'
        },
        // 医疗事件 - 用药
        {
          id: 6,
          content: '用药时间 A',
          start: moment(`${today} 08:00`).toDate(),
          end: moment(`${today} 08:15`).toDate(),
          group: 2,
          className: 'medical-event medication-event',
          title: '早晨用药\n时间: 08:00 - 08:15'
        },
        // 医疗事件 - 用药
        {
          id: 7,
          content: '用药时间 B',
          start: moment(`${today} 12:00`).toDate(),
          end: moment(`${today} 12:15`).toDate(),
          group: 2,
          className: 'medical-event medication-event',
          title: '中午用药\n时间: 12:00 - 12:15'
        },
        // 医疗事件 - 用药
        {
          id: 8,
          content: '用药时间 C',
          start: moment(`${today} 18:00`).toDate(),
          end: moment(`${today} 18:15`).toDate(),
          group: 2,
          className: 'medical-event medication-event',
          title: '晚上用药\n时间: 18:00 - 18:15'
        },
        // 交接班事件
        {
          id: 9,
          content: '交接班',
          start: moment(`${today} 07:00`).toDate(),
          end: moment(`${today} 07:30`).toDate(),
          group: 2,
          className: 'handover-event',
          title: '早班交接班\n时间: 07:00 - 07:30'
        },
        {
          id: 10,
          content: '交接班',
          start: moment(`${today} 15:00`).toDate(),
          end: moment(`${today} 15:30`).toDate(),
          group: 2,
          className: 'handover-event',
          title: '晚班交接班\n时间: 15:00 - 15:30'
        },
        {
          id: 11,
          content: '交接班',
          start: moment(`${today} 23:00`).toDate(),
          end: moment(`${today} 23:30`).toDate(),
          group: 2,
          className: 'handover-event',
          title: '夜班交接班\n时间: 23:00 - 23:30'
        },
        // 病房状态 - 清洁
        {
          id: 12,
          content: '病房清洁',
          start: moment(`${today} 10:00`).toDate(),
          end: moment(`${today} 11:00`).toDate(),
          group: 3,
          className: 'room-status cleaning-event',
          title: '病房清洁时间\n10:00 - 11:00'
        },
        // 病房状态 - 消毒
        {
          id: 13,
          content: '病房消毒',
          start: moment(`${today} 14:00`).toDate(),
          end: moment(`${today} 15:00`).toDate(),
          group: 3,
          className: 'room-status disinfection-event',
          title: '病房消毒时间\n14:00 - 15:00'
        },
        // 病房状态 - 探视时间
        {
          id: 14,
          content: '探视时间',
          start: moment(`${today} 15:30`).toDate(),
          end: moment(`${today} 16:30`).toDate(),
          group: 3,
          className: 'room-status visiting-event',
          title: '家属探视时间\n15:30 - 16:30'
        }
      ]);

      // 创建分组
      groups = new DataSet([
        { 
          id: 1, 
          content: '👩‍⚕️ 护士排班', 
          className: 'group-nurse',
          title: '护士值班安排'
        },
        { 
          id: 2, 
          content: '🏥 医疗事件', 
          className: 'group-events',
          title: '查房、用药等医疗活动'
        },
        { 
          id: 3, 
          content: '🛏️ 病房状态', 
          className: 'group-room',
          title: '病房清洁、消毒、探视'
        }
      ]);
    };

    // 获取当前日期
    const getTodayRange = () => {
      const today = moment().format('YYYY-MM-DD');
      return {
        start: moment(today).startOf('day').toDate(),      // 今天 00:00:00
        end: moment(today).add(1, 'days').startOf('day').toDate()  // 明天 00:00:00 (24小时)
      };
    };

    // 初始化timeline
    const initTimeline = () => {
      if (!timelineRef.value) return;

      // 初始化数据
      initData();

      // 获取今天的时间范围
      const todayRange = getTodayRange();

      // 配置选项 - 关键部分：设置垂直时间轴和24小时范围
      const options = {
        // 垂直模式配置 - 这是实现纵坐标的关键！
        orientation: {
          axis: 'both',      // 左右两侧都显示时间轴
          item: 'top'        // 项目从顶部开始显示
        },
        
        // 设置时间范围为24小时 (今天00:00到明天00:00)
        start: todayRange.start,
        end: todayRange.end,
        
        // 最小/最大缩放范围（允许查看前后一天）
        min: moment(todayRange.start).subtract(1, 'days').toDate(),
        max: moment(todayRange.end).add(1, 'days').toDate(),
        
        // 分组排序
        groupOrder: 'id',
        
        // 滚动设置
        verticalScroll: true,    // 允许垂直滚动
        horizontalScroll: true,  // 允许水平滚动
        
        // 缩放设置
        zoomable: true,
        zoomMin: 1000 * 60 * 60 * 2,      // 最小缩放：2小时
        zoomMax: 1000 * 60 * 60 * 48,      // 最大缩放：48小时
        
        // 时间轴格式设置 - 显示24小时制
        format: {
          minorLabels: {
            millisecond: 'HH:mm:ss.SSS',
            second: 'HH:mm:ss',
            minute: 'HH:mm',
            hour: 'HH:mm'
          },
          majorLabels: {
            hour: 'MM-DD HH:00'
          }
        },
        
        // 时间轴刻度设置
        timeAxis: {
          scale: 'hour',        // 以小时为基本刻度
          step: 2                // 每2小时显示一个主刻度
        },
        
        // 堆叠模式
        stack: true,
        
        // 显示当前时间线
        showCurrentTime: true,
        
        // 当前时间线样式
        currentTimeTick: {
          width: '2px',
          color: '#ff4081'
        },
        
        // 显示自定义时间线
        showCustomTime: true,
        
        // 可编辑设置
        editable: {
          add: false,
          remove: false,
          updateGroup: false,
          updateTime: true,      // 允许拖拽调整时间
          overrideItems: false
        },
        
        // 分组标签位置
        groupLabels: {
          left: true,
          right: false
        },
        
        // 分组高度模式
        groupHeightMode: 'auto',
        
        // 使用moment处理时间
        moment: function(date) {
          return moment(date);
        },
        
        // 工具提示
        tooltip: {
          followMouse: true,
          overflowMethod: 'cap',
          delay: 300
        },
        
        // 项目模板
        template: function(item, element, data) {
          if (item.content) {
            return item.content;
          }
          return '';
        },
        
        // 鼠标悬停提示
        tooltipOnItem: true,
        
        // 点击选中
        selectable: true,
        
        // 多选
        multiselect: false,
        
        // 快照
        snap: null,
        
        // 垂直轴标签对齐
        align: 'center',
        
        // 背景区域
        backgroundAreas: [
          {
            id: 'night',
            start: moment(todayRange.start).hour(0).toDate(),
            end: moment(todayRange.start).hour(6).toDate(),
            className: 'night-background',
            title: '深夜时段 (00:00-06:00)'
          },
          {
            id: 'morning',
            start: moment(todayRange.start).hour(6).toDate(),
            end: moment(todayRange.start).hour(12).toDate(),
            className: 'morning-background',
            title: '上午时段 (06:00-12:00)'
          },
          {
            id: 'afternoon',
            start: moment(todayRange.start).hour(12).toDate(),
            end: moment(todayRange.start).hour(18).toDate(),
            className: 'afternoon-background',
            title: '下午时段 (12:00-18:00)'
          },
          {
            id: 'evening',
            start: moment(todayRange.start).hour(18).toDate(),
            end: moment(todayRange.start).hour(24).toDate(),
            className: 'evening-background',
            title: '晚上时段 (18:00-24:00)'
          }
        ]
      };

      // 创建timeline实例
      timeline = new Timeline(timelineRef.value, items, groups, options);

      // 设置当前时间线
      timeline.setCurrentTime(moment().toDate());

      // 添加自定义时间线（显示当前选中时间）
      const now = moment();
      const customTimeId = timeline.addCustomTime(
        now.toDate(),
        'selected-time'
      );
      
      // 设置自定义时间线标题
      timeline.setCustomTimeTitle(`当前时间: ${now.format('HH:mm')}`, customTimeId);

      // 事件监听
      
      // 选择事件
      timeline.on('select', (properties) => {
        const selectedItems = properties.items;
        if (selectedItems && selectedItems.length > 0) {
          const item = items.get(selectedItems[0]);
          // console.log('选中项目:', item);
          
          // 可以在这里添加选中效果
          document.querySelectorAll('.vis-item').forEach(el => {
            el.classList.remove('selected-item');
          });
          
          setTimeout(() => {
            const selectedEl = document.querySelector(`[data-id="${selectedItems[0]}"]`);
            if (selectedEl) {
              selectedEl.classList.add('selected-item');
            }
          }, 0);
        }
      });

      // 时间改变事件
      timeline.on('timechange', (properties) => {
        // console.log('时间改变:', moment(properties.time).format('HH:mm'));
      });

      // 范围改变事件
      timeline.on('rangechange', (properties) => {
        const start = moment(properties.start).format('HH:mm');
        const end = moment(properties.end).format('HH:mm');
        // console.log(`当前视图范围: ${start} - ${end}`);
      });

      // 双击事件
      timeline.on('doubleClick', (properties) => {
        if (properties.item) {
          const item = items.get(properties.item);
          alert(`事件详情:\n${item.title || item.content}`);
        } else {
          const time = moment(properties.time).format('HH:mm');
          alert(`点击时间点: ${time}`);
        }
      });

      // 项目悬停事件
      timeline.on('itemover', (properties) => {
        const item = items.get(properties.item);
        // console.log('悬停项目:', item.content);
      });

      // 初始移动到当前时间
      setTimeout(() => {
        if (timeline) {
          const now = moment();
          timeline.moveTo(now.toDate());
        }
      }, 100);
    };

    // 公共方法：跳转到指定时间
    const moveToTime = (timeStr) => {
      if (timeline) {
        const time = moment(timeStr).toDate();
        timeline.moveTo(time);
      }
    };

    // 公共方法：跳转到当前时间
    const moveToNow = () => {
      if (timeline) {
        timeline.moveTo(moment().toDate());
      }
    };

    // 公共方法：获取当前可见范围
    const getVisibleRange = () => {
      if (timeline) {
        const range = timeline.getWindow();
        return {
          start: moment(range.start).format('HH:mm'),
          end: moment(range.end).format('HH:mm'),
          startFull: moment(range.start).format('YYYY-MM-DD HH:mm:ss'),
          endFull: moment(range.end).format('YYYY-MM-DD HH:mm:ss')
        };
      }
      return null;
    };

    // 公共方法：缩放时间轴
    const zoomIn = () => {
      if (timeline) {
        const range = timeline.getWindow();
        const center = moment(range.start).add(moment(range.end).diff(moment(range.start)) / 2);
        const newStart = moment(center).subtract(2, 'hours').toDate();
        const newEnd = moment(center).add(2, 'hours').toDate();
        timeline.setWindow(newStart, newEnd);
      }
    };

    const zoomOut = () => {
      if (timeline) {
        const range = timeline.getWindow();
        const center = moment(range.start).add(moment(range.end).diff(moment(range.start)) / 2);
        const newStart = moment(center).subtract(8, 'hours').toDate();
        const newEnd = moment(center).add(8, 'hours').toDate();
        timeline.setWindow(newStart, newEnd);
      }
    };

    // 生命周期钩子
    onMounted(() => {
      nextTick(() => {
        initTimeline();
      });
    });

    onBeforeUnmount(() => {
      if (timeline) {
        timeline.destroy();
        timeline = null;
      }
    });

    // 暴露公共方法给模板使用
    return {
      timelineRef,
      moveToTime,
      moveToNow,
      getVisibleRange,
      zoomIn,
      zoomOut
    };
  }
}
</script>

<style scoped>
.bindNurseToRoom-container {
  width: 1200px;
  height: 400px;
  position: relative;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  background-color: #fff;
}

.timeline-vertical {
  width: 100%;
  height: 100%;
}

/* 控制按钮容器 - 可以放在组件外部使用 */
.timeline-controls {
  position: absolute;
  top: 10px;
  right: 10px;
  z-index: 100;
  display: flex;
  gap: 8px;
}

.control-btn {
  padding: 6px 12px;
  background: #fff;
  border: 1px solid #2196F3;
  border-radius: 4px;
  color: #2196F3;
  cursor: pointer;
  font-size: 12px;
  transition: all 0.2s;
}

.control-btn:hover {
  background: #2196F3;
  color: #fff;
}
</style>

<style>
/* 全局样式 - 不加scoped以确保覆盖vis-timeline的默认样式 */

/* 时间轴容器 */
.vis-timeline {
  border: none !important;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
}

/* 时间轴背景 */
.vis-panel.vis-background.vis-vertical {
  background-color: #ffffff;
}

/* 时间轴刻度区域 */
.vis-time-axis {
  background-color: #f8f9fa;
  border-bottom: 1px solid #e0e0e0;
}

.vis-time-axis .vis-text {
  color: #495057;
  font-size: 12px;
  font-weight: 500;
  padding: 4px;
}

.vis-time-axis .vis-major {
  font-weight: 600;
  color: #212529;
}

/* 项目样式 - 护士排班 */
.nurse-shift {
  border-radius: 4px !important;
  border-left-width: 4px !important;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1) !important;
  opacity: 0.9;
  transition: all 0.2s;
}

.nurse-shift:hover {
  opacity: 1;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2) !important;
  transform: translateY(-1px);
}

.morning-shift {
  background-color: rgba(76, 175, 80, 0.15) !important;
  border-color: #4CAF50 !important;
}

.evening-shift {
  background-color: rgba(255, 152, 0, 0.15) !important;
  border-color: #FF9800 !important;
}

.night-shift {
  background-color: rgba(33, 33, 33, 0.1) !important;
  border-color: #212121 !important;
}

.midnight-shift {
  background-color: rgba(63, 81, 181, 0.1) !important;
  border-color: #3F51B5 !important;
}

/* 医疗事件样式 */
.medical-event {
  border-radius: 4px !important;
  border-left-width: 4px !important;
}

.rounds-event {
  background-color: rgba(33, 150, 243, 0.12) !important;
  border-color: #2196F3 !important;
}

.medication-event {
  background-color: rgba(156, 39, 176, 0.12) !important;
  border-color: #9C27B0 !important;
}

.handover-event {
  background-color: rgba(255, 87, 34, 0.12) !important;
  border-color: #FF5722 !important;
}

/* 病房状态样式 */
.room-status {
  border-radius: 4px !important;
  border-left-width: 4px !important;
}

.cleaning-event {
  background-color: rgba(0, 188, 212, 0.12) !important;
  border-color: #00BCD4 !important;
}

.disinfection-event {
  background-color: rgba(233, 30, 99, 0.12) !important;
  border-color: #E91E63 !important;
}

.visiting-event {
  background-color: rgba(76, 175, 80, 0.12) !important;
  border-color: #8BC34A !important;
}

/* 分组样式 */
.group-nurse .vis-label {
  background-color: #E8F5E9 !important;
  font-weight: 600;
  color: #2E7D32;
}

.group-events .vis-label {
  background-color: #E3F2FD !important;
  font-weight: 600;
  color: #1565C0;
}

.group-room .vis-label {
  background-color: #FFF3E0 !important;
  font-weight: 600;
  color: #E65100;
}

/* 时间段背景色 */
.night-background {
  background-color: rgba(33, 33, 33, 0.05) !important;
}

.morning-background {
  background-color: rgba(255, 193, 7, 0.03) !important;
}

.afternoon-background {
  background-color: rgba(33, 150, 243, 0.03) !important;
}

.evening-background {
  background-color: rgba(156, 39, 176, 0.03) !important;
}

/* 当前时间线 */
.vis-current-time {
  background-color: #FF4081 !important;
  width: 2px !important;
  z-index: 3;
}

/* 自定义时间线 */
.vis-custom-time {
  background-color: #7C4DFF !important;
  width: 2px !important;
  z-index: 3;
}

/* 选中项目 */
.vis-item.selected-item {
  box-shadow: 0 0 0 3px rgba(33, 150, 243, 0.5) !important;
  z-index: 10 !important;
}

/* 工具提示 */
.vis-tooltip {
  background-color: rgba(33, 33, 33, 0.9) !important;
  color: white !important;
  padding: 8px 12px !important;
  border-radius: 4px !important;
  font-size: 12px !important;
  line-height: 1.5 !important;
  white-space: pre-line !important;
  z-index: 9999 !important;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3) !important;
  border: none !important;
  font-family: monospace !important;
}

/* 左侧时间轴 */
.vis-panel.vis-left {
  border-right: 1px solid #e0e0e0 !important;
  background-color: #fafafa;
}

.vis-panel.vis-right {
  border-left: 1px solid #e0e0e0 !important;
  background-color: #fafafa;
}

/* 滚动条样式 */
.vis-panel.vis-center::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

.vis-panel.vis-center::-webkit-scrollbar-track {
  background: #f1f1f1;
}

.vis-panel.vis-center::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 4px;
}

.vis-panel.vis-center::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}

/* 项目内容 */
.vis-item .vis-item-content {
  padding: 6px 10px !important;
  font-size: 12px !important;
  font-weight: 500 !important;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* 分组标签 */
.vis-label {
  font-size: 14px !important;
  padding: 10px !important;
  border-bottom: 1px solid #e0e0e0 !important;
  user-select: none;
  cursor: pointer;
}

.vis-label:hover {
  background-color: #f5f5f5 !important;
}

/* 网格线 */
.vis-grid.vis-minor {
  border-color: #f0f0f0 !important;
}

.vis-grid.vis-major {
  border-color: #e0e0e0 !important;
}
</style>