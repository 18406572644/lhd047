<script>
  import { onMount, onDestroy, afterUpdate } from 'svelte'
  import * as echarts from 'echarts'
  import { statsAPI } from '../api/modules'

  let loading = true
  let statsData = null
  let timeseriesData = null
  let selectedRange = null

  const rangeOptions = [
    { label: '近7天', value: 7 },
    { label: '近30天', value: 30 },
    { label: '全部', value: null }
  ]

  let pieChartRef = null
  let barChartRef = null
  let yearChartRef = null
  let lineChartRef = null
  let heatmapChartRef = null
  let topChartRef = null

  let pieChart = null
  let barChart = null
  let yearChart = null
  let lineChart = null
  let heatmapChart = null
  let topChart = null

  const rustPalette = ['#b7410e', '#cd5c5c', '#dc6c39', '#8b2500', '#6b3820', '#d48a5c', '#a0522d', '#c46210', '#a04000', '#e07030']
  const dangerColors = ['#4a7c59', '#6b8e6b', '#cd853f', '#dc6c39', '#8b2500']

  async function loadData() {
    loading = true
    try {
      const [stats, timeseries] = await Promise.all([
        statsAPI.getStats(selectedRange),
        statsAPI.getTimeseries(selectedRange)
      ])
      statsData = stats
      timeseriesData = timeseries
    } catch (err) {
      console.error('加载统计数据失败:', err)
    } finally {
      loading = false
    }
  }

  async function handleExport() {
    try {
      const blob = await statsAPI.exportCSV(selectedRange)
      const url = URL.createObjectURL(new Blob([blob], { type: 'text/csv;charset=utf-8-sig' }))
      const a = document.createElement('a')
      a.href = url
      const dateStr = new Date().toISOString().slice(0, 10).replace(/-/g, '')
      a.download = `buildings_export_${dateStr}.csv`
      document.body.appendChild(a)
      a.click()
      document.body.removeChild(a)
      URL.revokeObjectURL(url)
    } catch (err) {
      console.error('导出失败:', err)
    }
  }

  function initCharts() {
    if (pieChartRef && !pieChart) {
      pieChart = echarts.init(pieChartRef)
    }
    if (barChartRef && !barChart) {
      barChart = echarts.init(barChartRef)
    }
    if (yearChartRef && !yearChart) {
      yearChart = echarts.init(yearChartRef)
    }
    if (lineChartRef && !lineChart) {
      lineChart = echarts.init(lineChartRef)
    }
    if (heatmapChartRef && !heatmapChart) {
      heatmapChart = echarts.init(heatmapChartRef)
    }
    if (topChartRef && !topChart) {
      topChart = echarts.init(topChartRef)
    }
  }

  function renderCharts() {
    if (!statsData || !timeseriesData) return

    if (pieChart) {
      const pieData = Object.entries(statsData.buildings_by_type || {}).map(([name, value]) => ({ name, value }))
      pieChart.setOption({
        tooltip: { trigger: 'item', formatter: '{b}: {c} ({d}%)' },
        legend: {
          textStyle: { color: '#d4d0c8' },
          bottom: 5,
          type: 'scroll',
          pageTextStyle: { color: '#d4d0c8' },
          pageIconColor: '#b7410e',
          pageIconInactiveColor: '#5a5a56'
        },
        color: rustPalette,
        series: [{
          type: 'pie',
          radius: ['35%', '65%'],
          center: ['50%', '42%'],
          avoidLabelOverlap: true,
          itemStyle: {
            borderRadius: 6,
            borderColor: '#1c1c1a',
            borderWidth: 2
          },
          label: {
            color: '#d4d0c8',
            fontSize: 11,
            formatter: '{b}\n{d}%'
          },
          labelLine: { lineStyle: { color: '#5a5a56' } },
          emphasis: {
            label: { fontSize: 14, fontWeight: 'bold' },
            itemStyle: { shadowBlur: 20, shadowColor: 'rgba(183, 65, 14, 0.5)' }
          },
          data: pieData
        }]
      })
    }

    if (barChart) {
      const dangerEntries = Object.entries(statsData.buildings_by_danger_level || {})
        .sort((a, b) => Number(a[0]) - Number(b[0]))
      const barData = dangerEntries.map(([level, count]) => {
        const idx = Math.min(Number(level) - 1, dangerColors.length - 1)
        return {
          value: count,
          itemStyle: { color: dangerColors[idx] || '#b7410e', borderRadius: [4, 4, 0, 0] }
        }
      })
      const barLabels = dangerEntries.map(([level]) => `等级 ${level}`)
      barChart.setOption({
        tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
        grid: { left: '12%', right: '5%', top: '10%', bottom: '15%' },
        xAxis: {
          type: 'category',
          data: barLabels,
          axisLine: { lineStyle: { color: '#5a5a56' } },
          axisLabel: { color: '#d4d0c8', fontSize: 12 },
          axisTick: { show: false }
        },
        yAxis: {
          type: 'value',
          axisLine: { lineStyle: { color: '#5a5a56' } },
          axisLabel: { color: '#d4d0c8', fontSize: 11 },
          splitLine: { lineStyle: { color: '#383835' } }
        },
        series: [{
          type: 'bar',
          data: barData,
          barWidth: '50%',
          emphasis: { itemStyle: { shadowBlur: 15, shadowColor: 'rgba(183, 65, 14, 0.4)' } }
        }]
      })
    }

    if (yearChart) {
      const yearEntries = Object.entries(statsData.buildings_by_year || {})
        .sort((a, b) => Number(a[0]) - Number(b[0]))
      const yearLabels = yearEntries.map(([y]) => y + '年')
      const yearValues = yearEntries.map(([, v]) => v)
      yearChart.setOption({
        tooltip: {
          trigger: 'axis',
          axisPointer: { type: 'cross', label: { backgroundColor: '#b7410e' } }
        },
        grid: { left: '10%', right: '5%', top: '12%', bottom: '18%' },
        dataZoom: [{
          type: 'inside',
          start: 0,
          end: 100
        }, {
          start: 0,
          end: 100,
          height: 18,
          bottom: 5,
          borderColor: 'transparent',
          fillerColor: 'rgba(183, 65, 14, 0.2)',
          handleStyle: { color: '#b7410e' },
          moveHandleStyle: { color: '#cd5c5c' },
          textStyle: { color: '#d4d0c8' }
        }],
        xAxis: {
          type: 'category',
          data: yearLabels,
          axisLine: { lineStyle: { color: '#5a5a56' } },
          axisLabel: { color: '#d4d0c8', fontSize: 10, rotate: 45 },
          axisTick: { show: false }
        },
        yAxis: {
          type: 'value',
          axisLine: { lineStyle: { color: '#5a5a56' } },
          axisLabel: { color: '#d4d0c8', fontSize: 11 },
          splitLine: { lineStyle: { color: '#383835' } }
        },
        series: [{
          name: '建筑数',
          type: 'line',
          data: yearValues,
          smooth: true,
          symbol: 'circle',
          symbolSize: 8,
          lineStyle: { color: '#b7410e', width: 3 },
          itemStyle: { color: '#cd5c5c', borderColor: '#1c1c1a', borderWidth: 2 },
          areaStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: 'rgba(183, 65, 14, 0.45)' },
              { offset: 1, color: 'rgba(183, 65, 14, 0.02)' }
            ])
          },
          emphasis: { focus: 'series' }
        }]
      })
    }

    if (lineChart) {
      const allDates = new Set()
      const buildingsMap = {}
      const usersMap = {}
      ;(timeseriesData.buildings || []).forEach(p => { allDates.add(p.date); buildingsMap[p.date] = p.count })
      ;(timeseriesData.users || []).forEach(p => { allDates.add(p.date); usersMap[p.date] = p.count })
      const dates = Array.from(allDates).sort()
      const buildingSeries = dates.map(d => buildingsMap[d] || 0)
      const userSeries = dates.map(d => usersMap[d] || 0)

      lineChart.setOption({
        tooltip: { trigger: 'axis' },
        legend: {
          data: ['新增建筑', '新增用户'],
          textStyle: { color: '#d4d0c8' },
          top: 5
        },
        grid: { left: '10%', right: '5%', top: '18%', bottom: '18%' },
        dataZoom: [{
          type: 'inside',
          start: 0,
          end: 100
        }, {
          start: 0,
          end: 100,
          height: 18,
          bottom: 5,
          borderColor: 'transparent',
          fillerColor: 'rgba(74, 124, 89, 0.2)',
          handleStyle: { color: '#4a7c59' },
          textStyle: { color: '#d4d0c8' }
        }],
        xAxis: {
          type: 'category',
          data: dates,
          axisLine: { lineStyle: { color: '#5a5a56' } },
          axisLabel: { color: '#d4d0c8', fontSize: 10, rotate: 45 },
          axisTick: { show: false }
        },
        yAxis: {
          type: 'value',
          axisLine: { lineStyle: { color: '#5a5a56' } },
          axisLabel: { color: '#d4d0c8', fontSize: 11 },
          splitLine: { lineStyle: { color: '#383835' } }
        },
        series: [
          {
            name: '新增建筑',
            type: 'line',
            data: buildingSeries,
            smooth: true,
            symbol: 'circle',
            symbolSize: 6,
            lineStyle: { color: '#b7410e', width: 2.5 },
            itemStyle: { color: '#cd5c5c' }
          },
          {
            name: '新增用户',
            type: 'line',
            data: userSeries,
            smooth: true,
            symbol: 'circle',
            symbolSize: 6,
            lineStyle: { color: '#4a7c59', width: 2.5 },
            itemStyle: { color: '#6b8e6b' }
          }
        ]
      })
    }

    if (heatmapChart) {
      const geoData = statsData.geo_distribution || []
      if (geoData.length > 0) {
        const scatterData = geoData.map(g => [g.longitude, g.latitude, g.count])
        const maxCount = Math.max(...geoData.map(g => g.count))
        heatmapChart.setOption({
          tooltip: {
            formatter: (p) => `经度: ${p.value[0].toFixed(2)}<br/>纬度: ${p.value[1].toFixed(2)}<br/>建筑数: ${p.value[2]}`
          },
          grid: { left: '5%', right: '5%', top: '10%', bottom: '12%' },
          xAxis: {
            type: 'value',
            name: '经度',
            nameTextStyle: { color: '#d4d0c8', fontSize: 11 },
            axisLine: { lineStyle: { color: '#5a5a56' } },
            axisLabel: { color: '#d4d0c8', fontSize: 10 },
            splitLine: { lineStyle: { color: '#383835' } }
          },
          yAxis: {
            type: 'value',
            name: '纬度',
            nameTextStyle: { color: '#d4d0c8', fontSize: 11 },
            axisLine: { lineStyle: { color: '#5a5a56' } },
            axisLabel: { color: '#d4d0c8', fontSize: 10 },
            splitLine: { lineStyle: { color: '#383835' } }
          },
          visualMap: {
            min: 1,
            max: maxCount,
            dimension: 2,
            orient: 'horizontal',
            right: 'center',
            bottom: 5,
            text: ['多', '少'],
            textStyle: { color: '#d4d0c8', fontSize: 11 },
            inRange: {
              color: ['#1a3a2a', '#2d5a3d', '#cd853f', '#dc6c39', '#8b2500']
            },
            itemWidth: 15,
            itemHeight: 120
          },
          series: [{
            type: 'scatter',
            data: scatterData,
            symbolSize: (val) => Math.min(8 + val[2] * 3, 30),
            itemStyle: {
              shadowBlur: 10,
              shadowColor: 'rgba(183, 65, 14, 0.5)'
            }
          }]
        })
      } else {
        heatmapChart.setOption({
          title: {
            text: '暂无地理分布数据',
            left: 'center',
            top: 'center',
            textStyle: { color: '#8a8780', fontSize: 14, fontWeight: 'normal' }
          }
        })
      }
    }

    if (topChart) {
      const top = (statsData.top_explored || []).slice(0, 10).reverse()
      const topTitles = top.map(b => b.title.length > 15 ? b.title.slice(0, 15) + '...' : b.title)
      const topCounts = top.map(b => b.explore_count)
      topChart.setOption({
        tooltip: {
          trigger: 'axis',
          axisPointer: { type: 'shadow' },
          formatter: (params) => {
            const idx = params[0].dataIndex
            return `${top[idx].title}<br/>探索次数: ${top[idx].explore_count}`
          }
        },
        grid: { left: '22%', right: '8%', top: '5%', bottom: '8%' },
        xAxis: {
          type: 'value',
          axisLine: { lineStyle: { color: '#5a5a56' } },
          axisLabel: { color: '#d4d0c8', fontSize: 11 },
          splitLine: { lineStyle: { color: '#383835' } }
        },
        yAxis: {
          type: 'category',
          data: topTitles,
          axisLine: { lineStyle: { color: '#5a5a56' } },
          axisLabel: { color: '#d4d0c8', fontSize: 11 },
          axisTick: { show: false }
        },
        series: [{
          type: 'bar',
          data: topCounts.map((v, i) => ({
            value: v,
            itemStyle: {
              color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
                { offset: 0, color: '#6b3820' },
                { offset: 1, color: rustPalette[i % rustPalette.length] }
              ]),
              borderRadius: [0, 4, 4, 0]
            }
          })),
          barWidth: '60%',
          label: {
            show: true,
            position: 'right',
            color: '#d4d0c8',
            fontSize: 11
          },
          emphasis: { itemStyle: { shadowBlur: 15, shadowColor: 'rgba(183, 65, 14, 0.4)' } }
        }]
      })
    }
  }

  function handleResize() {
    pieChart && pieChart.resize()
    barChart && barChart.resize()
    yearChart && yearChart.resize()
    lineChart && lineChart.resize()
    heatmapChart && heatmapChart.resize()
    topChart && topChart.resize()
  }

  async function changeRange(val) {
    selectedRange = val
    await loadData()
  }

  afterUpdate(() => {
    initCharts()
    if (statsData && timeseriesData) {
      renderCharts()
    }
  })

  onMount(async () => {
    await loadData()
    window.addEventListener('resize', handleResize)
  })

  onDestroy(() => {
    window.removeEventListener('resize', handleResize)
    pieChart && pieChart.dispose()
    barChart && barChart.dispose()
    yearChart && yearChart.dispose()
    lineChart && lineChart.dispose()
    heatmapChart && heatmapChart.dispose()
    topChart && topChart.dispose()
  })
</script>

<div class="dashboard-page">
  <div class="page-header">
    <div class="header-left">
      <h1 class="page-title">数据仪表盘</h1>
      <p class="page-subtitle">DATA DASHBOARD · 废墟档案全景视图</p>
    </div>
    <div class="header-right">
      <div class="range-selector">
        {#each rangeOptions as opt}
          <button
            class={selectedRange === opt.value ? 'range-btn active' : 'range-btn'}
            on:click={() => changeRange(opt.value)}
            disabled={loading}
          >
            {opt.label}
          </button>
        {/each}
      </div>
      <button class="export-btn" on:click={handleExport} disabled={loading}>
        <span class="export-icon">📥</span>
        导出 CSV
      </button>
    </div>
  </div>

  {#if loading}
    <div class="loading-wrap">
      <div class="spinner"></div>
      <p class="loading-text">正在加载数据...</p>
    </div>
  {:else}
    {#if statsData}
      <div class="stats-cards">
        <div class="stat-card card-buildings">
          <div class="stat-icon">🏚️</div>
          <div class="stat-content">
            <div class="stat-value">{statsData.total_buildings}</div>
            <div class="stat-label">建筑总数</div>
          </div>
        </div>
        <div class="stat-card card-users">
          <div class="stat-icon">👥</div>
          <div class="stat-content">
            <div class="stat-value">{statsData.total_users}</div>
            <div class="stat-label">用户总数</div>
          </div>
        </div>
        <div class="stat-card card-comments">
          <div class="stat-icon">💬</div>
          <div class="stat-content">
            <div class="stat-value">{statsData.total_comments}</div>
            <div class="stat-label">评论总数</div>
          </div>
        </div>
        <div class="stat-card card-photos">
          <div class="stat-icon">📷</div>
          <div class="stat-content">
            <div class="stat-value">{statsData.total_photos}</div>
            <div class="stat-label">照片总数</div>
          </div>
        </div>
      </div>

      <div class="charts-grid">
        <div class="chart-card large">
          <div class="chart-header">
            <h3>建筑类型分布</h3>
            <span class="chart-tag">饼图</span>
          </div>
          <div class="chart-body">
            <div class="chart-container" bind:this={pieChartRef}></div>
          </div>
        </div>

        <div class="chart-card">
          <div class="chart-header">
            <h3>危险等级分布</h3>
            <span class="chart-tag">柱状图</span>
          </div>
          <div class="chart-body">
            <div class="chart-container" bind:this={barChartRef}></div>
          </div>
        </div>

        <div class="chart-card">
          <div class="chart-header">
            <h3>热门建筑 Top 10</h3>
            <span class="chart-tag">横向柱状</span>
          </div>
          <div class="chart-body">
            <div class="chart-container" bind:this={topChartRef}></div>
          </div>
        </div>

        <div class="chart-card full">
          <div class="chart-header">
            <h3>建筑年代分布时间线</h3>
            <span class="chart-tag">折线图</span>
          </div>
          <div class="chart-body">
            <div class="chart-container" bind:this={yearChartRef}></div>
          </div>
        </div>

        <div class="chart-card full">
          <div class="chart-header">
            <h3>月度新增建筑 / 用户增长趋势</h3>
            <span class="chart-tag">双折线</span>
          </div>
          <div class="chart-body">
            <div class="chart-container" bind:this={lineChartRef}></div>
          </div>
        </div>

        <div class="chart-card full">
          <div class="chart-header">
            <h3>地理分布热力图</h3>
            <span class="chart-tag">散点聚合</span>
          </div>
          <div class="chart-body">
            <div class="chart-container" bind:this={heatmapChartRef}></div>
          </div>
        </div>
      </div>
    {/if}
  {/if}
</div>

<style>
  .dashboard-page {
    max-width: 1400px;
    margin: 0 auto;
    padding: 30px 24px 60px;
  }

  .page-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    flex-wrap: wrap;
    gap: 20px;
    margin-bottom: 28px;
    padding-bottom: 20px;
    border-bottom: 1px solid var(--border-color);
  }

  .header-left {
    flex: 1;
  }

  .page-title {
    font-size: 32px;
    color: var(--text-bright);
    margin-bottom: 6px;
    letter-spacing: 4px;
  }

  .page-subtitle {
    font-size: 12px;
    color: var(--rust-light);
    letter-spacing: 3px;
    font-family: 'Courier New', monospace;
  }

  .header-right {
    display: flex;
    align-items: center;
    gap: 16px;
    flex-wrap: wrap;
  }

  .range-selector {
    display: flex;
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: 8px;
    overflow: hidden;
  }

  .range-btn {
    background: transparent;
    color: var(--text-muted);
    padding: 10px 18px;
    font-size: 13px;
    border: none;
    border-right: 1px solid var(--border-color);
    transition: all 0.3s ease;
    letter-spacing: 1px;
  }

  .range-btn:last-child {
    border-right: none;
  }

  .range-btn:hover:not(:disabled) {
    background: var(--bg-hover);
    color: var(--text-bright);
  }

  .range-btn.active {
    background: var(--rust-mid);
    color: var(--text-bright);
    box-shadow: inset 0 2px 6px rgba(0, 0, 0, 0.2);
  }

  .range-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  .export-btn {
    background: linear-gradient(135deg, var(--moss-mid), var(--moss-dark));
    color: var(--text-bright);
    padding: 10px 20px;
    border-radius: 8px;
    font-size: 13px;
    border: 1px solid var(--moss-light);
    display: flex;
    align-items: center;
    gap: 8px;
    letter-spacing: 1px;
    transition: all 0.3s ease;
  }

  .export-btn:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(45, 90, 61, 0.4);
  }

  .export-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  .export-icon {
    font-size: 15px;
  }

  .loading-wrap {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 100px 0;
    gap: 16px;
  }

  .spinner {
    width: 48px;
    height: 48px;
    border: 4px solid var(--border-color);
    border-top-color: var(--rust-mid);
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
  }

  @keyframes spin {
    to { transform: rotate(360deg); }
  }

  .loading-text {
    color: var(--text-muted);
    font-size: 14px;
    letter-spacing: 2px;
  }

  .stats-cards {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 18px;
    margin-bottom: 28px;
  }

  .stat-card {
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: 22px;
    display: flex;
    align-items: center;
    gap: 18px;
    position: relative;
    overflow: hidden;
    transition: all 0.3s ease;
  }

  .stat-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 4px;
    height: 100%;
  }

  .stat-card:hover {
    transform: translateY(-3px);
    box-shadow: var(--shadow-dark);
    border-color: var(--border-rust);
  }

  .card-buildings::before { background: var(--rust-mid); }
  .card-users::before { background: var(--moss-light); }
  .card-comments::before { background: #cd853f; }
  .card-photos::before { background: #6b8e6b; }

  .stat-icon {
    font-size: 42px;
    width: 64px;
    height: 64px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: var(--bg-hover);
    border-radius: 12px;
    flex-shrink: 0;
  }

  .stat-content {
    flex: 1;
  }

  .stat-value {
    font-size: 32px;
    font-weight: bold;
    color: var(--text-bright);
    font-family: 'ZCOOL KuaiLe', cursive;
    letter-spacing: 2px;
    line-height: 1.2;
  }

  .stat-label {
    font-size: 13px;
    color: var(--text-muted);
    letter-spacing: 2px;
    margin-top: 4px;
  }

  .charts-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 20px;
  }

  .chart-card {
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    overflow: hidden;
    transition: all 0.3s ease;
  }

  .chart-card:hover {
    border-color: var(--border-rust);
    box-shadow: var(--shadow-dark);
  }

  .chart-card.large {
    grid-column: span 1;
  }

  .chart-card.full {
    grid-column: span 2;
  }

  .chart-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 16px 22px;
    border-bottom: 1px solid var(--border-color);
    background: linear-gradient(180deg, var(--bg-hover), transparent);
  }

  .chart-header h3 {
    font-size: 16px;
    color: var(--text-bright);
    letter-spacing: 2px;
    margin: 0;
  }

  .chart-tag {
    font-size: 11px;
    color: var(--rust-light);
    background: rgba(183, 65, 14, 0.12);
    padding: 3px 10px;
    border-radius: 4px;
    border: 1px solid var(--border-rust);
    letter-spacing: 1px;
    font-family: 'Courier New', monospace;
  }

  .chart-body {
    padding: 10px;
  }

  .chart-container {
    width: 100%;
    height: 340px;
  }

  .chart-card.full .chart-container {
    height: 360px;
  }

  @media (max-width: 900px) {
    .charts-grid {
      grid-template-columns: 1fr;
    }

    .chart-card.full {
      grid-column: span 1;
    }

    .page-title {
      font-size: 24px;
    }

    .stat-value {
      font-size: 26px;
    }
  }
</style>
