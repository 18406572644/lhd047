<script>
  import { onMount } from 'svelte'
  import { link } from 'svelte-spa-router'
  import { routesAPI } from '../api/modules'

  let routes = []
  let loading = true

  onMount(async () => {
    try {
      routes = await routesAPI.getList()
    } catch (e) {
      console.error('加载路线失败', e)
    } finally {
      loading = false
    }
  })

  function formatDuration(minutes) {
    if (minutes < 60) return `${minutes}分钟`
    const hours = Math.floor(minutes / 60)
    const mins = minutes % 60
    return mins > 0 ? `${hours}小时${mins}分钟` : `${hours}小时`
  }

  function getDifficultyText(level) {
    const texts = ['', '轻松', '简单', '中等', '困难', '极限']
    return texts[level] || '未知'
  }

  function getDifficultyClass(level) {
    if (level <= 2) return 'easy'
    if (level <= 3) return 'medium'
    return 'hard'
  }
</script>

<div class="routes-page container">
  <div class="page-header">
    <h1 class="page-title">🗺️ 探索路线</h1>
    <p class="page-subtitle">探索者们分享的经典路线，跟着走就对了</p>
  </div>

  {#if loading}
    <div class="loading-state">
      <div class="loading-spinner"></div>
      <p>加载探索路线中...</p>
    </div>
  {:else if routes.length === 0}
    <div class="empty-state">
      <div class="empty-icon">🛤️</div>
      <p>还没有探索路线</p>
      <p class="text-muted">成为第一个分享路线的探索者吧</p>
    </div>
  {:else}
    <div class="routes-grid grid grid-2">
      {#each routes as route}
        <div class="route-card card">
          <div class="route-header">
            <h3 class="route-title">{route.title}</h3>
            <span class="difficulty-badge {getDifficultyClass(route.difficulty)}">
              {getDifficultyText(route.difficulty)}
            </span>
          </div>

          <p class="route-desc">{route.description}</p>

          <div class="route-meta">
            <div class="meta-item">
              <span class="meta-icon">📍</span>
              <span class="meta-text">{route.points?.length || 0} 个点位</span>
            </div>
            <div class="meta-item">
              <span class="meta-icon">⏱️</span>
              <span class="meta-text">{formatDuration(route.duration_minutes)}</span>
            </div>
            <div class="meta-item">
              <span class="meta-icon">👤</span>
              <span class="meta-text">{route.user?.username || '匿名'}</span>
            </div>
          </div>

          {#if route.points && route.points.length > 0}
            <div class="route-points">
              {#each route.points as point, index}
                <div class="point-item">
                  <div class="point-number">{index + 1}</div>
                  <div class="point-info">
                    <p class="point-desc">{point.description || '途经点'}</p>
                    <span class="point-coords">
                      {point.latitude.toFixed(4)}, {point.longitude.toFixed(4)}
                    </span>
                  </div>
                </div>
                {#if index < route.points.length - 1}
                  <div class="point-line"></div>
                {/if}
              {/each}
            </div>
          {/if}

          <div class="route-footer">
            <a href="#/map" use:link class="view-map-link">
              在地图中查看 →
            </a>
          </div>
        </div>
      {/each}
    </div>
  {/if}

  <div class="cta-section card">
    <div class="cta-content">
      <h3>💡 有好的探索路线？</h3>
      <p>分享你的探索路线，帮助其他废墟爱好者发现更多精彩地点</p>
    </div>
    <button class="btn btn-primary">
      + 创建路线
    </button>
  </div>
</div>

<style>
  .routes-page {
    padding: 40px 20px 60px;
    max-width: 1000px;
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
    font-size: 15px;
  }

  .loading-state {
    text-align: center;
    padding: 80px 20px;
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

  .empty-state {
    text-align: center;
    padding: 80px 20px;
  }

  .empty-icon {
    font-size: 64px;
    margin-bottom: 16px;
    opacity: 0.5;
  }

  .empty-state p {
    font-size: 16px;
    color: var(--text-main);
    margin-bottom: 8px;
  }

  .routes-grid {
    margin-bottom: 40px;
  }

  .route-card {
    display: flex;
    flex-direction: column;
  }

  .route-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 12px;
  }

  .route-title {
    font-size: 18px;
    color: var(--text-bright);
  }

  .difficulty-badge {
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 500;
    flex-shrink: 0;
  }

  .difficulty-badge.easy {
    background: rgba(74, 124, 89, 0.2);
    color: var(--moss-pale);
    border: 1px solid var(--moss-dark);
  }

  .difficulty-badge.medium {
    background: rgba(212, 160, 64, 0.2);
    color: #d4a040;
    border: 1px solid #8b6914;
  }

  .difficulty-badge.hard {
    background: rgba(183, 65, 14, 0.2);
    color: var(--rust-light);
    border: 1px solid var(--rust-dark);
  }

  .route-desc {
    font-size: 14px;
    color: var(--text-muted);
    line-height: 1.6;
    margin-bottom: 16px;
  }

  .route-meta {
    display: flex;
    gap: 16px;
    padding-bottom: 16px;
    border-bottom: 1px dashed var(--border-color);
    margin-bottom: 16px;
  }

  .meta-item {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 12px;
    color: var(--text-muted);
  }

  .meta-icon {
    font-size: 14px;
  }

  .route-points {
    flex: 1;
    margin-bottom: 16px;
  }

  .point-item {
    display: flex;
    gap: 12px;
    align-items: flex-start;
  }

  .point-number {
    width: 24px;
    height: 24px;
    border-radius: 50%;
    background: var(--rust-mid);
    color: white;
    font-size: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    font-weight: bold;
  }

  .point-info {
    flex: 1;
    padding-bottom: 4px;
  }

  .point-desc {
    font-size: 13px;
    color: var(--text-main);
    margin-bottom: 2px;
  }

  .point-coords {
    font-size: 11px;
    color: var(--text-muted);
    font-family: monospace;
  }

  .point-line {
    width: 2px;
    height: 16px;
    background: var(--border-color);
    margin-left: 11px;
  }

  .route-footer {
    padding-top: 12px;
    border-top: 1px solid var(--border-color);
  }

  .view-map-link {
    font-size: 13px;
    color: var(--rust-light);
    text-decoration: none;
  }

  .view-map-link:hover {
    color: var(--rust-bright);
  }

  .cta-section {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 30px;
    background: linear-gradient(135deg, var(--bg-card), var(--bg-mid));
  }

  .cta-content h3 {
    font-size: 18px;
    margin-bottom: 6px;
  }

  .cta-content p {
    font-size: 14px;
    color: var(--text-muted);
  }

  @media (max-width: 768px) {
    .routes-grid {
      grid-template-columns: 1fr;
    }

    .cta-section {
      flex-direction: column;
      gap: 16px;
      text-align: center;
    }
  }
</style>
