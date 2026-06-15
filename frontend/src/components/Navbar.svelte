<script>
  import { link } from 'svelte-spa-router'
  import { auth } from '../stores/auth'
  import { onMount } from 'svelte'

  let mobileMenuOpen = false

  function toggleMobileMenu() {
    mobileMenuOpen = !mobileMenuOpen
  }

  function handleLogout() {
    auth.logout()
    window.location.hash = '#/'
  }

  $: isLoggedIn = $auth.isAuthenticated
  $: user = $auth.user
</script>

<nav class="navbar">
  <div class="nav-container">
    <a href="#/" use:link class="logo">
      <span class="logo-icon">🏚️</span>
      <span class="logo-text">废墟档案</span>
      <span class="logo-sub">RUINS ARCHIVE</span>
    </a>

    <div class="nav-links">
      <a href="#/" use:link class="nav-link">首页</a>
      <a href="#/buildings" use:link class="nav-link">建筑档案</a>
      <a href="#/map" use:link class="nav-link">探索地图</a>
      <a href="#/routes" use:link class="nav-link">探索路线</a>
      <a href="#/rankings" use:link class="nav-link">热门排行</a>
    </div>

    <div class="nav-actions">
      {#if isLoggedIn}
        <a href="#/upload" use:link class="btn btn-primary upload-btn">
          <span>+ 记录废墟</span>
        </a>
        <div class="user-menu">
          <span class="username">{user?.username || '用户'}</span>
          <button on:click={handleLogout} class="logout-btn">退出</button>
        </div>
      {:else}
        <a href="#/login" use:link class="nav-link">登录</a>
        <a href="#/register" use:link class="btn btn-primary">注册</a>
      {/if}
    </div>

    <button class="mobile-menu-btn" on:click={toggleMobileMenu}>
      <span class="hamburger"></span>
    </button>
  </div>

  {#if mobileMenuOpen}
    <div class="mobile-menu">
      <a href="#/" use:link class="mobile-link" on:click={toggleMobileMenu}>首页</a>
      <a href="#/buildings" use:link class="mobile-link" on:click={toggleMobileMenu}>建筑档案</a>
      <a href="#/map" use:link class="mobile-link" on:click={toggleMobileMenu}>探索地图</a>
      <a href="#/routes" use:link class="mobile-link" on:click={toggleMobileMenu}>探索路线</a>
      <a href="#/rankings" use:link class="mobile-link" on:click={toggleMobileMenu}>热门排行</a>
      <div class="mobile-divider"></div>
      {#if isLoggedIn}
        <a href="#/upload" use:link class="mobile-link" on:click={toggleMobileMenu}>记录废墟</a>
        <span class="mobile-link" on:click={handleLogout}>退出登录</span>
      {:else}
        <a href="#/login" use:link class="mobile-link" on:click={toggleMobileMenu}>登录</a>
        <a href="#/register" use:link class="mobile-link" on:click={toggleMobileMenu}>注册</a>
      {/if}
    </div>
  {/if}
</nav>

<style>
  .navbar {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 1000;
    background: linear-gradient(180deg, rgba(28, 28, 26, 0.98) 0%, rgba(28, 28, 26, 0.95) 100%);
    backdrop-filter: blur(10px);
    border-bottom: 1px solid var(--border-color);
    box-shadow: 0 2px 20px rgba(0, 0, 0, 0.3);
  }

  .nav-container {
    max-width: 1280px;
    margin: 0 auto;
    padding: 0 20px;
    height: 70px;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  .logo {
    display: flex;
    align-items: center;
    gap: 10px;
    text-decoration: none;
  }

  .logo-icon {
    font-size: 28px;
    filter: grayscale(30%);
  }

  .logo-text {
    font-family: 'ZCOOL KuaiLe', cursive;
    font-size: 22px;
    color: var(--text-bright);
    letter-spacing: 3px;
  }

  .logo-sub {
    font-size: 10px;
    color: var(--rust-light);
    letter-spacing: 2px;
    margin-top: 2px;
    display: none;
  }

  .nav-links {
    display: flex;
    gap: 8px;
  }

  .nav-link {
    color: var(--text-main);
    text-decoration: none;
    padding: 8px 16px;
    border-radius: 4px;
    font-size: 14px;
    letter-spacing: 1px;
    transition: all 0.3s ease;
    position: relative;
  }

  .nav-link:hover {
    color: var(--rust-light);
    background-color: rgba(183, 65, 14, 0.1);
  }

  .nav-actions {
    display: flex;
    align-items: center;
    gap: 16px;
  }

  .upload-btn {
    font-size: 13px;
    padding: 8px 18px;
  }

  .user-menu {
    display: flex;
    align-items: center;
    gap: 12px;
  }

  .username {
    color: var(--text-bright);
    font-size: 14px;
  }

  .logout-btn {
    background: none;
    border: 1px solid var(--border-color);
    color: var(--text-muted);
    padding: 6px 14px;
    border-radius: 4px;
    font-size: 12px;
    cursor: pointer;
    transition: all 0.3s ease;
  }

  .logout-btn:hover {
    border-color: var(--rust-dark);
    color: var(--rust-light);
  }

  .mobile-menu-btn {
    display: none;
    background: none;
    border: none;
    cursor: pointer;
    padding: 8px;
  }

  .hamburger {
    display: block;
    width: 22px;
    height: 2px;
    background-color: var(--text-main);
    position: relative;
  }

  .hamburger::before,
  .hamburger::after {
    content: '';
    position: absolute;
    left: 0;
    width: 22px;
    height: 2px;
    background-color: var(--text-main);
  }

  .hamburger::before {
    top: -7px;
  }

  .hamburger::after {
    top: 7px;
  }

  .mobile-menu {
    display: none;
    background-color: var(--bg-mid);
    border-top: 1px solid var(--border-color);
    padding: 16px;
  }

  .mobile-link {
    display: block;
    padding: 12px 16px;
    color: var(--text-main);
    text-decoration: none;
    border-radius: 4px;
    transition: background-color 0.2s;
  }

  .mobile-link:hover {
    background-color: var(--bg-hover);
    color: var(--rust-light);
  }

  .mobile-divider {
    height: 1px;
    background-color: var(--border-color);
    margin: 8px 0;
  }

  @media (max-width: 900px) {
    .nav-links {
      display: none;
    }

    .nav-actions {
      display: none;
    }

    .mobile-menu-btn {
      display: block;
    }

    .mobile-menu {
      display: block;
    }
  }
</style>
