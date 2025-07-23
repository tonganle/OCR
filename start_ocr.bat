@echo off
REM 激活conda paddle环境
call conda activate paddle
REM 启动PaddleHub Serving服务（新窗口，防止阻塞）
start cmd /k "hub serving start -m chinese_ocr_db_crnn_server"
REM 等待服务启动
ping 127.0.0.1 -n 6 >nul
REM 启动OCR客户端
python ocr_client.py 