from flask import Flask, render_template, request, url_for, send_from_directory
import os
import requests
import json
import cv2
import base64
import time
import random

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def cv2_to_base64(image):
    data = cv2.imencode('.jpg', image)[1]
    return base64.b64encode(data.tobytes()).decode('utf8')

def ocr_by_serving(img_path):
    img = cv2.imread(img_path)
    data = {'images': [cv2_to_base64(img)]}
    headers = {"Content-type": "application/json"}
    url = "http://127.0.0.1:8866/predict/chinese_ocr_db_crnn_server"
    r = requests.post(url=url, headers=headers, data=json.dumps(data))
    if r.status_code == 200:
        return r.json().get("results", [])
    else:
        return [{"error": "服务请求失败"}]

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    img_url = None
    if request.method == 'POST':
        file = request.files['file']
        if file:
            # 自动重命名，避免中文和重名
            ext = os.path.splitext(file.filename)[1]
            new_filename = time.strftime('%Y%m%d%H%M%S') + '_' + str(random.randint(1000,9999)) + ext
            img_path = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
            file.save(img_path)
            img_url = url_for('uploaded_file', filename=new_filename)
            result = ocr_by_serving(img_path)
    return render_template('index.html', result=result, img_url=img_url)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True) 