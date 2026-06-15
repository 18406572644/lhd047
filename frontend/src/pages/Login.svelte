<script>
  import { link, push } from 'svelte-spa-router'
  import { auth } from '../stores/auth'
  import { authAPI } from '../api/modules'

  let formData = {
    username: '',
    password: ''
  }
  let loading = false
  let error = ''

  async function handleLogin() {
    if (!formData.username || !formData.password) {
      error = '请填写用户名和密码'
      return
    }

    loading = true
    error = ''

    try {
      const data = await authAPI.login(formData)
      const userData = await authAPI.getMe()
      auth.login(data.access_token, userData)
      push('/')
    } catch (e) {
      error = e.detail || '登录失败，请检查用户名和密码'
    } finally {
      loading = false
    }
  }

  function handleKeydown(e) {
    if (e.key === 'Enter') {
      handleLogin()
    }
  }
</script>

<div class="auth-page">
  <div class="auth-container">
    <div class="auth-card card">
      <div class="auth-header">
        <div class="auth-icon">🔐</div>
        <h1 class="auth-title">探索者登录</h1>
        <p class="auth-subtitle">进入废墟世界的通行证</p>
      </div>

      {#if error}
        <div class="error-message">
          <span class="error-icon">⚠️</span>
          {error}
        </div>
      {/if}

      <form class="auth-form" on:submit|preventDefault={handleLogin}>
        <div class="form-group">
          <label class="form-label">用户名</label>
          <input
            type="text"
            bind:value={formData.username}
            placeholder="请输入用户名"
            on:keydown={handleKeydown}
            autocomplete="username"
          />
        </div>

        <div class="form-group">
          <label class="form-label">密码</label>
          <input
            type="password"
            bind:value={formData.password}
            placeholder="请输入密码"
            on:keydown={handleKeydown}
            autocomplete="current-password"
          />
        </div>

        <button 
          type="submit" 
          class="btn btn-primary w-full"
          disabled={loading}
        >
          {loading ? '登录中...' : '登 录'}
        </button>
      </form>

      <div class="auth-divider">
        <span>还没有账号？</span>
      </div>

      <a href="#/register" use:link class="btn btn-secondary w-full">
        立即注册
      </a>

      <div class="demo-info">
        <p class="demo-title">🎮 演示账号</p>
        <p class="demo-account">用户名: 废墟猎人 / 密码: 123456</p>
      </div>
    </div>

    <div class="auth-decoration">
      <div class="deco-text">废墟档案</div>
      <div class="deco-sub">RUINS ARCHIVE</div>
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
      radial-gradient(circle at 20% 30%, rgba(139, 37, 0, 0.1) 0%, transparent 40%),
      radial-gradient(circle at 80% 70%, rgba(45, 90, 61, 0.1) 0%, transparent 40%);
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
    margin-bottom: 32px;
  }

  .auth-icon {
    font-size: 48px;
    margin-bottom: 16px;
  }

  .auth-title {
    font-size: 28px;
    margin-bottom: 8px;
  }

  .auth-subtitle {
    color: var(--text-muted);
    font-size: 14px;
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
    gap: 18px;
  }

  .form-group {
    display: flex;
    flex-direction: column;
    gap: 8px;
  }

  .form-label {
    font-size: 13px;
    color: var(--text-muted);
    letter-spacing: 1px;
  }

  .form-group input {
    padding: 12px 16px;
    font-size: 15px;
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
    margin: 24px 0 16px;
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
    font-size: 13px;
    padding: 0 12px;
    background: var(--bg-card);
  }

  .demo-info {
    margin-top: 24px;
    padding: 16px;
    background: var(--bg-mid);
    border-radius: 6px;
    text-align: center;
  }

  .demo-title {
    font-size: 13px;
    color: var(--moss-pale);
    margin-bottom: 6px;
  }

  .demo-account {
    font-size: 12px;
    color: var(--text-muted);
    font-family: monospace;
  }

  .auth-decoration {
    text-align: center;
  }

  .deco-text {
    font-family: 'ZCOOL KuaiLe', cursive;
    font-size: 72px;
    color: var(--text-bright);
    letter-spacing: 12px;
    line-height: 1.2;
    opacity: 0.9;
    text-shadow: 0 4px 30px rgba(0, 0, 0, 0.5);
  }

  .deco-sub {
    font-size: 20px;
    color: var(--rust-light);
    letter-spacing: 8px;
    margin-top: 12px;
    opacity: 0.8;
  }

  @media (max-width: 768px) {
    .auth-container {
      grid-template-columns: 1fr;
      gap: 30px;
    }

    .auth-decoration {
      display: none;
    }

    .auth-card {
      padding: 30px 24px;
    }
  }
</style>
