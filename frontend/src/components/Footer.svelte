<script>
  const currentYear = new Date().getFullYear()
</script>

<footer class="footer">
  <div class="footer-container">
    <div class="footer-content">
      <div class="footer-section">
        <h3 class="footer-title">🏚️ 废墟档案</h3>
        <p class="footer-desc">
          记录被遗忘的城市角落，探索时间留下的痕迹。
          每一座废弃建筑都有它的故事。
        </p>
      </div>

      <div class="footer-section">
        <h4 class="footer-heading">快速链接</h4>
        <ul class="footer-links">
          <li><a href="#/">首页</a></li>
          <li><a href="#/buildings">建筑档案</a></li>
          <li><a href="#/map">探索地图</a></li>
          <li><a href="#/rankings">热门排行</a></li>
        </ul>
      </div>

      <div class="footer-section">
        <h4 class="footer-heading">探索者须知</h4>
        <ul class="footer-links">
          <li>注意人身安全</li>
          <li>遵守法律法规</li>
          <li>保护历史遗迹</li>
          <li>尊重私人领地</li>
        </ul>
      </div>

      <div class="footer-section">
        <h4 class="footer-heading">联系我们</h4>
        <p class="footer-text">
          有新的废墟发现？<br>
          欢迎分享给我们！
        </p>
        <div class="footer-tagline">
          在废墟中寻找诗意
        </div>
      </div>
    </div>

    <div class="footer-bottom">
      <p class="copyright">
        © {currentYear} 废墟档案 RUINS ARCHIVE | 城市废墟探索记录平台
      </p>
      <div class="footer-decor"></div>
    </div>
  </div>
</footer>

<style>
  .footer {
    background: linear-gradient(180deg, var(--bg-mid) 0%, var(--bg-dark) 100%);
    border-top: 2px solid var(--border-rust);
    margin-top: 60px;
    position: relative;
  }

  .footer::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 1px;
    background: linear-gradient(90deg, 
      transparent, 
      var(--rust-mid), 
      var(--moss-mid), 
      var(--rust-mid), 
      transparent
    );
  }

  .footer-container {
    max-width: 1280px;
    margin: 0 auto;
    padding: 50px 20px 20px;
  }

  .footer-content {
    display: grid;
    grid-template-columns: 2fr 1fr 1fr 1.5fr;
    gap: 40px;
    margin-bottom: 40px;
  }

  .footer-title {
    font-family: 'ZCOOL KuaiLe', cursive;
    font-size: 24px;
    color: var(--text-bright);
    margin-bottom: 16px;
    letter-spacing: 2px;
  }

  .footer-desc {
    color: var(--text-muted);
    font-size: 14px;
    line-height: 1.8;
  }

  .footer-heading {
    color: var(--rust-light);
    font-size: 14px;
    margin-bottom: 16px;
    letter-spacing: 2px;
  }

  .footer-links {
    list-style: none;
    padding: 0;
  }

  .footer-links li {
    margin-bottom: 10px;
  }

  .footer-links a {
    color: var(--text-muted);
    text-decoration: none;
    font-size: 13px;
    transition: color 0.3s ease;
  }

  .footer-links a:hover {
    color: var(--rust-light);
  }

  .footer-text {
    color: var(--text-muted);
    font-size: 13px;
    line-height: 1.8;
    margin-bottom: 16px;
  }

  .footer-tagline {
    font-family: 'ZCOOL KuaiLe', cursive;
    color: var(--moss-pale);
    font-size: 14px;
    letter-spacing: 2px;
    padding: 8px 0;
    border-top: 1px dashed var(--border-color);
  }

  .footer-bottom {
    border-top: 1px solid var(--border-color);
    padding-top: 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .copyright {
    color: var(--text-muted);
    font-size: 12px;
  }

  .footer-decor {
    width: 100px;
    height: 20px;
    background-image: 
      radial-gradient(circle, var(--rust-dark) 2px, transparent 2px);
    background-size: 10px 10px;
    opacity: 0.3;
  }

  @media (max-width: 768px) {
    .footer-content {
      grid-template-columns: 1fr 1fr;
      gap: 30px;
    }
  }

  @media (max-width: 480px) {
    .footer-content {
      grid-template-columns: 1fr;
    }
  }
</style>
