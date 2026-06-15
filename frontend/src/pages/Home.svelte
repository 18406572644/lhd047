<script>
  import { onMount } from 'svelte'
  import { link } from 'svelte-spa-router'
  import BuildingCard from '../components/BuildingCard.svelte'
  import { buildingsAPI, statsAPI } from '../api/modules'

  let hotBuildings = []
  let stats = null
  let loading = true

  onMount(async () => {
    try {
      const [hotData, statsData] = await Promise.all([
        buildingsAPI.getHot(6),
        statsAPI.getStats()
      ])
      hotBuildings = hotData
      stats = statsData
    } catch (e) {
      console.error('加载首页数据失败', e)
    } finally {
      loading = false
    }
  })

  const dangerLevels = [
    { level: 1, label: '安全', desc: '结构稳固，风险较低' },
    { level: 2, label: '注意', desc: '有一定风险，需小心' },
    { level: 3, label: '危险', desc: '结构松动，谨慎进入' },
    { level: 4, label: '高危', desc: '严重损坏，不建议进入' },
    { level: 5, label: '极危', desc: '随时可能坍塌，禁止进入' }
  ]
</script>

<div class="home-page">
  <section class="hero-section">
    <div class="hero-bg"></div>
    <div class="hero-content container">
      <div class="hero-text">
        <h1 class="hero-title">
          <span class="title-main">废墟档案</span>
          <span class="title-sub">城市遗忘角落的记录者</span>
        </h1>
        <p class="hero-desc">
          在钢筋水泥的丛林深处，有许多被时间遗忘的角落。
          废弃的工厂、沉默的医院、凋零的校园...
          每一座废墟都承载着一段历史，等待被重新发现。
        </p>
        <div class="hero-actions">
          <a href="#/buildings" use:link class="btn btn-primary btn-lg">
            开始探索 →
          </a>
          <a href="#/map" use:link class="btn btn-secondary btn-lg">
            查看地图
          </a>
        </div>
      </div>

      <div class="hero-stats">
        {#if stats}
          <div class="stat-item">
            <span class="stat-number">{stats.total_buildings}</span>
            <span class="stat-label">处废墟</span>
          </div>
          <div class="stat-item">
            <span class="stat-number">{stats.total_users}</span>
            <span class="stat-label">位探索者</span>
          </div>
          <div class="stat-item">
            <span class="stat-number">{stats.total_photos}</span>
            <span class="stat-label">张照片</span>
          </div>
          <div class="stat-item">
            <span class="stat-number">{stats.total_comments}</span>
            <span class="stat-label">条心得</span>
          </div>
        {/if}
      </div>
    </div>
  </section>

  <section class="section container">
    <div class="section-header">
      <h2 class="section-title">🔥 热门探索点</h2>
      <a href="#/buildings" use:link class="more-link">
        查看全部 →
      </a>
    </div>

    {#if loading}
      <div class="loading-state">加载中...</div>
    {:else}
      <div class="grid grid-3">
        {#each hotBuildings as building (building.id)}
          <BuildingCard {building} />
        {/each}
      </div>
    {/if}
  </section>

  <section class="section dark-section">
    <div class="container">
      <h2 class="section-title">⚠️ 安全指南</h2>
      <div class="safety-grid grid grid-3">
        {#each dangerLevels as level}
          <div class="safety-card card">
            <div class="safety-header danger-{level.level}">
              <span class="danger-number">{level.level}</span>
              <span class="danger-label">{level.label}</span>
            </div>
            <p class="safety-desc">{level.desc}</p>
          </div>
        {/each}
      </div>
    </div>
  </section>

  <section class="section container">
    <h2 class="section-title">📜 探索须知</h2>
    <div class="rules-grid grid grid-2">
      <div class="rule-card">
        <div class="rule-icon">🔒</div>
        <h3>遵守法律</h3>
        <p>请勿非法闯入私人领地，尊重产权。探险前确认场所的可进入性。</p>
      </div>
      <div class="rule-card">
        <div class="rule-icon">🛡️</div>
        <h3>安全第一</h3>
        <p>穿戴合适的防护装备，结伴出行。不冒险进入危险等级过高的建筑。</p>
      </div>
      <div class="rule-card">
        <div class="rule-icon">📸</div>
        <h3>只带走照片</h3>
        <p>除了照片什么都别带走，除了脚印什么都别留下。保护废墟原貌。</p>
      </div>
      <div class="rule-card">
        <div class="rule-icon">🤝</div>
        <h3>分享心得</h3>
        <p>记录你的发现和体验，分享给其他探索者，共同完善废墟档案。</p>
      </div>
    </div>
  </section>
</div>

<style>
  .home-page {
    padding-bottom: 0;
  }

  .hero-section {
    position: relative;
    min-height: 560px;
    display: flex;
    align-items: center;
    overflow: hidden;
  }

  .hero-bg {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: 
      linear-gradient(135deg, var(--bg-dark) 0%, rgba(28, 28, 26, 0.9) 100%),
      radial-gradient(circle at 20% 50%, rgba(139, 37, 0, 0.2) 0%, transparent 50%),
      radial-gradient(circle at 80% 80%, rgba(45, 90, 61, 0.15) 0%, transparent 40%);
  }

  .hero-bg::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 800 600' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M0,450 L100,400 L150,420 L200,380 L250,350 L300,400 L350,370 L400,300 L450,280 L500,350 L550,320 L600,280 L650,250 L700,300 L750,280 L800,260 L800,600 L0,600 Z' fill='%232a2a28' opacity='0.5'/%3E%3C/svg%3E");
    background-size: cover;
    background-position: bottom;
    opacity: 0.3;
  }

  .hero-content {
    position: relative;
    z-index: 1;
    padding-top: 60px;
    padding-bottom: 60px;
  }

  .hero-text {
    max-width: 640px;
    margin-bottom: 50px;
  }

  .hero-title {
    margin-bottom: 24px;
  }

  .title-main {
    display: block;
    font-family: 'ZCOOL KuaiLe', cursive;
    font-size: 56px;
    color: var(--text-bright);
    letter-spacing: 8px;
    line-height: 1.2;
    margin-bottom: 12px;
    text-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
  }

  .title-sub {
    display: block;
    font-size: 18px;
    color: var(--rust-light);
    letter-spacing: 6px;
  }

  .hero-desc {
    font-size: 16px;
    color: var(--text-muted);
    line-height: 1.8;
    margin-bottom: 32px;
  }

  .hero-actions {
    display: flex;
    gap: 16px;
    flex-wrap: wrap;
  }

  .btn-lg {
    padding: 14px 32px;
    font-size: 16px;
  }

  .hero-stats {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 20px;
    padding: 30px;
    background: rgba(46, 46, 44, 0.6);
    backdrop-filter: blur(10px);
    border: 1px solid var(--border-color);
    border-radius: 8px;
  }

  .stat-item {
    text-align: center;
  }

  .stat-number {
    display: block;
    font-family: 'ZCOOL KuaiLe', cursive;
    font-size: 42px;
    color: var(--rust-light);
    line-height: 1;
    margin-bottom: 8px;
  }

  .stat-label {
    display: block;
    font-size: 14px;
    color: var(--text-muted);
    letter-spacing: 2px;
  }

  .section {
    padding: 60px 0;
  }

  .dark-section {
    background-color: var(--bg-mid);
    border-top: 1px solid var(--border-color);
    border-bottom: 1px solid var(--border-color);
  }

  .section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 32px;
  }

  .section-title {
    margin-bottom: 0;
  }

  .more-link {
    color: var(--rust-light);
    text-decoration: none;
    font-size: 14px;
    transition: color 0.3s ease;
  }

  .more-link:hover {
    color: var(--rust-bright);
  }

  .loading-state {
    text-align: center;
    padding: 60px;
    color: var(--text-muted);
  }

  .safety-grid {
    margin-top: 30px;
  }

  .safety-card {
    text-align: center;
  }

  .safety-header {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 12px;
    margin-bottom: 12px;
    padding: 12px;
    border-radius: 6px;
  }

  .safety-header.danger-1 { background: rgba(74, 124, 89, 0.2); }
  .safety-header.danger-2 { background: rgba(180, 140, 60, 0.2); }
  .safety-header.danger-3 { background: rgba(183, 65, 14, 0.2); }
  .safety-header.danger-4 { background: rgba(139, 37, 0, 0.3); }
  .safety-header.danger-5 { background: rgba(75, 0, 0, 0.4); }

  .danger-number {
    font-family: 'ZCOOL KuaiLe', cursive;
    font-size: 32px;
    color: var(--text-bright);
  }

  .danger-label {
    font-size: 14px;
    color: var(--text-bright);
  }

  .safety-desc {
    font-size: 13px;
    color: var(--text-muted);
    line-height: 1.6;
  }

  .rules-grid {
    margin-top: 30px;
  }

  .rule-card {
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: 6px;
    padding: 30px;
    display: flex;
    flex-direction: column;
    gap: 12px;
  }

  .rule-icon {
    font-size: 40px;
    margin-bottom: 8px;
  }

  .rule-card h3 {
    font-size: 18px;
    color: var(--rust-light);
  }

  .rule-card p {
    font-size: 14px;
    color: var(--text-muted);
    line-height: 1.7;
  }

  @media (max-width: 768px) {
    .title-main {
      font-size: 36px;
    }

    .hero-stats {
      grid-template-columns: repeat(2, 1fr);
    }
  }

  @media (max-width: 480px) {
    .hero-stats {
      grid-template-columns: repeat(2, 1fr);
      gap: 15px;
      padding: 20px;
    }

    .stat-number {
      font-size: 28px;
    }
  }
</style>
