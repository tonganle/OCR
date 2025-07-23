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

本项目需在 **Python 3.8** 环境下运行，建议使用 Anaconda/Miniconda 创建对应版本环境。请参考
      零基础windows安装
      第1步：安装Anaconda
      说明：使用paddlepaddle需要先安装python环境，这里我们选择python集成环境Anaconda工具包
      Anaconda是1个常用的python包管理程序
      安装完Anaconda后，可以安装python环境，以及numpy等所需的工具包环境。
      Anaconda下载：
      地址：https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/?C=M&O=D
      大部分win10电脑均为64位操作系统，选择x86_64版本；若电脑为32位操作系统，则选择x86.exe
      anaconda download
      下载完成后，双击安装程序进入图形界面
      默认安装位置为C盘，建议将安装位置更改到D盘：
      install config
      勾选conda加入环境变量，忽略警告：
      add conda to path
      第2步：打开终端并创建conda环境
      打开Anaconda Prompt终端

      左下角Windows Start Menu -> Anaconda3 -> Anaconda Prompt启动控制台
      anaconda download
      创建新的conda环境

      # 在命令行输入以下命令，创建名为paddle_env的环境
      # 此处为加速下载，使用清华源
      conda create --name paddle_env python=3.8 --channel https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/  # 这是一行命令
      该命令会创建1个名为paddle_env、python版本为3.8的可执行环境，根据网络状态，需要花费一段时间

      之后命令行中会输出提示信息，输入y并回车继续安装

      conda create
      激活刚创建的conda环境，在命令行中输入以下命令：

      # 激活paddle_env环境
      conda activate paddle_env
      # 查看当前python的位置
      where python
      create environment
      以上anaconda环境和python环境安装完毕

      第3步：安装程序运行所需库
      使用pip命令在刚激活的环境中安装paddle，

      # 在命令行中输入以下命令
      # 确认当前所用的pip是否是paddle_env环境下的pip
      where pip
      # 默认安装CPU版本，安装paddle时建议使用百度源
      pip install paddlepaddle -i https://mirror.baidu.com/pypi/simple
      若需要安装GPU版本，则请打开paddle官网选择适合的版本

      paddle官网：https://www.paddlepaddle.org.cn/
      由于安装GPU版本需要先配置好CUDA和cudnn，建议有一定基础后再安装GPU版本
      安装完paddle后，继续在paddle_env环境中安装paddlehub：

      # 在命令行中输入以下命令
      pip install paddlehub -i https://mirror.baidu.com/pypi/simple
      paddlehub的介绍文档：https://github.com/PaddlePaddle/PaddleHub/blob/release/v2.1/README_ch.md
      
      #启动PaddleHub Serving
      hub serving start -m chinese_ocr_db_crnn_server

## 依赖安装

本项目所有依赖已列在 requirements.txt 文件中。你可以用如下命令一键安装：

```bash
pip install -r requirements.txt
```

如需使用 GPU 版本的 paddlepaddle，请参考 https://www.paddlepaddle.org.cn/install/quick 

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