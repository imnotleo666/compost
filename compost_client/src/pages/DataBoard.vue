<template>
  <div class="dashboard">
    <!-- 柱状图 -->
    <div ref="barChart" class="chart-item"></div>

    <!-- 折线图 -->
    <div ref="lineChart" class="chart-item"></div>

    <!-- 饼图1-活动数量比例 -->
    <div ref="pieChart1" class="chart-item"></div>

    <!-- 饼图2-姓名数量分布 -->
    <div ref="pieChart2" class="chart-item"></div>
  </div>
</template>

<script setup>
import {onBeforeUnmount, onMounted, ref} from 'vue'
import * as echarts from 'echarts'
import http from '@/api/index'


// 图表容器引用
const barChart = ref(null)
const lineChart = ref(null)
const pieChart1 = ref(null)
const pieChart2 = ref(null)
let barInstance, lineInstance, pieInstance1, pieInstance2
// 初始化图表配置
const initCharts = async () => {
  let datas = await http.getAllData()
  console.log(datas)
  // 柱状图配置
  const barOption = {
    title: {text: '用户操作统计', left: 'center'},
    xAxis: {
      type: 'category',
      data: datas.user_count.map(item => item.name),
      axisLabel: {rotate: 45}
    },
    yAxis: {type: 'value'},
    series: [{
      data: datas.user_count.map(item => item.total),
      type: 'bar',
      itemStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          {offset: 0, color: '#ec9c4c'},
          {offset: 1, color: '#f06b18'}
        ])
      }
    }
    ]
  }

  // 折线图配置
  const lineOption = {
    title: {text: '按日期统计操作', left: 'center'},
    xAxis: {
      type: 'category',
      data: datas.daily_counts.map(item => item.date),
      axisLabel: {rotate: 45}
    },
    yAxis: {type: 'value'},
    series: [{
      data: datas.daily_counts.map(item => item.count),
      type: 'line',
      smooth: true,
      areaStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          {offset: 0, color: 'rgba(0, 128, 255, 0.3)'},
          {offset: 1, color: 'rgba(0, 128, 255, 0)'}
        ])
      }
    }]
  }

  // 饼图1配置
  const pieOption1 = {
    title: {text: '按操作类型统计', left: 'center'},
    tooltip: {trigger: 'item'},
    series: [{
      type: 'pie',
      radius: ['35%', '55%'], // 环形效果
      data: datas.action_counts.map(item => {
        return {
          name: item.action ? item.action : "其他操作",
          value: item.count
        }
      }),
      label: {formatter: '{b}: {d}%'}
    }]
  }

  // 饼图2配置
  const pieOption2 = {
    title: {text: '操作表统计', left: 'center'},
    tooltip: {trigger: 'item'},
    //鼠标放上去，显示饼图的name和value
    label: {
      show: true,
      formatter: '{b}: {d}%'
    },
    series: [{
      type: 'pie',

      data: datas.table_counts.map((item) => ({
        name: item.tables,
        value: item.count
      })),
      labelLine: {show: true, length: 20},
      emphasis: {label: {show: true, fontSize: 16}}
    }]
  }

  // 初始化实例
  barInstance = echarts.init(barChart.value)
  lineInstance = echarts.init(lineChart.value)
  pieInstance1 = echarts.init(pieChart1.value)
  pieInstance2 = echarts.init(pieChart2.value)

  // 设置配置项
  barInstance.setOption(barOption)
  lineInstance.setOption(lineOption)
  pieInstance1.setOption(pieOption1)
  pieInstance2.setOption(pieOption2)
}

// 生命周期管理
onMounted(() => {
  initCharts()
  window.addEventListener('resize', () => {
    barInstance.resize()
    lineInstance.resize()
    pieInstance1.resize()
    pieInstance2.resize()
  })
})

onBeforeUnmount(() => {
  [barInstance, lineInstance, pieInstance1, pieInstance2].forEach(instance => {
    instance?.dispose()
  })
})
</script>

<style scoped>
.dashboard {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
  padding: 20px;
}

.chart-item {
  height: 400px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  padding: 15px;
}
</style>