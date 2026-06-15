<script>
  import { link } from 'svelte-spa-router'
  import dayjs from 'dayjs'

  export let building
</script>

<article class="building-card card">
  <a href={`#/buildings/${building.id}`} use:link class="card-link">
    <div class="card-image">
      <div class="image-placeholder">
        <span class="building-type-badge">{building.building_type}</span>
        <div class="danger-indicator danger-{building.danger_level}">
          <span class="danger-icon">⚠</span>
          <span class="danger-text">危险等级 {building.danger_level}</span>
        </div>
        <div class="card-overlay">
          <div class="overlay-icon">🔍</div>
          <span>查看详情</span>
        </div>
      </div>
    </div>

    <div class="card-content">
      <h3 class="card-title">{building.title}</h3>
      
      <p class="card-description">{building.description}</p>

      <div class="card-meta">
        <div class="meta-item">
          <span class="meta-icon">📍</span>
          <span class="meta-text">{building.address}</span>
        </div>

        <div class="meta-footer">
          <div class="meta-item">
            <span class="meta-icon">👁️</span>
            <span class="meta-text">{building.explore_count} 次探索</span>
          </div>
          
          {#if building.construction_year}
            <div class="meta-item">
              <span class="meta-icon">🏗️</span>
              <span class="meta-text">{building.construction_year}年</span>
            </div>
          {/if}
        </div>
      </div>

      {#if building.tags && building.tags.length > 0}
        <div class="card-tags">
          {#each building.tags.slice(0, 3) as tag}
            <span class="badge badge-rust">#{tag.tag}</span>
          {/each}
        </div>
      {/if}
    </div>
  </a>
</article>

<style>
  .building-card {
    padding: 0;
    overflow: hidden;
  }

  .card-link {
    display: block;
    text-decoration: none;
    color: inherit;
  }

  .card-image {
    position: relative;
    height: 200px;
    overflow: hidden;
  }

  .image-placeholder {
    width: 100%;
    height: 100%;
    background: 
      linear-gradient(135deg, var(--cement-mid) 0%, var(--cement-dark) 100%);
    position: relative;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding: 16px;
  }

  .image-placeholder::before {
    content: '🏚️';
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    font-size: 60px;
    opacity: 0.3;
    filter: grayscale(100%);
  }

  .building-type-badge {
    align-self: flex-start;
    background: linear-gradient(135deg, var(--moss-dark), var(--moss-mid));
    color: var(--text-bright);
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 12px;
    z-index: 2;
    border: 1px solid var(--moss-light);
  }

  .danger-indicator {
    align-self: flex-start;
    display: flex;
    align-items: center;
    gap: 4px;
    padding: 4px 10px;
    border-radius: 4px;
    font-size: 11px;
    z-index: 2;
  }

  .danger-1 {
    background: rgba(74, 124, 89, 0.8);
    color: var(--text-bright);
  }

  .danger-2 {
    background: rgba(180, 140, 60, 0.8);
    color: var(--text-bright);
  }

  .danger-3 {
    background: rgba(183, 65, 14, 0.8);
    color: var(--text-bright);
  }

  .danger-4 {
    background: rgba(139, 37, 0, 0.9);
    color: var(--text-bright);
  }

  .danger-5 {
    background: linear-gradient(135deg, #4a0000, #8b0000);
    color: #fff;
    animation: pulse 2s infinite;
  }

  @keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.7; }
  }

  .card-overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.6);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 10px;
    opacity: 0;
    transition: opacity 0.3s ease;
    color: var(--text-bright);
    font-size: 14px;
  }

  .overlay-icon {
    font-size: 36px;
  }

  .building-card:hover .card-overlay {
    opacity: 1;
  }

  .card-content {
    padding: 20px;
  }

  .card-title {
    font-size: 18px;
    margin-bottom: 10px;
    color: var(--text-bright);
    line-height: 1.4;
  }

  .card-description {
    color: var(--text-muted);
    font-size: 13px;
    line-height: 1.6;
    margin-bottom: 16px;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }

  .card-meta {
    border-top: 1px solid var(--border-color);
    padding-top: 12px;
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

  .meta-footer {
    display: flex;
    justify-content: space-between;
    margin-top: 8px;
  }

  .card-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    margin-top: 12px;
  }

  .building-card:hover .card-title {
    color: var(--rust-light);
  }
</style>
