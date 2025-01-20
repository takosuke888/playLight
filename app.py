from flask import Flask, render_template, request
import random
import os
import switchbot_led_test

app = Flask(__name__)

# アイコン画像のディレクトリを指定
ICON_DIRS = ["static/pokemon", "static/icons"]

color_dict = {
    "blue.png": "0:0:255",
    "green.png": "0:255:0",
    "lightblue.png": "0:255:255",
    "orange.png": "255:50:0",
    "red.png": "255:0:0",
    "yellow.png": "255:255:0",

    "ashimari.png": "0:0:255",
    "hogeta.png": "255:0:0",
    "pikachu.png": "255:255:0",
    "sarunori.png": "50:200:10"
}

swithLED = switchbot_led_test.SwitchBotAPI()

@app.route('/')
def index():

    icon_dir = ICON_DIRS[random.randint(0,1)]

    # 画像ディレクトリからファイル名を取得
    all_images = [f for f in os.listdir(icon_dir) if f.endswith(('.png', '.jpg', '.jpeg', '.gif'))]
    
    # ランダムに4つの画像を選択
    selected_images = random.sample(all_images, 4)
    selected_images = [icon_dir.split('/')[-1] + '/' + name for name in selected_images]
    
    # 中心画像
    center_image = "light.jpg"

    # APIヘッダーの初期化
    swithLED.header = swithLED.create_header()

    return render_template('index.html', center_image=center_image, images=selected_images)

@app.route('/light_control', methods=['POST'])
def change_light_color():
    # クリックされた画像名を取得
    image_path = request.json.get('image_path')  # POSTのJSONデータから取得
    image_name = image_path.split('/')[-1]


    print(f"Clicked image: {image_name}")  # ターミナルにログ出力

    if image_name == 'light.jpg':
        swithLED.turn_on(swithLED.bulb_device_id)
        swithLED.set_cct(swithLED.bulb_device_id, 5200)
        return '', 204
    else:

        # デバイスIDが見つからない場合の処理
        if not swithLED.bulb_device_id:
            print("Device not found.")
            return "Device not found", 404
        
        if image_name in color_dict:
            color = color_dict[image_name]
        else:
            return "Color not found", 404

        response = swithLED.set_color(swithLED.bulb_device_id, color)

        return '', 204  # レスポンスボディなし、ステータスコード204で終了

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)