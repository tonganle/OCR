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

## 环境要求

本项目需在 **Python 3.8** 环境下运行，建议使用 Anaconda/Miniconda 创建对应版本环境。

## 依赖安装

本项目所有依赖已列在 requirements.txt 文件中。你可以用如下命令一键安装：

```bash
pip install -r requirements.txt
```

如需使用 GPU 版本的 paddlepaddle，请参考 https://www.paddlepaddle.org.cn/install/quick 