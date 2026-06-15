<script>
  import { link, push } from 'svelte-spa-router'
  import { auth } from '../stores/auth'
  import { authAPI } from '../api/modules'

  let formData = {
    username: '',
    email: '',
    password: '',
    confirmPassword: ''
  }
  let loading = false
  let error = ''

  async function handleRegister() {
    error = ''

    if (!formData.username || formData.username.length < 3) {
      error = '用户名至少3个字符'
      return
    }
    if (!formData.email) {
      error = '请输入邮箱'
      return
    }
    if (!formData.password || formData.password.length < 6) {
      error = '密码至少6个字符'
      return
    }
    if (formData.password !== formData.confirmPassword) {
      error = '两次输入的密码不一致'
      return
    }

    loading = true

    try {
      const data = await authAPI.register({
        username: formData.username,
        email: formData.email,
        password: formData.password
      })
      const userData = await authAPI.getMe()
      auth.login(data.access_token, userData)
      push('/')
    } catch (e) {
      error = e.detail || '注册失败，请重试'
    } finally {
      loading = false
    }
  }
</script>

<div class="auth-page">
  <div class="auth-container">
    <div class="auth-decoration">
      <div class="deco-text">加入探索</div>
      <div class="deco-sub">JOIN THE ADVENTURE</div>
      <p class="deco-desc">
        记录你发现的每一处废墟，<br>
        分享城市被遗忘的故事。
      </p>
    </div>

    <div class="auth-card card">
      <div class="auth-header">
        <div class="auth-icon">📝</div>
        <h1 class="auth-title">探索者注册</h1>
        <p class="auth-subtitle">开启你的废墟探索之旅</p>
      </div>

      {#if error}
        <div class="error-message">
          <span class="error-icon">⚠️</span>
          {error}
        </div>
      {/if}

      <form class="auth-form" on:submit|preventDefault={handleRegister}>
        <div class="form-group">
          <label class="form-label">用户名</label>
          <input
            type="text"
            bind:value={formData.username}
            placeholder="请输入用户名（至少3个字符）"
          />
        </div>

        <div class="form-group">
          <label class="form-label">邮箱</label>
          <input
            type="email"
            bind:value={formData.email}
            placeholder="请输入邮箱地址"
          />
        </div>

        <div class="form-group">
          <label class="form-label">密码</label>
          <input
            type="password"
            bind:value={formData.password}
            placeholder="请输入密码（至少6位）"
          />
        </div>

        <div class="form-group">
          <label class="form-label">确认密码</label>
          <input
            type="password"
            bind:value={formData.confirmPassword}
            placeholder="请再次输入密码"
          />
        </div>

        <button 
          type="submit" 
          class="btn btn-primary w-full"
          disabled={loading}
        >
          {loading ? '注册中...' : '注 册'}
        </button>
      </form>

      <div class="auth-divider">
        <span>已有账号？</span>
      </div>

      <a href="#/login" use:link class="btn btn-secondary w-full">
        去登录
      </a>

      <p class="agreement-text">
        注册即表示你同意我们的探索守则，
        请文明探险，注意安全。
      </p>
    </div>
  </div>
</div>

<style>
  .auth-page {
    min-height: calc(100vh - 70px);
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 40px 20px;
    position: relative;
    overflow: hidden;
  }

  .auth-page::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: 
      radial-gradient(circle at 80% 30%, rgba(45, 90, 61, 0.1) 0%, transparent 40%),
      radial-gradient(circle at 20% 70%, rgba(139, 37, 0, 0.1) 0%, transparent 40%);
  }

  .auth-container {
    position: relative;
    z-index: 1;
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 60px;
    max-width: 900px;
    width: 100%;
    align-items: center;
  }

  .auth-card {
    padding: 40px;
    backdrop-filter: blur(10px);
  }

  .auth-header {
    text-align: center;
    margin-bottom: 28px;
  }

  .auth-icon {
    font-size: 48px;
    margin-bottom: 12px;
  }

  .auth-title {
    font-size: 26px;
    margin-bottom: 6px;
  }

  .auth-subtitle {
    color: var(--text-muted);
    font-size: 13px;
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
    margin-bottom: 20px;
  }

  .error-icon {
    font-size: 18px;
  }

  .auth-form {
    display: flex;
    flex-direction: column;
    gap: 14px;
  }

  .form-group {
    display: flex;
    flex-direction: column;
    gap: 6px;
  }

  .form-label {
    font-size: 12px;
    color: var(--text-muted);
    letter-spacing: 1px;
  }

  .form-group input {
    padding: 10px 14px;
    font-size: 14px;
  }

  .w-full {
    width: 100%;
  }

  .btn {
    padding: 12px 24px;
    font-size: 15px;
    letter-spacing: 2px;
  }

  .auth-divider {
    text-align: center;
    margin: 20px 0 14px;
    position: relative;
  }

  .auth-divider::before,
  .auth-divider::after {
    content: '';
    position: absolute;
    top: 50%;
    width: 30%;
    height: 1px;
    background: var(--border-color);
  }

  .auth-divider::before {
    left: 0;
  }

  .auth-divider::after {
    right: 0;
  }

  .auth-divider span {
    color: var(--text-muted);
    font-size: 12px;
    padding: 0 12px;
    background: var(--bg-card);
  }

  .agreement-text {
    margin-top: 20px;
    text-align: center;
    font-size: 11px;
    color: var(--text-muted);
    line-height: 1.6;
  }

  .auth-decoration {
    text-align: center;
  }

  .deco-text {
    font-family: 'ZCOOL KuaiLe', cursive;
    font-size: 56px;
    color: var(--text-bright);
    letter-spacing: 10px;
    line-height: 1.2;
    margin-bottom: 8px;
    text-shadow: 0 4px 30px rgba(0, 0, 0, 0.5);
  }

  .deco-sub {
    font-size: 16px;
    color: var(--moss-pale);
    letter-spacing: 6px;
    margin-bottom: 24px;
    opacity: 0.8;
  }

  .deco-desc {
    font-size: 15px;
    color: var(--text-muted);
    line-height: 1.8;
  }

  @media (max-width: 768px) {
    .auth-container {
      grid-template-columns: 1fr;
      gap: 0;
    }

    .auth-decoration {
      display: none;
    }

    .auth-card {
      padding: 30px 24px;
    }
  }
</style>
