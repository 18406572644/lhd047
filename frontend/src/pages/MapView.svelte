<script>
  import { onMount, onDestroy } from 'svelte'
  import { link } from 'svelte-spa-router'
  import L from 'leaflet'
  import { buildingsAPI } from '../api/modules'

  let map = null
  let buildings = []
  let selectedBuilding = null
  let loading = true
  let mapContainer = null

  onMount(async () => {
    try {
      const data = await buildingsAPI.getList({ page_size: 50 })
      buildings = data.items
      initMap()
    } catch (e) {
      console.error('加载建筑数据失败', e)
    } finally {
      loading = false
    }
  })

  function initMap() {
    if (!mapContainer || buildings.length === 0) return

    map = L.map(mapContainer).setView([31.23, 121.47], 13)

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map)

    buildings.forEach(building => {
      const marker = L.circleMarker(
        [building.latitude, building.longitude],
        {
          radius: 10,
          fillColor: getDangerColor(building.danger_level),
          color: '#000',
          weight: 2,
          opacity: 1,
          fillOpacity: 0.8
        }
      ).addTo(map)

      marker.bindPopup(`
        <div style="min-width: 200px;">
          <h4 style="margin: 0 0 8px 0; font-size: 16px;">${building.title}</h4>
          <p style="margin: 0 0 8px 0; font-size: 13px; color: #666;">
            ${building.building_type} · 危险等级 ${building.danger_level}
          </p>
          <p style="margin: 0 0 10px 0; font-size: 12px; color: #888;">
            ${building.address}
          </p>
          <a href="#/buildings/${building.id}" 
             style="color: #b7410e; text-decoration: none; font-size: 13px;">
            查看详情 →
          </a>
        </div>
      `)

      marker.on('click', () => {
        selectedBuilding = building
      })
    })
  }

  function getDangerColor(level) {
    const colors = ['', '#4a7c59', '#d4a040', '#b7410e', '#dc4c2e', '#ff3030']
    return colors[level] || '#888'
  }

  onDestroy(() => {
    if (map) {
      map.remove()
      map = null
    }
  })
</script>

<div class="map-page">
  <div class="page-header container">
    <h1 class="page-title">探索地图</h1>
    <p class="page-subtitle">在地图上发现城市中的废墟秘境</p>
  </div>

  <div class="map-container">
    <div class="map-wrapper">
      <div bind:this={mapContainer} class="map-canvas"></div>

      <div class="map-legend">
        <h4>危险等级图例</h4>
        <div class="legend-items">
          <div class="legend-item">
            <span class="legend-dot" style="background: #4a7c59;"></span>
            <span>1级 - 安全</span>
          </div>
          <div class="legend-item">
            <span class="legend-dot" style="background: #d4a040;"></span>
            <span>2级 - 注意</span>
          </div>
          <div class="legend-item">
            <span class="legend-dot" style="background: #b7410e;"></span>
            <span>3级 - 危险</span>
          </div>
          <div class="legend-item">
            <span class="legend-dot" style="background: #dc4c2e;"></span>
            <span>4级 - 高危</span>
          </div>
          <div class="legend-item">
            <span class="legend-dot" style="background: #ff3030;"></span>
            <span>5级 - 极危</span>
          </div>
        </div>
      </div>
    </div>

    <div class="map-sidebar">
      <div class="sidebar-card card">
        <h3 class="sidebar-title">📍 废墟分布</h3>
        <p class="sidebar-count">
          共 <span class="text-rust">{buildings.length}</span> 处已记录
        </p>
      </div>

      {#if selectedBuilding}
        <div class="sidebar-card card selected-card">
          <div class="selected-header">
            <span class="selected-badge">已选择</span>
          </div>
          <h3 class="building-name">{selectedBuilding.title}</h3>
          <div class="building-meta">
            <span class="badge badge-moss">{selectedBuilding.building_type}</span>
            <span class="badge badge-rust">危险 {selectedBuilding.danger_level}</span>
          </div>
          <p class="building-desc">{selectedBuilding.description}</p>
          <p class="building-address">📍 {selectedBuilding.address}</p>
          <a href={`#/buildings/${selectedBuilding.id}`} use:link class="btn btn-primary w-full">
            查看详细档案 →
          </a>
        </div>
      {/if}

      <div class="sidebar-card card">
        <h3 class="sidebar-title">💡 探索提示</h3>
        <ul class="tips-list">
          <li>点击地图标记查看建筑信息</li>
          <li>红色标记表示危险等级较高</li>
          <li>绿色标记表示相对安全</li>
          <li>探索前请做好安全准备</li>
        </ul>
      </div>
    </div>
  </div>
</div>

<style>
  .map-page {
    padding-bottom: 60px;
  }

  .page-header {
    text-align: center;
    padding: 40px 20px 30px;
  }

  .page-title {
    font-size: 32px;
    margin-bottom: 8px;
  }

  .page-subtitle {
    color: var(--text-muted);
    font-size: 16px;
  }

  .map-container {
    max-width: 1280px;
    margin: 0 auto;
    padding: 0 20px;
    display: grid;
    grid-template-columns: 1fr 320px;
    gap: 20px;
  }

  .map-wrapper {
    position: relative;
    border-radius: 8px;
    overflow: hidden;
    border: 2px solid var(--border-color);
    box-shadow: var(--shadow-dark);
  }

  .map-canvas {
    height: 600px;
    background: var(--bg-mid);
  }

  .map-canvas :global(.leaflet-container) {
    height: 100%;
    width: 100%;
    filter: grayscale(30%) contrast(90%);
  }

  .map-legend {
    position: absolute;
    bottom: 20px;
    left: 20px;
    background: rgba(28, 28, 26, 0.95);
    backdrop-filter: blur(10px);
    padding: 16px 20px;
    border-radius: 6px;
    border: 1px solid var(--border-color);
    z-index: 1000;
  }

  .map-legend h4 {
    font-size: 13px;
    margin-bottom: 12px;
    color: var(--text-bright);
  }

  .legend-items {
    display: flex;
    flex-direction: column;
    gap: 8px;
  }

  .legend-item {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 12px;
    color: var(--text-main);
  }

  .legend-dot {
    width: 14px;
    height: 14px;
    border-radius: 50%;
    border: 2px solid #000;
  }

  .map-sidebar {
    display: flex;
    flex-direction: column;
    gap: 16px;
  }

  .sidebar-card {
    padding: 20px;
  }

  .sidebar-title {
    font-size: 15px;
    margin-bottom: 12px;
    padding-bottom: 10px;
    border-bottom: 1px solid var(--border-color);
  }

  .sidebar-count {
    font-size: 14px;
    color: var(--text-muted);
  }

  .selected-card {
    border-color: var(--rust-mid);
    position: relative;
  }

  .selected-header {
    position: absolute;
    top: 0;
    right: 0;
  }

  .selected-badge {
    display: inline-block;
    padding: 4px 12px;
    background: var(--rust-mid);
    color: white;
    font-size: 11px;
    border-radius: 0 6px 0 6px;
  }

  .building-name {
    font-size: 18px;
    margin-bottom: 10px;
    padding-top: 8px;
  }

  .building-meta {
    display: flex;
    gap: 8px;
    margin-bottom: 12px;
  }

  .building-desc {
    font-size: 13px;
    color: var(--text-muted);
    line-height: 1.6;
    margin-bottom: 12px;
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }

  .building-address {
    font-size: 13px;
    color: var(--text-main);
    margin-bottom: 16px;
  }

  .w-full {
    width: 100%;
  }

  .tips-list {
    list-style: none;
    padding: 0;
    margin: 0;
  }

  .tips-list li {
    padding: 8px 0;
    font-size: 13px;
    color: var(--text-muted);
    border-bottom: 1px dashed var(--border-color);
    padding-left: 16px;
    position: relative;
  }

  .tips-list li::before {
    content: '•';
    position: absolute;
    left: 0;
    color: var(--rust-mid);
  }

  .tips-list li:last-child {
    border-bottom: none;
  }

  @media (max-width: 900px) {
    .map-container {
      grid-template-columns: 1fr;
    }

    .map-canvas {
      height: 400px;
    }
  }
</style>
