from flask import Flask, render_template, request
import random
import os
import switchbot_led_test
import cv2
from sklearn.cluster import KMeans
import time

import logging

# ロガーの設定
logging.basicConfig(filename='event_log.log', level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

# werkzeugのロガーのレベルを変更
logging.getLogger('werkzeug').setLevel(logging.ERROR)

# アイコン画像のディレクトリを指定
ICON_DIRS = ["static/pokemon", "static/icons", "static/anpan"]

color_dict = {
    "blue.png": "0:0:255",
    "green.png": "0:255:0",
    "lightblue.png": "0:200:255",
    "orange.png": "255:50:0",
    "red.png": "255:0:0",
    "yellow.png": "255:200:0",
    "peach.png": "255:0:150",
    "nasu.png": "200:0:255",

    "ashimari.png": "0:0:255",
    "hogeta.png": "255:0:0",
    "pikachu.png": "255:200:0",
    "sarunori.png": "50:200:10",
    "meripu.png": "255:100:50",
    "evee.png": "255:50:0",

    "anpan.png": "255:0:0",
    "baikin.png": "200:0:255",
    "cheeze.png": "255:50:0",
    "dokin.png": "255:50:0",
    "kare.png": "255:50:50",
    "kokin.png": "10:10:255",
    "meron.png": "255:200:0",
    "shoku.png": "255:255:255"
}

swithLED = switchbot_led_test.SwitchBotAPI()

# 画像から主要な色を抽出
def extract_dominant_colors(image_path, n_colors=1):
    # 画像を読み込む
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # RGBに変換

    # 画像をリサイズ（処理を高速化するため）
    reshaped_image = image.reshape((-1, 3))  # 1次元化

    # K-meansクラスタリングで主要な色を抽出
    kmeans = KMeans(n_clusters=n_colors, random_state=42)
    kmeans.fit(reshaped_image)
    dominant_colors = kmeans.cluster_centers_.astype(int)  # クラスタ中心が主要な色

    return dominant_colors #RGB

# SwitchBotAPIの形式に合わせたカラーコード辞書を設定
def add_color_dict(image_path):

    main_color = extract_dominant_colors(image_path, 3)

    # SwitchBotAPIの形式に合わせたカラーコード
    color_string = str(main_color[0][0]) + ':' + str(main_color[0][1]) + ':' + str(main_color[0][2])

    color_dict[os.path.basename(image_path)] = color_string

@app.route('/')
def index():

    icon_dir = ICON_DIRS[random.randint(0,len(ICON_DIRS)-1)]

    # 画像ディレクトリからファイル名を取得
    all_images = [f for f in os.listdir(icon_dir) if f.endswith(('.png', '.jpg', '.jpeg', '.gif'))]
    
    # ランダムに4つの画像を選択
    selected_images = random.sample(all_images, 4)
    selected_images_paths = [icon_dir.split('/')[-1] + '/' + name for name in selected_images]
    
    # Color Dict を生成
    #for image in selected_images:
    #    add_color_dict(os.path.join(icon_dir, image))

    # 中心画像
    center_image = "light.jpg"

    # 前回のヘッダー作成から2分経過している場合、ヘッダーを再作成
    if (time.time() - swithLED.header_created_at) > 180:
        swithLED.header = swithLED.create_header()
        swithLED.header_created_at = time.time()
        logger.info(f"Event: create_header, Header: {swithLED.header}")
    else:
        print("Header is still valid.")

    return render_template('index.html', center_image=center_image, images=selected_images_paths)

@app.route('/light_control', methods=['POST'])
def change_light_color():

    # クリックされた画像名を取得
    image_path = request.json.get('image_path')  # POSTのJSONデータから取得
    image_name = image_path.split('/')[-1]

    if image_name == 'light.jpg':
        #swithLED.turn_on(swithLED.bulb_device_id)
        swithLED.toggle(swithLED.bulb_device_id)
        time.sleep(3)
        logger.info(f"Event: turn_on, DeviceID: {swithLED.bulb_device_id}")
        return '', 204
    else:

        # デバイスIDが見つからない場合の処理
        if not swithLED.bulb_device_id:
            return "Device not found", 404
        
        if image_name in color_dict:
            color = color_dict[image_name]
        else:
            return "Color not found", 404

        response = swithLED.set_color(swithLED.bulb_device_id, color)
        time.sleep(3)
        logger.info(f"Event: set_color, DeviceID: {swithLED.bulb_device_id}, 色: {color}")

        return '', 204  # レスポンスボディなし、ステータスコード204で終了

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)