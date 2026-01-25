<template>
  <div class="dashboard-container">
    <el-row :gutter="20" class="panel-group">
      <el-col :xs="12" :sm="12" :lg="6" class="card-panel-col">
        <div class="card-panel">
          <div class="card-panel-icon-wrapper icon-people">
            <i class="el-icon-user-solid card-panel-icon"></i>
          </div>
          <div class="card-panel-description">
            <div class="card-panel-text">用户总数</div>
            <div class="card-panel-num">{{ panelData.users }}</div>
          </div>
        </div>
      </el-col>
      <el-col :xs="12" :sm="12" :lg="6" class="card-panel-col">
        <div class="card-panel">
          <div class="card-panel-icon-wrapper icon-message">
            <i class="el-icon-reading card-panel-icon"></i>
          </div>
          <div class="card-panel-description">
            <div class="card-panel-text">课程总数</div>
            <div class="card-panel-num">{{ panelData.courses }}</div>
          </div>
        </div>
      </el-col>
      <el-col :xs="12" :sm="12" :lg="6" class="card-panel-col">
        <div class="card-panel">
          <div class="card-panel-icon-wrapper icon-money">
            <i class="el-icon-trophy card-panel-icon"></i>
          </div>
          <div class="card-panel-description">
            <div class="card-panel-text">竞赛活动</div>
            <div class="card-panel-num">{{ panelData.competitions }}</div>
          </div>
        </div>
      </el-col>
      <el-col :xs="12" :sm="12" :lg="6" class="card-panel-col">
        <div class="card-panel">
          <div class="card-panel-icon-wrapper icon-shopping">
            <i class="el-icon-cpu card-panel-icon"></i>
          </div>
          <div class="card-panel-description">
            <div class="card-panel-text">编程题库</div>
            <div class="card-panel-num">{{ panelData.problems }}</div>
          </div>
        </div>
      </el-col>
    </el-row>

    <el-row style="background:#fff;padding:16px 16px 0;margin-bottom:32px;">
      <div id="lineChart" style="height: 350px; width: 100%;"></div>
    </el-row>

    <el-row :gutter="32">
      <el-col :xs="24" :sm="24" :lg="12">
        <div class="chart-wrapper">
          <div class="chart-title">作业成绩分布</div>
          <div id="pieChart" style="height: 300px; width: 100%;"></div>
        </div>
      </el-col>
      <el-col :xs="24" :sm="24" :lg="12">
        <div class="chart-wrapper">
          <div class="chart-title">热门竞赛参与人数</div>
          <div id="barChart" style="height: 300px; width: 100%;"></div>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import * as echarts from 'echarts';

export default {
  name: "AdminDashboard",
  data() {
    return {
      panelData: {
        users: 0,
        courses: 0,
        competitions: 0,
        problems: 0
      },
      lineChart: null,
      pieChart: null,
      barChart: null
    };
  },
  mounted() {
    this.fetchData();
    window.addEventListener('resize', this.resizeCharts);
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.resizeCharts);
    if (this.lineChart) this.lineChart.dispose();
    if (this.pieChart) this.pieChart.dispose();
    if (this.barChart) this.barChart.dispose();
  },
  methods: {
    async fetchData() {
      try {
        const res = await this.$axios.get('dashboard/statistics/');
        const data = res.data;
        
        // 1. 设置面板数据
        this.panelData = data.panel;

        // 2. 初始化图表
        this.initLineChart(data.lineChart);
        this.initPieChart(data.pieChart);
        this.initBarChart(data.barChart);

      } catch (error) {
        console.error("获取仪表盘数据失败", error);
        this.$message.error("加载数据失败");
      }
    },
    resizeCharts() {
      if (this.lineChart) this.lineChart.resize();
      if (this.pieChart) this.pieChart.resize();
      if (this.barChart) this.barChart.resize();
    },
    initLineChart(data) {
      this.lineChart = echarts.init(document.getElementById('lineChart'));
      this.lineChart.setOption({
        title: { text: '全站近7天数据趋势', left: 'center' },
        tooltip: { trigger: 'axis' },
        legend: { data: ['作业提交量', '活跃用户'], bottom: 0 },
        grid: { left: '3%', right: '4%', bottom: '10%', containLabel: true },
        xAxis: { type: 'category', boundaryGap: false, data: data.dates },
        yAxis: { type: 'value' },
        series: [
          {
            name: '作业提交量',
            type: 'line',
            smooth: true,
            data: data.submissions,
            itemStyle: { color: '#3888fa' },
            areaStyle: { color: 'rgba(56, 136, 250, 0.1)' }
          },
          {
            name: '活跃用户',
            type: 'line',
            smooth: true,
            data: data.active_users,
            itemStyle: { color: '#f4516c' },
            areaStyle: { color: 'rgba(244, 81, 108, 0.1)' }
          }
        ]
      });
    },
    initPieChart(data) {
      this.pieChart = echarts.init(document.getElementById('pieChart'));
      this.pieChart.setOption({
        tooltip: { trigger: 'item' },
        legend: { orient: 'vertical', left: 'left' },
        series: [
          {
            name: '成绩分布',
            type: 'pie',
            radius: '50%',
            data: data,
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
              }
            }
          }
        ]
      });
    },
    initBarChart(data) {
      this.barChart = echarts.init(document.getElementById('barChart'));
      this.barChart.setOption({
        tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
        grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
        xAxis: { type: 'category', data: data.categories, axisLabel: { interval: 0, rotate: 30 } },
        yAxis: { type: 'value' },
        series: [
          {
            name: '报名人数',
            type: 'bar',
            barWidth: '40%',
            data: data.values,
            itemStyle: { color: '#34bfa3' }
          }
        ]
      });
    }
  }
};
</script>

<style lang="scss" scoped>
.dashboard-container {
  padding: 32px;
  background-color: #f0f2f5;
  min-height: 100vh;
}

.chart-wrapper {
  background: #fff;
  padding: 16px 16px 0;
  margin-bottom: 32px;
  border-radius: 4px;
  .chart-title {
    font-size: 16px;
    font-weight: bold;
    color: #333;
    margin-bottom: 15px;
    text-align: center;
  }
}

.panel-group {
  margin-top: 18px;
  .card-panel-col {
    margin-bottom: 32px;
  }
  .card-panel {
    height: 108px;
    cursor: pointer;
    font-size: 12px;
    position: relative;
    overflow: hidden;
    color: #666;
    background: #fff;
    box-shadow: 4px 4px 40px rgba(0, 0, 0, .05);
    border-color: rgba(0, 0, 0, .05);
    display: flex;
    align-items: center;

    &:hover {
      .card-panel-icon-wrapper { color: #fff; }
      .icon-people { background: #40c9c6; }
      .icon-message { background: #36a3f7; }
      .icon-money { background: #f4516c; }
      .icon-shopping { background: #34bfa3; }
    }

    .icon-people { color: #40c9c6; }
    .icon-message { color: #36a3f7; }
    .icon-money { color: #f4516c; }
    .icon-shopping { color: #34bfa3; }

    .card-panel-icon-wrapper {
      float: left;
      margin: 14px 0 0 14px;
      padding: 16px;
      transition: all 0.38s ease-out;
      border-radius: 6px;
    }

    .card-panel-icon {
      float: left;
      font-size: 48px;
    }

    .card-panel-description {
      float: right;
      font-weight: bold;
      margin: 26px;
      margin-left: 0px;

      .card-panel-text {
        line-height: 18px;
        color: rgba(0, 0, 0, 0.45);
        font-size: 16px;
        margin-bottom: 12px;
      }

      .card-panel-num {
        font-size: 20px;
      }
    }
  }
}
</style>