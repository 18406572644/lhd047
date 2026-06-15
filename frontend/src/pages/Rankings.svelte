<script>
  import { onMount } from 'svelte'
  import { link } from 'svelte-spa-router'
  import { buildingsAPI, statsAPI } from '../api/modules'

  let topBuildings = []
  let stats = null
  let loading = true

  onMount(async () => {
    try {
      const [topData, statsData] = await Promise.all([
        buildingsAPI.getHot(20),
        statsAPI.getStats()
      ])
      topBuildings = topData
      stats = statsData
    } catch (e) {
      console.error('加载排行榜数据失败', e)
    } finally {
      loading = false
    }
  })

  function getRankBadgeClass(rank) {
    if (rank === 1) return 'rank-gold'
    if (rank === 2) return 'rank-silver'
    if (rank === 3) return 'rank-bronze'
    return 'rank-normal'
  }
</script>

<div class="rankings-page container">
  <div class="page-header">
    <h1 class="page-title">🏆 热门探索排行</h1>
    <p class="page-subtitle">探索者们最爱的废墟打卡点</p>
  </div>

  {#if stats}
    <div class="stats-overview">
      <div class="stat-card card">
        <div class="stat-icon">🏚️</div>
        <div class="stat-info">
          <span class="stat-number">{stats.total_buildings}</span>
          <span class="stat-label">处废墟档案</span>
        </div>
      </div>
      <div class="stat-card card">
        <div class="stat-icon">👥</div>
        <div class="stat-info">
          <span class="stat-number">{stats.total_users}</span>
          <span class="stat-label">位探索者</span>
        </div>
      </div>
      <div class="stat-card card">
        <div class="stat-icon">💬</div>
        <div class="stat-info">
          <span class="stat-number">{stats.total_comments}</span>
          <span class="stat-label">条探索心得</span>
        </div>
      </div>
      <div class="stat-card card">
        <div class="stat-icon">📷</div>
        <div class="stat-info">
          <span class="stat-number">{stats.total_photos}</span>
          <span class="stat-label">张实拍照片</span>
        </div>
      </div>
    </div>
  {/if}

  <div class="ranking-section">
    <div class="section-header">
      <h2 class="section-title">🔥 热门探索点 TOP 20</h2>
      <span class="section-desc">按探索次数排序</span>
    </div>

    {#if loading}
      <div class="loading-state">
        <div class="loading-spinner"></div>
        <p>加载排行榜中...</p>
      </div>
    {:else}
      <div class="ranking-list">
        {#each topBuildings as building, index}
          <a href={`#/buildings/${building.id}`} use:link class="ranking-item card">
            <div class="rank-number {getRankBadgeClass(index + 1)}">
              {#if index < 3}
                <span class="crown">👑</span>
              {/if}
              {index + 1}
            </div>
            
            <div class="building-image">
              <span class="building-icon">🏚️</span>
            </div>

            <div class="building-info">
              <h3 class="building-name">{building.title}</h3>
              <div class="building-meta">
                <span class="badge badge-moss">{building.building_type}</span>
                <span class="danger-level danger-{building.danger_level}">
                  危险等级 {building.danger_level}
                </span>
              </div>
              <p class="building-address">📍 {building.address}</p>
              
              {#if building.tags && building.tags.length > 0}
                <div class="building-tags">
                  {#each building.tags.slice(0, 3) as tag}
                    <span class="tag-small">#{tag.tag}</span>
                  {/each}
                </div>
              {/if}
            </div>

            <div class="explore-count">
              <span class="count-number">{building.explore_count}</span>
              <span class="count-label">次探索</span>
            </div>
          </a>
        {/each}
      </div>
    {/if}
  </div>
</div>

<style>
  .rankings-page {
    padding: 40px 20px 60px;
  }

  .page-header {
    text-align: center;
    margin-bottom: 40px;
  }

  .page-title {
    font-size: 32px;
    margin-bottom: 8px;
  }

  .page-subtitle {
    color: var(--text-muted);
    font-size: 16px;
  }

  .stats-overview {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    margin-bottom: 50px;
  }

  .stat-card {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 24px;
  }

  .stat-icon {
    font-size: 40px;
    opacity: 0.8;
  }

  .stat-info {
    display: flex;
    flex-direction: column;
  }

  .stat-number {
    font-family: 'ZCOOL KuaiLe', cursive;
    font-size: 32px;
    color: var(--rust-light);
    line-height: 1;
  }

  .stat-label {
    font-size: 13px;
    color: var(--text-muted);
    margin-top: 4px;
  }

  .ranking-section {
    max-width: 900px;
    margin: 0 auto;
  }

  .section-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    margin-bottom: 24px;
  }

  .section-title {
    margin-bottom: 0;
    font-size: 24px;
  }

  .section-desc {
    font-size: 13px;
    color: var(--text-muted);
  }

  .loading-state {
    text-align: center;
    padding: 60px;
    color: var(--text-muted);
  }

  .loading-spinner {
    width: 40px;
    height: 40px;
    border: 3px solid var(--border-color);
    border-top-color: var(--rust-mid);
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin: 0 auto 16px;
  }

  @keyframes spin {
    to { transform: rotate(360deg); }
  }

  .ranking-list {
    display: flex;
    flex-direction: column;
    gap: 12px;
  }

  .ranking-item {
    display: flex;
    align-items: center;
    gap: 20px;
    padding: 16px 20px;
    text-decoration: none;
    color: inherit;
    transition: all 0.3s ease;
  }

  .ranking-item:hover {
    transform: translateX(4px);
    border-color: var(--rust-mid);
  }

  .rank-number {
    width: 44px;
    height: 44px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: 'ZCOOL KuaiLe', cursive;
    font-size: 20px;
    font-weight: bold;
    background: var(--bg-mid);
    color: var(--text-muted);
    flex-shrink: 0;
    position: relative;
  }

  .rank-gold {
    background: linear-gradient(135deg, #ffd700, #b8860b);
    color: #4a3800;
  }

  .rank-silver {
    background: linear-gradient(135deg, #c0c0c0, #808080);
    color: #333;
  }

  .rank-bronze {
    background: linear-gradient(135deg, #cd7f32, #8b4513);
    color: #3d1f00;
  }

  .crown {
    position: absolute;
    top: -14px;
    left: 50%;
    transform: translateX(-50%);
    font-size: 20px;
  }

  .building-image {
    width: 80px;
    height: 80px;
    border-radius: 6px;
    background: linear-gradient(135deg, var(--cement-mid), var(--cement-dark));
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
  }

  .building-icon {
    font-size: 36px;
    opacity: 0.5;
    filter: grayscale(50%);
  }

  .building-info {
    flex: 1;
    min-width: 0;
  }

  .building-name {
    font-size: 17px;
    margin-bottom: 8px;
    color: var(--text-bright);
  }

  .ranking-item:hover .building-name {
    color: var(--rust-light);
  }

  .building-meta {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 8px;
  }

  .danger-level {
    font-size: 11px;
    padding: 3px 8px;
    border-radius: 3px;
  }

  .danger-1 { background: rgba(74, 124, 89, 0.3); color: var(--moss-pale); }
  .danger-2 { background: rgba(212, 160, 64, 0.2); color: #d4a040; }
  .danger-3 { background: rgba(183, 65, 14, 0.3); color: var(--rust-light); }
  .danger-4 { background: rgba(220, 76, 46, 0.3); color: #dc6c46; }
  .danger-5 { background: rgba(255, 48, 48, 0.3); color: #ff6060; }

  .building-address {
    font-size: 12px;
    color: var(--text-muted);
    margin-bottom: 8px;
  }

  .building-tags {
    display: flex;
    gap: 6px;
    flex-wrap: wrap;
  }

  .tag-small {
    font-size: 11px;
    color: var(--rust-light);
    opacity: 0.8;
  }

  .explore-count {
    text-align: right;
    flex-shrink: 0;
  }

  .count-number {
    display: block;
    font-family: 'ZCOOL KuaiLe', cursive;
    font-size: 28px;
    color: var(--rust-light);
    line-height: 1;
  }

  .count-label {
    font-size: 12px;
    color: var(--text-muted);
  }

  @media (max-width: 768px) {
    .stats-overview {
      grid-template-columns: repeat(2, 1fr);
    }

    .building-image {
      display: none;
    }

    .count-number {
      font-size: 22px;
    }
  }

  @media (max-width: 480px) {
    .stats-overview {
      grid-template-columns: 1fr 1fr;
      gap: 10px;
    }

    .stat-card {
      padding: 16px;
    }

    .stat-icon {
      font-size: 28px;
    }

    .stat-number {
      font-size: 24px;
    }
  }
</style>
