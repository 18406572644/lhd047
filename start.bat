@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ========================================
echo   城市废墟探索系统 - Docker 一键启动
echo ========================================
echo.
echo [端口映射]
echo   - 前端: 2047
echo   - 后端: 6047
echo.
echo [镜像源] 华为云 SWR (国内高速)
echo.

echo [1/4] 清理旧容器和构建缓存...
docker-compose down 2>nul
docker image prune -f 2>nul
docker builder prune -af 2>nul

echo.
echo [2/4] 预拉取基础镜像（华为云镜像源）...
set MIRROR=swr.cn-north-4.myhuaweicloud.com/ddn-k8s/docker.io
set IMAGES=python:3.9-slim node:18-alpine nginx:alpine
set MAX_RETRY=3

for %%img in (%IMAGES%) do (
    set SRC=%MIRROR%/%%img
    set /a retry=0
    :pull_loop_%%img
    set /a retry+=1
    echo   正在拉取 %%img [尝试 !retry!/%MAX_RETRY%]...
    docker pull !SRC!
    if !errorlevel! neq 0 (
        if !retry! lss %MAX_RETRY% (
            echo     失败，3秒后重试...
            timeout /t 3 /nobreak >nul
            goto pull_loop_%%img
        ) else (
            echo.
            echo [错误] 拉取 %%img 失败！请检查网络连接。
            echo.
            pause
            exit /b 1
        )
    )
    echo   [OK] %%img 拉取成功
)

echo.
echo [3/4] 构建并启动容器...
docker-compose up -d --build

if %errorlevel% neq 0 (
    echo.
    echo [错误] 构建失败！请检查上面的错误信息。
    echo.
    pause
    exit /b 1
)

echo.
echo [4/4] 等待服务启动...
timeout /t 15 /nobreak >nul

echo.
echo ========================================
echo   启动完成！
echo ========================================
echo.
echo 前端访问: http://localhost:2047
echo 后端API : http://localhost:6047/api/health
echo.
echo 常用命令:
echo   查看日志: docker-compose logs -f
echo   停止服务: docker-compose down
echo   重启服务: docker-compose restart
echo.
pause
