<script>
  import { onMount } from 'svelte'
  import BuildingCard from '../components/BuildingCard.svelte'
  import { buildingsAPI } from '../api/modules'

  let buildings = []
  let total = 0
  let page = 1
  let pageSize = 12
  let loading = true

  let filters = {
    keyword: '',
    building_type: '',
    danger_level: null
  }

  let buildingTypes = []

  onMount(async () => {
    await loadBuildingTypes()
    await loadBuildings()
  })

  async function loadBuildingTypes() {
    try {
      const data = await buildingsAPI.getTypes()
      buildingTypes = data.types
    } catch (e) {
      console.error('加载建筑类型失败', e)
    }
  }

  async function loadBuildings() {
    loading = true
    try {
      const params = {
        page,
        page_size: pageSize
      }
      if (filters.keyword) params.keyword = filters.keyword
      if (filters.building_type) params.building_type = filters.building_type
      if (filters.danger_level !== null) params.danger_level = filters.danger_level

      const data = await buildingsAPI.getList(params)
      buildings = data.items
      total = data.total
    } catch (e) {
      console.error('加载建筑列表失败', e)
    } finally {
      loading = false
    }
  }

  function handleSearch() {
    page = 1
    loadBuildings()
  }

  function changePage(newPage) {
    page = newPage
    loadBuildings()
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  $: totalPages = Math.ceil(total / pageSize)
</script>

<div class="buildings-page container">
  <div class="page-header">
    <h1 class="page-title">建筑档案</h1>
    <p class="page-subtitle">探索城市中被遗忘的角落</p>
  </div>

  <div class="filters-section card">
    <div class="filters-grid">
      <div class="filter-item">
        <label class="filter-label">关键词搜索</label>
        <div class="search-input-wrapper">
          <input
            type="text"
            bind:value={filters.keyword}
            placeholder="搜索建筑名称、地址..."
            on:keydown={e => e.key === 'Enter' && handleSearch()}
          />
          <button class="search-btn" on:click={handleSearch}>🔍</button>
        </div>
      </div>

      <div class="filter-item">
        <label class="filter-label">建筑类型</label>
        <select bind:value={filters.building_type} on:change={handleSearch}>
          <option value="">全部类型</option>
          {#each buildingTypes as type}
            <option value={type}>{type}</option>
          {/each}
        </select>
      </div>

      <div class="filter-item">
        <label class="filter-label">危险等级</label>
        <select bind:value={filters.danger_level} on:change={handleSearch}>
          <option value={null}>全部等级</option>
          <option value={1}>1级 - 安全</option>
          <option value={2}>2级 - 注意</option>
          <option value={3}>3级 - 危险</option>
          <option value={4}>4级 - 高危</option>
          <option value={5}>5级 - 极危</option>
        </select>
      </div>
    </div>

    <div class="results-info">
      共找到 <span class="text-rust">{total}</span> 处废墟档案
    </div>
  </div>

  {#if loading}
    <div class="loading-state">
      <div class="loading-spinner"></div>
      <p>正在加载废墟档案...</p>
    </div>
  {:else if buildings.length === 0}
    <div class="empty-state">
      <div class="empty-icon">🏚️</div>
      <p>暂无符合条件的废墟档案</p>
      <p class="text-muted">试试调整筛选条件</p>
    </div>
  {:else}
    <div class="buildings-grid grid grid-3">
      {#each buildings as building (building.id)}
        <BuildingCard {building} />
      {/each}
    </div>

    {#if totalPages > 1}
      <div class="pagination">
        <button 
          class="page-btn" 
          disabled={page === 1}
          on:click={() => changePage(1)}
        >
          « 首页
        </button>
        <button 
          class="page-btn" 
          disabled={page === 1}
          on:click={() => changePage(page - 1)}
        >
          ‹ 上一页
        </button>

        <span class="page-info">
          第 {page} / {totalPages} 页
        </span>

        <button 
          class="page-btn" 
          disabled={page === totalPages}
          on:click={() => changePage(page + 1)}
        >
          下一页 ›
        </button>
        <button 
          class="page-btn" 
          disabled={page === totalPages}
          on:click={() => changePage(totalPages)}
        >
          末页 »
        </button>
      </div>
    {/if}
  {/if}
</div>

<style>
  .buildings-page {
    padding: 40px 20px;
  }

  .page-header {
    text-align: center;
    margin-bottom: 40px;
  }

  .page-title {
    font-size: 36px;
    margin-bottom: 8px;
  }

  .page-subtitle {
    color: var(--text-muted);
    font-size: 16px;
  }

  .filters-section {
    margin-bottom: 32px;
  }

  .filters-grid {
    display: grid;
    grid-template-columns: 2fr 1fr 1fr;
    gap: 20px;
    margin-bottom: 16px;
  }

  .filter-item {
    display: flex;
    flex-direction: column;
    gap: 8px;
  }

  .filter-label {
    font-size: 13px;
    color: var(--text-muted);
    letter-spacing: 1px;
  }

  .search-input-wrapper {
    position: relative;
  }

  .search-input-wrapper input {
    width: 100%;
    padding-right: 44px;
  }

  .search-btn {
    position: absolute;
    right: 4px;
    top: 50%;
    transform: translateY(-50%);
    background: none;
    border: none;
    font-size: 18px;
    cursor: pointer;
    padding: 6px 10px;
    border-radius: 4px;
    transition: background-color 0.2s;
  }

  .search-btn:hover {
    background-color: var(--bg-hover);
  }

  .results-info {
    font-size: 14px;
    color: var(--text-muted);
    padding-top: 12px;
    border-top: 1px solid var(--border-color);
  }

  .buildings-grid {
    margin-bottom: 40px;
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

  .pagination {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 12px;
    flex-wrap: wrap;
  }

  .page-btn {
    padding: 8px 16px;
    background-color: var(--bg-card);
    border: 1px solid var(--border-color);
    color: var(--text-main);
    border-radius: 4px;
    font-size: 13px;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .page-btn:hover:not(:disabled) {
    border-color: var(--rust-mid);
    color: var(--rust-light);
  }

  .page-btn:disabled {
    opacity: 0.4;
    cursor: not-allowed;
  }

  .page-info {
    font-size: 14px;
    color: var(--text-muted);
    padding: 0 16px;
  }

  @media (max-width: 768px) {
    .filters-grid {
      grid-template-columns: 1fr;
    }
  }
</style>
