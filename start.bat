@echo off
echo ========================================
echo 海外工程项目招投标资料管理库 - 启动脚本
echo ========================================
echo.

echo [1/2] 启动后端服务 (端口5000)...
cd backend
start "Flask Server" cmd /k python app.py
echo.

echo [2/2] 启动前端服务 (端口3000)...
cd ..\frontend
start "Vue Dev Server" cmd /k npm run dev
echo.

echo ========================================
echo 启动完成！
echo 后端地址: http://localhost:5000
echo 前端地址: http://localhost:3000
echo ========================================
pause
