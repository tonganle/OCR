from flask import Flask, render_template, request, url_for, send_from_directory, Response, session, redirect
import os
import requests
import json
import cv2
import base64
import time
import random
import re
from openpyxl import Workbook
from io import BytesIO
from urllib.parse import quote

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
app.secret_key = 'your_secret_key'

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

def extract_info(texts):
    info = {
        '单号': '',
        '寄件人': '',
        '寄件人电话': '',
        '寄件人地址': '',
        '收件人': '',
        '收件人电话': '',
        '收件人地址': ''
    }
    all_text = '\n'.join(texts)
    # 单号
    m = re.search(r'([1-9]\d{9,})', all_text)
    if m:
        info['单号'] = m.group(1)
    phone_pattern = r'(1[3-9]\d{1}\*{2,4}\d{3,4}|1[3-9]\d{9})'
    # 收件人（找第一个出现的“收”或“收件人”或手机号前的中文名）
    for i, t in enumerate(texts):
        # 收件人姓名+电话
        m = re.match(r'([\u4e00-\u9fa5]{2,})[\s:：]*' + phone_pattern, t)
        if m and not info['收件人']:
            info['收件人'] = m.group(1)
            info['收件人电话'] = m.group(2)
            # 地址在后面一两行
            for j in range(i+1, min(i+3, len(texts))):
                if len(texts[j]) > 6:
                    info['收件人地址'] += texts[j]
        # 寄件人姓名+电话
        if not info['寄件人']:
            m2 = re.match(r'([\u4e00-\u9fa5]{2,})[\s:：]*' + phone_pattern, t)
            if m2 and info['收件人'] and m2.group(1) != info['收件人']:
                info['寄件人'] = m2.group(1)
                info['寄件人电话'] = m2.group(2)
                # 地址在后面一两行
                for j in range(i+1, min(i+3, len(texts))):
                    if len(texts[j]) > 6:
                        info['寄件人地址'] += texts[j]
    # 地址补全（如果没找到）
    if not info['收件人地址']:
        for i, t in enumerate(texts):
            if '收' == t.strip() or '收件人' in t:
                # 地址在后面
                for j in range(i+1, min(i+4, len(texts))):
                    if len(texts[j]) > 6:
                        info['收件人地址'] += texts[j]
    return info

@app.route('/', methods=['GET', 'POST'])
def index():
    results = []
    img_urls = []
    if request.method == 'POST':
        files = request.files.getlist('file')
        for file in files:
            ext = os.path.splitext(file.filename)[1]
            new_filename = time.strftime('%Y%m%d%H%M%S') + '_' + str(random.randint(1000,9999)) + ext
            img_path = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
            file.save(img_path)
            img_url = url_for('uploaded_file', filename=new_filename)
            img_urls.append(img_url)
            result = ocr_by_serving(img_path)
            texts = []
            for block in result:
                for item in block.get('data', []):
                    texts.append(item['text'])
            print(f"图片 {file.filename} 识别原始文本：\n" + '\n'.join(texts))
            info = extract_info(texts)
            info['图片名'] = file.filename
            results.append({'img_url': img_url, 'info': info, 'filename': file.filename})
        # 保存到 session 以便导出
        session['export_data'] = [r['info'] for r in results]
    return render_template('index.html', results=results, img_urls=img_urls)

@app.route('/export')
def export():
    export_data = session.get('export_data', [])
    if not export_data:
        return redirect(url_for('index'))
    wb = Workbook()
    ws = wb.active
    ws.title = "快递信息"
    # 表头
    ws.append(['单号', '寄件人', '寄件人电话', '寄件人地址', '收件人', '收件人电话', '收件人地址'])
    for info in export_data:
        ws.append([
            info.get('单号', ''),
            info.get('寄件人', ''),
            info.get('寄件人电话', ''),
            info.get('寄件人地址', ''),
            info.get('收件人', ''),
            info.get('收件人电话', ''),
            info.get('收件人地址', '')
        ])
    output = BytesIO()
    wb.save(output)
    output.seek(0)
    filename = "快递信息导出.xlsx"
    return Response(
        output.getvalue(),
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={
            'Content-Disposition': f"attachment; filename*=UTF-8''{quote(filename)}"
        }
    )

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True) 