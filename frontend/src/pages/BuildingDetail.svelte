<script>
  import { onMount, onDestroy } from 'svelte'
  import { link } from 'svelte-spa-router'
  import dayjs from 'dayjs'
  import { buildingsAPI, commentsAPI, mediaAPI } from '../api/modules'
  import { auth } from '../stores/auth'
  import Timeline from '../components/Timeline.svelte'

  export let params

  let building = null
  let comments = []
  let loading = true
  let commentText = ''
  let commentRating = 5
  let submittingComment = false

  let activeTab = 'info'

  let lightboxOpen = false
  let lightboxIndex = 0

  function openLightbox(index) {
    lightboxIndex = index
    lightboxOpen = true
    document.body.style.overflow = 'hidden'
  }

  function closeLightbox() {
    lightboxOpen = false
    document.body.style.overflow = ''
  }

  function prevPhoto() {
    if (building.photos.length === 0) return
    lightboxIndex = (lightboxIndex - 1 + building.photos.length) % building.photos.length
  }

  function nextPhoto() {
    if (building.photos.length === 0) return
    lightboxIndex = (lightboxIndex + 1) % building.photos.length
  }

  function handleKeydown(e) {
    if (!lightboxOpen) return
    if (e.key === 'Escape') closeLightbox()
    if (e.key === 'ArrowLeft') prevPhoto()
    if (e.key === 'ArrowRight') nextPhoto()
  }

  onMount(async () => {
    await loadBuilding()
    await loadComments()
    window.addEventListener('keydown', handleKeydown)
  })

  onDestroy(() => {
    window.removeEventListener('keydown', handleKeydown)
    document.body.style.overflow = ''
  })

  async function loadBuilding() {
    try {
      building = await buildingsAPI.getById(params.id)
    } catch (e) {
      console.error('加载建筑详情失败', e)
    }
  }

  async function loadComments() {
    try {
      comments = await commentsAPI.getByBuilding(params.id)
    } catch (e) {
      console.error('加载评论失败', e)
    } finally {
      loading = false
    }
  }

  async function submitComment() {
    if (!commentText.trim()) return
    if (!$auth.isAuthenticated) {
      alert('请先登录后再评论')
      return
    }

    submittingComment = true
    try {
      await commentsAPI.create(params.id, {
        content: commentText,
        rating: commentRating
      })
      commentText = ''
      commentRating = 5
      await loadComments()
    } catch (e) {
      console.error('评论失败', e)
      alert('评论失败，请重试')
    } finally {
      submittingComment = false
    }
  }

  $: dangerLevelText = building ? getDangerText(building.danger_level) : ''

  function getDangerText(level) {
    const texts = ['', '安全', '注意', '危险', '高危', '极危']
    return texts[level] || '未知'
  }

  function formatDate(dateStr) {
    return dayjs(dateStr).format('YYYY年MM月DD日')
  }
</script>

<div class="building-detail-page">
  {#if loading}
    <div class="loading-state container">
      <div class="loading-spinner"></div>
      <p>加载中...</p>
    </div>
  {:else if building}
    <div class="detail-header">
      <div class="container">
        <nav class="breadcrumb">
          <a href="#/buildings" use:link>建筑档案</a>
          <span class="breadcrumb-sep">›</span>
          <span class="current">{building.title}</span>
        </nav>

        <div class="header-content">
          <div class="title-section">
            <h1 class="building-title">{building.title}</h1>
            <div class="building-tags">
              <span class="badge badge-moss">{building.building_type}</span>
              <span class="badge badge-rust">危险等级 {building.danger_level} - {dangerLevelText}</span>
              <span class="badge badge-cement">👁 {building.explore_count} 次探索</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="container detail-content">
      <div class="detail-main">
        <div class="tabs">
          <button 
            class="tab-btn {activeTab === 'info' ? 'active' : ''}"
            on:click={() => activeTab = 'info'}
          >
            基本信息
          </button>
          <button 
            class="tab-btn {activeTab === 'history' ? 'active' : ''}"
            on:click={() => activeTab = 'history'}
          >
            历史背景
          </button>
          <button 
            class="tab-btn {activeTab === 'media' ? 'active' : ''}"
            on:click={() => activeTab = 'media'}
          >
            照片/视频
          </button>
          <button 
            class="tab-btn {activeTab === 'hazards' ? 'active' : ''}"
            on:click={() => activeTab = 'hazards'}
          >
            安全隐患
          </button>
          <button 
            class="tab-btn {activeTab === 'comments' ? 'active' : ''}"
            on:click={() => activeTab = 'comments'}
          >
            探索心得 ({comments.length})
          </button>
        </div>

        <div class="tab-content card">
          {#if activeTab === 'info'}
            <div class="info-section">
              <h3 class="info-title">📋 建筑信息</h3>
              <div class="info-grid">
                <div class="info-item">
                  <span class="info-label">建筑类型</span>
                  <span class="info-value">{building.building_type}</span>
                </div>
                <div class="info-item">
                  <span class="info-label">建设年代</span>
                  <span class="info-value">{building.construction_year || '未知'} 年</span>
                </div>
                <div class="info-item">
                  <span class="info-label">废弃时间</span>
                  <span class="info-value">{building.abandonment_year || '未知'} 年</span>
                </div>
                <div class="info-item">
                  <span class="info-label">危险等级</span>
                  <span class="info-value danger-{building.danger_level}">
                    {dangerLevelText} ({building.danger_level}级)
                  </span>
                </div>
                <div class="info-item full-width">
                  <span class="info-label">详细地址</span>
                  <span class="info-value">📍 {building.address}</span>
                </div>
                <div class="info-item full-width">
                  <span class="info-label">坐标位置</span>
                  <span class="info-value">
                    {building.latitude.toFixed(4)}, {building.longitude.toFixed(4)}
                  </span>
                </div>
              </div>

              <div class="divider"></div>

              <h3 class="info-title">📝 简介</h3>
              <p class="description-text">{building.description}</p>

              {#if building.tags && building.tags.length > 0}
                <div class="tag-section">
                  <span class="info-label">标签</span>
                  <div class="tags-list">
                    {#each building.tags as tag}
                      <span class="badge badge-rust">#{tag.tag}</span>
                    {/each}
                  </div>
                </div>
              {/if}
            </div>

          {:else if activeTab === 'history'}
            <div class="history-section">
              <h3 class="info-title">📜 历史背景</h3>
              {#if building.history}
                <div class="history-content">
                  {building.history}
                </div>
              {:else}
                <p class="text-muted">暂无历史背景介绍</p>
              {/if}

              <div class="divider"></div>

              <h3 class="info-title">🗓️ 建筑编年史</h3>
              <Timeline buildingId={params.id} />
            </div>

          {:else if activeTab === 'media'}
            <div class="media-section">
              <h3 class="info-title">📷 实拍照片</h3>
              {#if building.photos && building.photos.length > 0}
                <div class="photo-grid grid grid-3">
                  {#each building.photos as photo, index}
                    <div class="photo-item" on:click={() => openLightbox(index)}>
                      <div class="photo-wrapper">
                        <img 
                          src={photo.url} 
                          alt={photo.caption || building.title}
                          class="photo-image"
                        />
                        <div class="photo-overlay">
                          <span class="zoom-icon">🔍</span>
                        </div>
                      </div>
                      {#if photo.caption}
                        <p class="photo-caption">{photo.caption}</p>
                      {/if}
                    </div>
                  {/each}
                </div>
              {:else}
                <p class="text-muted">暂无照片，成为第一个上传照片的探索者吧！</p>
              {/if}

              <div class="divider"></div>

              <h3 class="info-title">🎬 视频记录</h3>
              {#if building.videos && building.videos.length > 0}
                <div class="video-list">
                  {#each building.videos as video}
                    <div class="video-item card">
                      <div class="video-thumbnail">
                        <span class="play-icon">▶</span>
                      </div>
                      <div class="video-info">
                        <h4>{video.title}</h4>
                        <p class="text-muted">{video.description}</p>
                      </div>
                    </div>
                  {/each}
                </div>
              {:else}
                <p class="text-muted">暂无视频记录</p>
              {/if}
            </div>

          {:else if activeTab === 'hazards'}
            <div class="hazards-section">
              <h3 class="info-title">⚠️ 安全隐患标注</h3>
              {#if building.hazards && building.hazards.length > 0}
                <div class="hazard-list">
                  {#each building.hazards as hazard}
                    <div class="hazard-item">
                      <div class="hazard-severity severity-{hazard.severity}">
                        <span>{hazard.severity}</span>
                      </div>
                      <div class="hazard-info">
                        <h4>{hazard.hazard_type}</h4>
                        <p class="text-muted">{hazard.description}</p>
                        {#if hazard.location}
                          <span class="hazard-location">📍 {hazard.location}</span>
                        {/if}
                      </div>
                    </div>
                  {/each}
                </div>
              {:else}
                <p class="text-muted">暂无安全隐患标注，了解情况的探索者可以补充</p>
              {/if}

              <div class="warning-box">
                <span class="warning-icon">⚠️</span>
                <div>
                  <strong>安全提示：</strong>
                  <p>废墟探索存在风险，请务必注意安全，结伴出行。
                  进入建筑前仔细观察结构稳定性，做好防护措施。</p>
                </div>
              </div>
            </div>

          {:else if activeTab === 'comments'}
            <div class="comments-section">
              <h3 class="info-title">💬 探索心得分享</h3>

              {#if $auth.isAuthenticated}
                <div class="comment-form">
                  <div class="rating-input">
                    <span class="rating-label">评分：</span>
                    {#each [5,4,3,2,1] as star}
                      <button 
                        class="star-btn {star <= commentRating ? 'active' : ''}"
                        on:click={() => commentRating = star}
                      >
                        ★
                      </button>
                    {/each}
                  </div>
                  <textarea
                    bind:value={commentText}
                    placeholder="分享你的探索心得..."
                    rows="4"
                  ></textarea>
                  <div class="form-actions">
                    <span class="char-count">{commentText.length} 字</span>
                    <button 
                      class="btn btn-primary"
                      disabled={submittingComment || !commentText.trim()}
                      on:click={submitComment}
                    >
                      {submittingComment ? '发布中...' : '发布心得'}
                    </button>
                  </div>
                </div>
              {:else}
                <div class="login-prompt">
                  <p>请 <a href="#/login" use:link>登录</a> 后分享你的探索心得</p>
                </div>
              {/if}

              <div class="comments-list">
                {#if comments.length === 0}
                  <p class="text-muted empty-comments">还没有心得，来分享第一条吧！</p>
                {:else}
                  {#each comments as comment}
                    <div class="comment-item">
                      <div class="comment-avatar">
                        {comment.user?.username?.[0] || '?'}
                      </div>
                      <div class="comment-body">
                        <div class="comment-header">
                          <span class="comment-author">{comment.user?.username}</span>
                          <div class="comment-rating">
                            {#each {length: comment.rating} as _, i}
                              <span class="star">★</span>
                            {/each}
                          </div>
                          <span class="comment-time">{formatDate(comment.created_at)}</span>
                        </div>
                        <p class="comment-content">{comment.content}</p>
                        <div class="comment-actions">
                          <button class="action-btn">👍 {comment.likes}</button>
                          <button class="action-btn">💬 回复</button>
                        </div>
                      </div>
                    </div>
                  {/each}
                {/if}
              </div>
            </div>
          {/if}
        </div>
      </div>

      <div class="detail-sidebar">
        <div class="sidebar-card card">
          <h3 class="sidebar-title">📍 位置信息</h3>
          <div class="map-placeholder">
            <span class="map-icon">🗺️</span>
            <p class="text-muted">地图视图</p>
            <a href="#/map" use:link class="map-link">在地图中查看 →</a>
          </div>
          <p class="address-text">{building.address}</p>
        </div>

        <div class="sidebar-card card">
          <h3 class="sidebar-title">👤 档案建立者</h3>
          <div class="owner-info">
            <div class="owner-avatar">{building.owner?.username?.[0] || '?'}</div>
            <div class="owner-detail">
              <p class="owner-name">{building.owner?.username || '匿名'}</p>
              <p class="text-muted">创建于 {formatDate(building.created_at)}</p>
            </div>
          </div>
        </div>

        <div class="sidebar-card card action-card">
          <h3 class="sidebar-title">🛠️ 操作</h3>
          <button class="btn btn-secondary w-full mb-2">📷 上传照片</button>
          <button class="btn btn-secondary w-full mb-2">🎬 上传视频</button>
          <button class="btn btn-secondary w-full">⚠️ 标注隐患</button>
        </div>
      </div>
    </div>

    {#if lightboxOpen && building.photos && building.photos.length > 0}
      <div class="lightbox" on:click|self={closeLightbox}>
        <button class="lightbox-close" on:click={closeLightbox}>&times;</button>
        <button class="lightbox-nav lightbox-prev" on:click={prevPhoto}>&#10094;</button>
        <button class="lightbox-nav lightbox-next" on:click={nextPhoto}>&#10095;</button>
        <div class="lightbox-content">
          <img 
            src={building.photos[lightboxIndex].url} 
            alt={building.photos[lightboxIndex].caption || building.title}
            class="lightbox-image"
          />
          {#if building.photos[lightboxIndex].caption}
            <p class="lightbox-caption">{building.photos[lightboxIndex].caption}</p>
          {/if}
          <div class="lightbox-counter">
            {lightboxIndex + 1} / {building.photos.length}
          </div>
        </div>
      </div>
    {/if}
  {/if}
</div>

<style>
  .building-detail-page {
    padding-bottom: 60px;
  }

  .detail-header {
    background: 
      linear-gradient(135deg, var(--bg-mid) 0%, var(--bg-dark) 100%);
    border-bottom: 1px solid var(--border-color);
    padding: 30px 0 40px;
    position: relative;
  }

  .detail-header::before {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    height: 2px;
    background: linear-gradient(90deg, 
      transparent, var(--rust-mid), var(--moss-mid), transparent
    );
  }

  .breadcrumb {
    font-size: 13px;
    color: var(--text-muted);
    margin-bottom: 20px;
  }

  .breadcrumb a {
    color: var(--text-muted);
    text-decoration: none;
  }

  .breadcrumb a:hover {
    color: var(--rust-light);
  }

  .breadcrumb-sep {
    margin: 0 8px;
  }

  .breadcrumb .current {
    color: var(--text-bright);
  }

  .building-title {
    font-size: 32px;
    margin-bottom: 12px;
  }

  .building-tags {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
  }

  .detail-content {
    padding-top: 30px;
    display: grid;
    grid-template-columns: 1fr 320px;
    gap: 30px;
  }

  .tabs {
    display: flex;
    gap: 4px;
    margin-bottom: 20px;
    border-bottom: 2px solid var(--border-color);
    overflow-x: auto;
  }

  .tab-btn {
    background: none;
    border: none;
    color: var(--text-muted);
    padding: 12px 20px;
    font-size: 14px;
    cursor: pointer;
    position: relative;
    white-space: nowrap;
    transition: color 0.3s ease;
  }

  .tab-btn:hover {
    color: var(--text-main);
  }

  .tab-btn.active {
    color: var(--rust-light);
  }

  .tab-btn.active::after {
    content: '';
    position: absolute;
    bottom: -2px;
    left: 0;
    right: 0;
    height: 2px;
    background: var(--rust-mid);
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

  .info-section, .history-section, .media-section, 
  .hazards-section, .comments-section {
    padding: 10px;
  }

  .info-title {
    font-size: 18px;
    margin-bottom: 20px;
    color: var(--text-bright);
  }

  .info-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
  }

  .info-item {
    display: flex;
    flex-direction: column;
    gap: 6px;
  }

  .info-item.full-width {
    grid-column: 1 / -1;
  }

  .info-label {
    font-size: 12px;
    color: var(--text-muted);
    letter-spacing: 1px;
  }

  .info-value {
    font-size: 15px;
    color: var(--text-main);
  }

  .danger-1 { color: var(--moss-pale); }
  .danger-2 { color: #d4a040; }
  .danger-3 { color: var(--rust-light); }
  .danger-4 { color: #dc4c2e; }
  .danger-5 { color: #ff3030; }

  .description-text {
    line-height: 1.8;
    color: var(--text-main);
    font-size: 14px;
  }

  .tag-section {
    margin-top: 20px;
    display: flex;
    align-items: flex-start;
    gap: 12px;
  }

  .tags-list {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
  }

  .history-content {
    line-height: 2;
    color: var(--text-main);
    font-size: 15px;
    text-indent: 2em;
    margin-bottom: 30px;
  }

  .photo-grid {
    margin-bottom: 30px;
  }

  .photo-item {
    border-radius: 4px;
    overflow: hidden;
    cursor: pointer;
  }

  .photo-wrapper {
    aspect-ratio: 4/3;
    position: relative;
    overflow: hidden;
    background: linear-gradient(135deg, var(--cement-mid), var(--cement-dark));
  }

  .photo-image {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
    transition: transform 0.3s ease;
  }

  .photo-item:hover .photo-image {
    transform: scale(1.05);
  }

  .photo-overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.4);
    display: flex;
    align-items: center;
    justify-content: center;
    opacity: 0;
    transition: opacity 0.3s ease;
  }

  .photo-item:hover .photo-overlay {
    opacity: 1;
  }

  .zoom-icon {
    font-size: 32px;
    color: #fff;
  }

  .photo-caption {
    padding: 10px;
    font-size: 13px;
    color: var(--text-muted);
    background: var(--bg-mid);
  }

  .lightbox {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.9);
    z-index: 1000;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 40px;
  }

  .lightbox-close {
    position: absolute;
    top: 20px;
    right: 30px;
    background: none;
    border: none;
    color: #fff;
    font-size: 40px;
    cursor: pointer;
    z-index: 1001;
    line-height: 1;
    opacity: 0.8;
    transition: opacity 0.2s ease;
  }

  .lightbox-close:hover {
    opacity: 1;
  }

  .lightbox-nav {
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
    background: rgba(255, 255, 255, 0.1);
    border: none;
    color: #fff;
    font-size: 30px;
    width: 50px;
    height: 50px;
    border-radius: 50%;
    cursor: pointer;
    z-index: 1001;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: background 0.2s ease;
  }

  .lightbox-nav:hover {
    background: rgba(255, 255, 255, 0.2);
  }

  .lightbox-prev {
    left: 20px;
  }

  .lightbox-next {
    right: 20px;
  }

  .lightbox-content {
    max-width: 90vw;
    max-height: 85vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 16px;
  }

  .lightbox-image {
    max-width: 100%;
    max-height: 75vh;
    object-fit: contain;
    border-radius: 4px;
  }

  .lightbox-caption {
    color: #fff;
    font-size: 14px;
    text-align: center;
    margin: 0;
  }

  .lightbox-counter {
    color: rgba(255, 255, 255, 0.7);
    font-size: 13px;
  }

  .video-list {
    display: flex;
    flex-direction: column;
    gap: 12px;
  }

  .video-item {
    display: flex;
    gap: 16px;
    padding: 16px;
  }

  .video-thumbnail {
    width: 120px;
    height: 80px;
    background: linear-gradient(135deg, var(--cement-mid), var(--cement-dark));
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 4px;
    flex-shrink: 0;
  }

  .play-icon {
    font-size: 24px;
    opacity: 0.7;
  }

  .video-info h4 {
    font-size: 14px;
    margin-bottom: 6px;
  }

  .video-info p {
    font-size: 12px;
    line-height: 1.5;
  }

  .hazard-list {
    display: flex;
    flex-direction: column;
    gap: 16px;
    margin-bottom: 30px;
  }

  .hazard-item {
    display: flex;
    gap: 16px;
    padding: 16px;
    background: var(--bg-mid);
    border-radius: 6px;
    border-left: 4px solid var(--border-color);
  }

  .hazard-item.severity-1 { border-left-color: var(--moss-mid); }
  .hazard-item.severity-2 { border-left-color: #d4a040; }
  .hazard-item.severity-3 { border-left-color: var(--rust-mid); }
  .hazard-item.severity-4 { border-left-color: #dc4c2e; }
  .hazard-item.severity-5 { border-left-color: #ff3030; }

  .hazard-severity {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    color: white;
    flex-shrink: 0;
  }

  .severity-1 { background: var(--moss-mid); }
  .severity-2 { background: #d4a040; }
  .severity-3 { background: var(--rust-mid); }
  .severity-4 { background: #dc4c2e; }
  .severity-5 { background: #ff3030; }

  .hazard-info h4 {
    font-size: 15px;
    margin-bottom: 6px;
  }

  .hazard-info p {
    font-size: 13px;
    margin-bottom: 6px;
  }

  .hazard-location {
    font-size: 12px;
    color: var(--moss-pale);
  }

  .warning-box {
    display: flex;
    gap: 16px;
    padding: 20px;
    background: rgba(183, 65, 14, 0.1);
    border: 1px solid var(--rust-dark);
    border-radius: 6px;
  }

  .warning-icon {
    font-size: 28px;
    flex-shrink: 0;
  }

  .warning-box strong {
    display: block;
    margin-bottom: 6px;
    color: var(--rust-light);
  }

  .warning-box p {
    font-size: 13px;
    line-height: 1.6;
    color: var(--text-muted);
  }

  .comment-form {
    margin-bottom: 30px;
    padding: 20px;
    background: var(--bg-mid);
    border-radius: 6px;
  }

  .rating-input {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 12px;
  }

  .rating-label {
    font-size: 13px;
    color: var(--text-muted);
  }

  .star-btn {
    background: none;
    border: none;
    font-size: 22px;
    color: var(--border-color);
    cursor: pointer;
    padding: 2px;
  }

  .star-btn.active {
    color: #ffb800;
  }

  .comment-form textarea {
    width: 100%;
    resize: vertical;
    min-height: 100px;
  }

  .form-actions {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 12px;
  }

  .char-count {
    font-size: 12px;
    color: var(--text-muted);
  }

  .login-prompt {
    text-align: center;
    padding: 30px;
    background: var(--bg-mid);
    border-radius: 6px;
    margin-bottom: 30px;
  }

  .comments-list {
    display: flex;
    flex-direction: column;
    gap: 20px;
  }

  .empty-comments {
    text-align: center;
    padding: 30px;
  }

  .comment-item {
    display: flex;
    gap: 16px;
  }

  .comment-avatar {
    width: 44px;
    height: 44px;
    border-radius: 50%;
    background: linear-gradient(135deg, var(--rust-dark), var(--rust-mid));
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-weight: bold;
    flex-shrink: 0;
  }

  .comment-body {
    flex: 1;
    padding-bottom: 16px;
    border-bottom: 1px solid var(--border-color);
  }

  .comment-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 8px;
  }

  .comment-author {
    font-weight: 500;
    color: var(--text-bright);
  }

  .comment-rating .star {
    color: #ffb800;
    font-size: 12px;
  }

  .comment-time {
    font-size: 12px;
    color: var(--text-muted);
    margin-left: auto;
  }

  .comment-content {
    font-size: 14px;
    line-height: 1.7;
    color: var(--text-main);
    margin-bottom: 10px;
  }

  .comment-actions {
    display: flex;
    gap: 16px;
  }

  .action-btn {
    background: none;
    border: none;
    color: var(--text-muted);
    font-size: 13px;
    cursor: pointer;
    padding: 4px 8px;
    border-radius: 4px;
  }

  .action-btn:hover {
    color: var(--rust-light);
    background: rgba(183, 65, 14, 0.1);
  }

  .detail-sidebar {
    position: sticky;
    top: 90px;
    align-self: flex-start;
    display: flex;
    flex-direction: column;
    gap: 20px;
  }

  .sidebar-card {
    padding: 20px;
  }

  .sidebar-title {
    font-size: 15px;
    margin-bottom: 16px;
    padding-bottom: 10px;
    border-bottom: 1px solid var(--border-color);
  }

  .map-placeholder {
    aspect-ratio: 1;
    background: linear-gradient(135deg, var(--bg-mid), var(--bg-dark));
    border-radius: 6px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 10px;
    margin-bottom: 12px;
    border: 1px dashed var(--border-color);
  }

  .map-icon {
    font-size: 40px;
    opacity: 0.6;
  }

  .map-link {
    font-size: 12px;
    color: var(--rust-light);
    text-decoration: none;
  }

  .address-text {
    font-size: 13px;
    color: var(--text-muted);
    line-height: 1.5;
  }

  .owner-info {
    display: flex;
    gap: 12px;
    align-items: center;
  }

  .owner-avatar {
    width: 48px;
    height: 48px;
    border-radius: 50%;
    background: linear-gradient(135deg, var(--moss-dark), var(--moss-mid));
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-weight: bold;
    font-size: 18px;
  }

  .owner-name {
    font-size: 15px;
    color: var(--text-bright);
    margin-bottom: 2px;
  }

  .owner-detail p {
    font-size: 12px;
  }

  .action-card .btn {
    padding: 10px;
    font-size: 13px;
  }

  .mb-2 {
    margin-bottom: 10px;
  }

  .w-full {
    width: 100%;
  }

  @media (max-width: 900px) {
    .detail-content {
      grid-template-columns: 1fr;
    }

    .detail-sidebar {
      position: static;
    }
  }

  @media (max-width: 600px) {
    .info-grid {
      grid-template-columns: 1fr;
    }

    .building-title {
      font-size: 24px;
    }
  }
</style>
