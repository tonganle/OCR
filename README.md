# PaddleHub OCR Flask Demo

本项目实现了基于 PaddleHub Serving 的中文OCR识别Web应用，支持图片上传、预览和识别结果展示。

---

## 目录结构

```
├── app.py                # Flask后端主程序
├── templates/
│   └── index.html        # 前端页面模板
├── uploads/              # 上传图片存放目录（自动生成）
└── README.md             # 使用说明
```

---

## 1. 环境依赖

建议使用 Python 3.7+，推荐使用虚拟环境。

```bash
pip install flask requests opencv-python paddlehub
```

> **注意：**
> - 若本地未安装 PaddlePaddle，请根据[官方文档](https://www.paddlepaddle.org.cn/install/quick)安装对应版本。
> - 若需使用GPU推理，需安装GPU版本的 PaddlePaddle，并设置 CUDA_VISIBLE_DEVICES 环境变量。

---

## 2. 启动 PaddleHub Serving 服务

首先下载并启动 OCR 服务：

```bash
hub install chinese_ocr_db_crnn_server
hub serving start -m chinese_ocr_db_crnn_server
```

- 默认服务端口为 8866。
- 若需使用GPU：
  ```bash
  set CUDA_VISIBLE_DEVICES=0  # Windows
  export CUDA_VISIBLE_DEVICES=0  # Linux/Mac
  hub serving start -m chinese_ocr_db_crnn_server
  ```

---

## 3. 启动 Flask Web 服务

确保 `uploads` 文件夹有写入权限（首次运行会自动创建）。

```bash
python app.py
```

- 默认访问地址：http://127.0.0.1:5000/

---

## 4. 使用说明

1. 打开浏览器访问 [http://127.0.0.1:5000/](http://127.0.0.1:5000/)
2. 点击“选择文件”上传图片，点击“上传并识别”
3. 左侧显示图片预览，右侧显示识别结果（文本、置信度、坐标）

---

## 5. 常见问题

- **图片预览不显示？**
  - 检查 `uploads` 目录是否存在且有写入权限。
  - 确认 Flask 路由 `/uploads/<filename>` 是否正常。
  - 避免上传中文或特殊字符命名的图片。

- **识别结果乱码或不显示？**
  - 前端已做表格展示，若仍乱码请检查 PaddleHub 服务端返回内容。

- **PaddleHub Serving 无法访问？**
  - 检查 8866 端口是否被占用。
  - 检查服务是否已启动，或尝试重启。

- **依赖安装失败？**
  - 建议使用国内镜像源或科学上网。

---

## 6. 参考链接
- [PaddleHub官方文档](https://www.paddlepaddle.org.cn/hublist)
- [PaddleOCR项目主页](https://github.com/PaddlePaddle/PaddleOCR)

---

如有其它问题或定制需求，请联系开发者。 

## 使用 PyInstaller 打包为 exe

你可以使用 PyInstaller 将 ocr_client.py 打包为 Windows 下的可执行文件（exe）。

### 打包命令

在已激活 paddle 环境的命令行中执行：

```
pyinstaller --noconsole --onefile --add-binary "D:/anacond/envs/paddle/Scripts/hub.exe;." ocr_client.py
```

- `--noconsole`：打包为无控制台窗口的 GUI 程序。
- `--onefile`：打包为单一 exe 文件。
- `--add-binary "D:/anacond/envs/paddle/Scripts/hub.exe;."`：将 hub.exe 一起打包到 exe 同目录。

### 注意事项

1. 需提前安装好 PyInstaller：
   ```
   pip install pyinstaller
   ```
2. 打包时请确保 hub.exe 路径与你本机实际路径一致。
3. 打包完成后，exe 文件在 `dist/ocr_client.exe`。
4. 目标电脑需有完整的 Python 环境和 paddlehub 相关依赖，否则 exe 可能无法独立运行。
5. 若需彻底免安装运行，建议使用 conda-pack 打包整个环境，详见本文件相关说明。 