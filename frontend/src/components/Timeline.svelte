<script>
  import { onMount } from 'svelte'
  import { timelineAPI } from '../api/modules'
  import { auth } from '../stores/auth'

  export let buildingId

  let events = []
  let loading = true
  let showForm = false
  let submitting = false

  let formYear = ''
  let formTitle = ''
  let formDescription = ''
  let formImageUrl = ''
  let formSource = ''

  let visibleItems = new Set()

  onMount(async () => {
    await loadEvents()
    setupObserver()
  })

  async function loadEvents() {
    try {
      events = await timelineAPI.getByBuilding(buildingId)
      visibleItems = new Set()
    } catch (e) {
      console.error('加载时间轴失败', e)
    } finally {
      loading = false
    }
  }

  function setupObserver() {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            const id = entry.target.dataset.id
            visibleItems = new Set([...visibleItems, id])
          }
        })
      },
      { threshold: 0.15, rootMargin: '0px 0px -50px 0px' }
    )

    setTimeout(() => {
      document.querySelectorAll('.timeline-item').forEach(el => {
        observer.observe(el)
      })
    }, 100)
  }

  async function submitEvent() {
    if (!formYear || !formTitle.trim()) return
    if (!$auth.isAuthenticated) {
      alert('请先登录后再添加事件')
      return
    }

    submitting = true
    try {
      await timelineAPI.create(buildingId, {
        year: parseInt(formYear),
        title: formTitle.trim(),
        description: formDescription.trim(),
        image_url: formImageUrl.trim(),
        source: formSource.trim()
      })
      formYear = ''
      formTitle = ''
      formDescription = ''
      formImageUrl = ''
      formSource = ''
      showForm = false
      await loadEvents()
      setupObserver()
    } catch (e) {
      console.error('添加事件失败', e)
      alert('添加事件失败，请重试')
    } finally {
      submitting = false
    }
  }

  async function deleteEvent(eventId) {
    if (!confirm('确定删除该事件？')) return
    try {
      await timelineAPI.delete(eventId)
      await loadEvents()
    } catch (e) {
      console.error('删除事件失败', e)
    }
  }

  function canDelete(event) {
    if (!$auth.isAuthenticated) return false
    return $auth.user?.id === event.submitted_by
  }

  function isVisible(id) {
    return visibleItems.has(String(id))
  }

  $: sortedEvents = [...events].sort((a, b) => a.year - b.year)
</script>

<div class="timeline-container">
  {#if loading}
    <div class="timeline-loading">
      <div class="loading-spinner"></div>
      <p>加载时间轴...</p>
    </div>
  {:else if sortedEvents.length === 0 && !showForm}
    <div class="timeline-empty">
      <div class="empty-icon">📜</div>
      <p>暂无历史事件记录</p>
      {#if $auth.isAuthenticated}
        <button class="btn btn-primary" on:click={() => showForm = true}>
          添加第一条事件
        </button>
      {/if}
    </div>
  {:else}
    <div class="timeline-actions">
      {#if $auth.isAuthenticated}
        <button class="btn btn-secondary" on:click={() => showForm = !showForm}>
          {showForm ? '取消' : '+ 添加历史事件'}
        </button>
      {/if}
    </div>

    {#if showForm}
      <div class="event-form card">
        <h4 class="form-title">添加历史事件</h4>
        <div class="form-grid">
          <div class="form-group">
            <label for="timeline-year">年份 *</label>
            <input id="timeline-year" type="number" bind:value={formYear} placeholder="例：1956" min="0" max="2100" />
          </div>
          <div class="form-group">
            <label for="timeline-title">事件标题 *</label>
            <input id="timeline-title" type="text" bind:value={formTitle} placeholder="例：工厂建成投产" maxlength="200" />
          </div>
          <div class="form-group full-width">
            <label for="timeline-desc">事件描述</label>
            <textarea id="timeline-desc" bind:value={formDescription} placeholder="描述该年份发生的重要事件..." rows="3"></textarea>
          </div>
          <div class="form-group">
            <label for="timeline-image">图片链接</label>
            <input id="timeline-image" type="text" bind:value={formImageUrl} placeholder="https://..." />
          </div>
          <div class="form-group">
            <label for="timeline-source">信息来源</label>
            <input id="timeline-source" type="text" bind:value={formSource} placeholder="例：地方志、口述历史" />
          </div>
        </div>
        <div class="form-footer">
          <button
            class="btn btn-primary"
            disabled={submitting || !formYear || !formTitle.trim()}
            on:click={submitEvent}
          >
            {submitting ? '提交中...' : '提交事件'}
          </button>
        </div>
      </div>
    {/if}

    <div class="timeline">
      <div class="timeline-line"></div>
      {#each sortedEvents as event, index (event.id)}
        <div class="timeline-item" data-id={event.id} class:visible={isVisible(event.id)}>
          <div class="timeline-node">
            <div class="node-dot {event.image_url ? 'has-image' : ''}"></div>
          </div>
          <div class="timeline-year">
            <span class="year-text">{event.year}</span>
          </div>
          <div class="timeline-content">
            <div class="event-card">
              <h4 class="event-title">{event.title}</h4>
              {#if event.description}
                <p class="event-desc">{event.description}</p>
              {/if}
              {#if event.image_url}
                <div class="event-image">
                  <img src={event.image_url} alt={event.title} loading="lazy" on:error|once={() => event.image_url = ''} />
                </div>
              {/if}
              {#if event.source}
                <span class="event-source">来源：{event.source}</span>
              {/if}
              {#if canDelete(event)}
                <div class="event-actions">
                  <button class="delete-btn" on:click={() => deleteEvent(event.id)} title="删除">✕</button>
                </div>
              {/if}
            </div>
          </div>
        </div>
      {/each}
    </div>
  {/if}
</div>

<style>
  .timeline-container {
    position: relative;
  }

  .timeline-loading {
    text-align: center;
    padding: 40px 20px;
    color: var(--text-muted);
  }

  .loading-spinner {
    width: 32px;
    height: 32px;
    border: 3px solid var(--border-color);
    border-top-color: var(--rust-mid);
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin: 0 auto 12px;
  }

  @keyframes spin {
    to { transform: rotate(360deg); }
  }

  .timeline-empty {
    text-align: center;
    padding: 50px 20px;
  }

  .empty-icon {
    font-size: 48px;
    margin-bottom: 16px;
    opacity: 0.4;
  }

  .timeline-empty p {
    color: var(--text-muted);
    margin-bottom: 20px;
  }

  .timeline-actions {
    display: flex;
    justify-content: flex-end;
    margin-bottom: 24px;
  }

  .event-form {
    margin-bottom: 30px;
    padding: 24px;
  }

  .form-title {
    font-size: 16px;
    margin-bottom: 20px;
    color: var(--rust-light);
  }

  .form-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
  }

  .form-group {
    display: flex;
    flex-direction: column;
    gap: 6px;
  }

  .form-group.full-width {
    grid-column: 1 / -1;
  }

  .form-group label {
    font-size: 12px;
    color: var(--text-muted);
    letter-spacing: 1px;
  }

  .form-group input,
  .form-group textarea {
    width: 100%;
  }

  .form-footer {
    margin-top: 20px;
    display: flex;
    justify-content: flex-end;
  }

  .timeline {
    position: relative;
    padding: 10px 0;
  }

  .timeline-line {
    position: absolute;
    left: 70px;
    top: 0;
    bottom: 0;
    width: 2px;
    background: linear-gradient(
      to bottom,
      transparent,
      var(--border-rust) 10%,
      var(--border-rust) 90%,
      transparent
    );
  }

  .timeline-item {
    position: relative;
    display: flex;
    align-items: flex-start;
    margin-bottom: 32px;
    opacity: 0;
    transform: translateY(20px);
    transition: opacity 0.6s ease, transform 0.6s ease;
  }

  .timeline-item.visible {
    opacity: 1;
    transform: translateY(0);
  }

  .timeline-item:last-child {
    margin-bottom: 0;
  }

  .timeline-node {
    position: relative;
    width: 20px;
    flex-shrink: 0;
    z-index: 2;
    margin-left: 61px;
  }

  .node-dot {
    width: 16px;
    height: 16px;
    border-radius: 50%;
    background: var(--rust-mid);
    border: 3px solid var(--bg-card);
    box-shadow: 0 0 0 2px var(--rust-dark);
    margin-top: 4px;
  }

  .node-dot.has-image {
    width: 20px;
    height: 20px;
    background: var(--moss-mid);
    box-shadow: 0 0 0 2px var(--moss-dark), 0 0 8px rgba(74, 124, 89, 0.4);
  }

  .timeline-year {
    width: 55px;
    flex-shrink: 0;
    text-align: right;
    padding-right: 16px;
  }

  .year-text {
    font-size: 18px;
    font-weight: 600;
    color: var(--rust-light);
    font-family: 'ZCOOL KuaiLe', cursive;
    letter-spacing: 1px;
  }

  .timeline-content {
    flex: 1;
    padding-left: 20px;
    min-width: 0;
  }

  .event-card {
    background: var(--bg-mid);
    border-radius: 6px;
    padding: 16px;
    border-left: 3px solid var(--rust-dark);
    position: relative;
    transition: border-color 0.3s ease, box-shadow 0.3s ease;
  }

  .event-card:hover {
    border-left-color: var(--rust-light);
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
  }

  .event-title {
    font-size: 15px;
    color: var(--text-bright);
    margin-bottom: 8px;
    letter-spacing: 1px;
  }

  .event-desc {
    font-size: 13px;
    color: var(--text-main);
    line-height: 1.7;
    margin-bottom: 10px;
  }

  .event-image {
    margin: 12px 0;
    border-radius: 4px;
    overflow: hidden;
    max-height: 200px;
  }

  .event-image img {
    width: 100%;
    max-height: 200px;
    object-fit: cover;
    border-radius: 4px;
  }

  .event-source {
    display: inline-block;
    font-size: 11px;
    color: var(--moss-pale);
    background: rgba(45, 90, 61, 0.15);
    padding: 2px 8px;
    border-radius: 3px;
  }

  .event-actions {
    position: absolute;
    top: 8px;
    right: 8px;
  }

  .delete-btn {
    background: none;
    border: none;
    color: var(--text-muted);
    font-size: 14px;
    cursor: pointer;
    padding: 4px 8px;
    border-radius: 3px;
    opacity: 0;
    transition: opacity 0.2s, color 0.2s;
  }

  .event-card:hover .delete-btn {
    opacity: 1;
  }

  .delete-btn:hover {
    color: var(--rust-light);
    background: rgba(183, 65, 14, 0.15);
  }

  @media (max-width: 600px) {
    .timeline-line {
      left: 30px;
    }

    .timeline-node {
      margin-left: 21px;
    }

    .timeline-year {
      display: none;
    }

    .timeline-content {
      padding-left: 12px;
    }

    .form-grid {
      grid-template-columns: 1fr;
    }
  }
</style>
