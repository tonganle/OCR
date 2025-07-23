import sys
import subprocess
import os
import time
import requests
import cv2
import base64
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QFileDialog, QTableWidget, QTableWidgetItem, QHeaderView
)
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt

def cv2_to_base64(image):
    data = cv2.imencode('.jpg', image)[1]
    return base64.b64encode(data.tobytes()).decode('utf8')

def is_server_running():
    try:
        # 改为请求根路径，只要不是 404 就认为服务已启动
        r = requests.get("http://127.0.0.1:8866/", timeout=2)
        return r.status_code != 404
    except Exception:
        return False

def start_paddlehub_serving():
    if is_server_running():
        return
    # Windows 下隐藏黑框
    creationflags = 0
    if sys.platform == "win32":
        creationflags = subprocess.CREATE_NO_WINDOW
    subprocess.Popen(
        [r"D:/anacond/envs/paddle/Scripts/hub.exe", "serving", "start", "-m", "chinese_ocr_db_crnn_server"],
        shell=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        creationflags=creationflags
    )
    for _ in range(20):
        if is_server_running():
            return
        time.sleep(1)
    raise RuntimeError("PaddleHub Serving 启动失败，请检查环境！")

class OCRClient(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PaddleHub OCR Windows客户端")
        self.resize(900, 600)
        self.image_path = None

        # 左侧：图片预览
        self.img_label = QLabel("请上传图片")
        self.img_label.setAlignment(Qt.AlignCenter)
        self.img_label.setFixedSize(350, 400)

        # 右侧：识别结果表格
        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(['文本', '置信度', '坐标'])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # 按钮
        self.btn_upload = QPushButton("选择图片")
        self.btn_upload.clicked.connect(self.choose_images)
        self.btn_ocr = QPushButton("识别")
        self.btn_ocr.clicked.connect(self.do_ocr)
        self.btn_ocr.setEnabled(False)

        # 布局
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.img_label)
        left_layout.addWidget(self.btn_upload)
        left_layout.addWidget(self.btn_ocr)

        right_layout = QVBoxLayout()
        right_layout.addWidget(QLabel("识别结果："))
        right_layout.addWidget(self.table)

        main_layout = QHBoxLayout()
        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)
        self.setLayout(main_layout)

    def choose_images(self):
        files, _ = QFileDialog.getOpenFileNames(self, "选择图片", "", "Images (*.png *.jpg *.jpeg *.bmp)")
        if files:
            self.image_paths = files
            # 显示第一张预览
            pixmap = QPixmap(files[0]).scaled(350, 400, Qt.KeepAspectRatio)
            self.img_label.setPixmap(pixmap)
            self.btn_ocr.setEnabled(True)
            self.table.setRowCount(0)

    def do_ocr(self):
        if not hasattr(self, 'image_paths') or not self.image_paths:
            return
        self.table.setRowCount(0)
        for img_path in self.image_paths:
            img = cv2.imread(img_path)
            data = {'images': [cv2_to_base64(img)]}
            headers = {"Content-type": "application/json"}
            url = "http://127.0.0.1:8866/predict/chinese_ocr_db_crnn_server"
            try:
                r = requests.post(url=url, headers=headers, json=data, timeout=30)
                r.raise_for_status()
                results = r.json().get("results", [])
                self.show_result(results, img_path)
            except Exception as e:
                row = self.table.rowCount()
                self.table.insertRow(row)
                self.table.setItem(row, 0, QTableWidgetItem(f"{os.path.basename(img_path)} 请求失败"))
                self.table.setItem(row, 1, QTableWidgetItem(str(e)))
                self.table.setItem(row, 2, QTableWidgetItem(""))

    def show_result(self, results, img_path):
        for block in results:
            for item in block.get('data', []):
                row = self.table.rowCount()
                self.table.insertRow(row)
                self.table.setItem(row, 0, QTableWidgetItem(f"{os.path.basename(img_path)} : {item['text']}"))
                self.table.setItem(row, 1, QTableWidgetItem(f"{item['confidence']:.3f}"))
                coord = str(item['text_box_position'])
                self.table.setItem(row, 2, QTableWidgetItem(coord))

if __name__ == '__main__':
    start_paddlehub_serving()
    app = QApplication(sys.argv)
    win = OCRClient()
    win.show()
    sys.exit(app.exec_()) 