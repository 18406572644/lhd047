<script>
  import { push } from 'svelte-spa-router'
  import { onMount } from 'svelte'
  import { auth } from '../stores/auth'
  import { buildingsAPI } from '../api/modules'

  let formData = {
    title: '',
    description: '',
    history: '',
    construction_year: '',
    abandonment_year: '',
    building_type: '工厂',
    address: '',
    latitude: '',
    longitude: '',
    danger_level: 2,
    tags: ''
  }

  let buildingTypes = []
  let loading = false
  let error = ''
  let submitting = false

  onMount(() => {
    if (!$auth.isAuthenticated) {
      push('/login')
      return
    }
    loadBuildingTypes()
  })

  async function loadBuildingTypes() {
    try {
      const data = await buildingsAPI.getTypes()
      buildingTypes = data.types
    } catch (e) {
      console.error('加载建筑类型失败', e)
    }
  }

  function handleLocate() {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          formData.latitude = position.coords.latitude.toFixed(6)
          formData.longitude = position.coords.longitude.toFixed(6)
        },
        (err) => {
          alert('定位失败：' + err.message)
        }
      )
    } else {
      alert('浏览器不支持定位功能')
    }
  }

  async function handleSubmit() {
    if (!formData.title.trim()) {
      error = '请输入建筑名称'
      return
    }
    if (!formData.latitude || !formData.longitude) {
      error = '请填写经纬度坐标'
      return
    }

    submitting = true
    error = ''

    try {
      const tags = formData.tags
        .split(/[,，]/)
        .map(t => t.trim())
        .filter(t => t.length > 0)

      const data = await buildingsAPI.create({
        title: formData.title,
        description: formData.description,
        history: formData.history,
        construction_year: formData.construction_year ? parseInt(formData.construction_year) : null,
        abandonment_year: formData.abandonment_year ? parseInt(formData.abandonment_year) : null,
        building_type: formData.building_type,
        address: formData.address,
        latitude: parseFloat(formData.latitude),
        longitude: parseFloat(formData.longitude),
        danger_level: parseInt(formData.danger_level),
        tags
      })

      push(`/buildings/${data.id}`)
    } catch (e) {
      error = e.detail || '提交失败，请重试'
    } finally {
      submitting = false
    }
  }
</script>

<div class="upload-page container">
  <div class="page-header">
    <h1 class="page-title">📝 记录废墟</h1>
    <p class="page-subtitle">分享你发现的废弃建筑，丰富废墟档案</p>
  </div>

  <div class="form-container">
    <div class="form-card card">
      {#if error}
        <div class="error-message">
          <span class="error-icon">⚠️</span>
          {error}
        </div>
      {/if}

      <div class="form-section">
        <h3 class="section-title">基本信息</h3>
        
        <div class="form-group">
          <label class="form-label">建筑名称 *</label>
          <input
            type="text"
            bind:value={formData.title}
            placeholder="例如：红星纺织厂"
          />
        </div>

        <div class="form-row">
          <div class="form-group">
            <label class="form-label">建筑类型</label>
            <select bind:value={formData.building_type}>
              {#each buildingTypes as type}
                <option value={type}>{type}</option>
              {/each}
            </select>
          </div>

          <div class="form-group">
            <label class="form-label">危险等级</label>
            <select bind:value={formData.danger_level}>
              <option value={1}>1级 - 安全</option>
              <option value={2}>2级 - 注意</option>
              <option value={3}>3级 - 危险</option>
              <option value={4}>4级 - 高危</option>
              <option value={5}>5级 - 极危</option>
            </select>
          </div>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label class="form-label">建设年代</label>
            <input
              type="number"
              bind:value={formData.construction_year}
              placeholder="例如：1958"
            />
          </div>

          <div class="form-group">
            <label class="form-label">废弃时间</label>
            <input
              type="number"
              bind:value={formData.abandonment_year}
              placeholder="例如：2005"
            />
          </div>
        </div>

        <div class="form-group">
          <label class="form-label">详细地址</label>
          <input
            type="text"
            bind:value={formData.address}
            placeholder="请输入详细地址"
          />
        </div>
      </div>

      <div class="divider"></div>

      <div class="form-section">
        <h3 class="section-title">位置坐标</h3>
        <p class="section-desc">填写经纬度坐标，方便其他探索者在地图上找到这里</p>

        <div class="form-row">
          <div class="form-group">
            <label class="form-label">纬度</label>
            <input
              type="number"
              step="0.000001"
              bind:value={formData.latitude}
              placeholder="例如：31.230416"
            />
          </div>

          <div class="form-group">
            <label class="form-label">经度</label>
            <input
              type="number"
              step="0.000001"
              bind:value={formData.longitude}
              placeholder="例如：121.473701"
            />
          </div>
        </div>

        <button type="button" class="btn btn-secondary locate-btn" on:click={handleLocate}>
          📍 使用当前位置
        </button>
      </div>

      <div class="divider"></div>

      <div class="form-section">
        <h3 class="section-title">详细介绍</h3>
        
        <div class="form-group">
          <label class="form-label">简介</label>
          <textarea
            bind:value={formData.description}
            placeholder="简要描述这座建筑的现状、特点..."
            rows="4"
          ></textarea>
        </div>

        <div class="form-group">
          <label class="form-label">历史背景</label>
          <textarea
            bind:value={formData.history}
            placeholder="介绍这座建筑的历史故事、背景..."
            rows="5"
          ></textarea>
        </div>

        <div class="form-group">
          <label class="form-label">标签</label>
          <input
            type="text"
            bind:value={formData.tags}
            placeholder="多个标签用逗号分隔，例如：工厂, 工业遗产, 苏式建筑"
          />
        </div>
      </div>

      <div class="divider"></div>

      <div class="form-actions">
        <button 
          type="button" 
          class="btn btn-secondary"
          on:click={() => history.back()}
          disabled={submitting}
        >
          取消
        </button>
        <button 
          type="button" 
          class="btn btn-primary"
          on:click={handleSubmit}
          disabled={submitting}
        >
          {submitting ? '提交中...' : '提交档案'}
        </button>
      </div>
    </div>

    <div class="tips-card card">
      <h3 class="tips-title">📋 提交须知</h3>
      <ul class="tips-list">
        <li><strong>真实准确：</strong>请确保提交的信息真实可靠</li>
        <li><strong>安全第一：</strong>不要冒险进入危险建筑获取信息</li>
        <li><strong>尊重隐私：</strong>避免泄露个人隐私信息</li>
        <li><strong>合法合规：</strong>请勿非法闯入私人领地</li>
        <li><strong>保护遗迹：</strong>只带走照片，只留下脚印</li>
      </ul>

      <div class="divider"></div>

      <h4 class="tips-subtitle">💡 小贴士</h4>
      <p class="tips-text">
        上传后可以继续补充照片、视频和安全隐患标注，
        完善的档案能帮助更多探索者。
      </p>
    </div>
  </div>
</div>

<style>
  .upload-page {
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

  .form-container {
    display: grid;
    grid-template-columns: 1fr 300px;
    gap: 24px;
    align-items: start;
  }

  .form-card {
    padding: 30px;
  }

  .error-message {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 12px 16px;
    background: rgba(139, 37, 0, 0.2);
    border: 1px solid var(--rust-dark);
    border-radius: 6px;
    color: var(--rust-light);
    font-size: 13px;
    margin-bottom: 24px;
  }

  .error-icon {
    font-size: 18px;
  }

  .form-section {
    margin-bottom: 10px;
  }

  .section-title {
    font-size: 18px;
    margin-bottom: 16px;
    color: var(--text-bright);
  }

  .section-desc {
    font-size: 13px;
    color: var(--text-muted);
    margin-bottom: 16px;
    margin-top: -8px;
  }

  .form-group {
    display: flex;
    flex-direction: column;
    gap: 8px;
    margin-bottom: 16px;
  }

  .form-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
  }

  .form-label {
    font-size: 13px;
    color: var(--text-muted);
    letter-spacing: 1px;
  }

  .form-group input,
  .form-group textarea,
  .form-group select {
    padding: 10px 14px;
    font-size: 14px;
    width: 100%;
  }

  .form-group textarea {
    resize: vertical;
    min-height: 100px;
  }

  .locate-btn {
    font-size: 13px;
    padding: 8px 16px;
  }

  .divider {
    height: 1px;
    background: var(--border-color);
    margin: 24px 0;
  }

  .form-actions {
    display: flex;
    justify-content: flex-end;
    gap: 12px;
    margin-top: 10px;
  }

  .btn {
    padding: 10px 24px;
    font-size: 14px;
  }

  .tips-card {
    padding: 24px;
    position: sticky;
    top: 90px;
  }

  .tips-title {
    font-size: 16px;
    margin-bottom: 16px;
    color: var(--rust-light);
  }

  .tips-list {
    list-style: none;
    padding: 0;
    margin: 0;
  }

  .tips-list li {
    padding: 10px 0;
    font-size: 13px;
    color: var(--text-main);
    line-height: 1.6;
    border-bottom: 1px dashed var(--border-color);
  }

  .tips-list li:last-child {
    border-bottom: none;
  }

  .tips-list strong {
    color: var(--moss-pale);
  }

  .tips-subtitle {
    font-size: 14px;
    color: var(--text-bright);
    margin-bottom: 10px;
  }

  .tips-text {
    font-size: 13px;
    color: var(--text-muted);
    line-height: 1.7;
  }

  @media (max-width: 900px) {
    .form-container {
      grid-template-columns: 1fr;
    }

    .tips-card {
      position: static;
      order: -1;
    }
  }

  @media (max-width: 480px) {
    .form-row {
      grid-template-columns: 1fr;
    }

    .form-card {
      padding: 20px;
    }
  }
</style>
