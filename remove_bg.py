import os
from rembg import remove
from PIL import Image

REMBG = 0
COLOR_PICK = 1
METHOD = REMBG

def remve_background(input_path, output_path):

    # 画像を開く
    with open(input_path, "rb") as file:
        input_image = file.read()
    
    # 背景削除処理
    output_image = remove(input_image)

    # 出力画像を保存
    output_image_path = os.path.join(output_folder, os.path.splitext(filename)[0] + ".png")
    with open(output_image_path, "wb") as file:
        file.write(output_image)

# 色を指定して透過させる
def color_pick(input_path, output_path, color=(255, 255, 255)):

    # 画像を開く
    with Image.open(input_path) as img:
        # 色を指定して透過処理
        img = img.convert("RGBA")
        datas = img.getdata()

        new_data = []
        for item in datas:
            if item[0] == color[0] and item[1] == color[1] and item[2] == color[2]:
                new_data.append((255, 255, 255, 0))  # 指定色を透過
            else:
                new_data.append(item)

        img.putdata(new_data)
        img.save(output_path, format='PNG')

# 入力フォルダと出力フォルダを設定
input_folder = "temp"  # 画像が保存されているフォルダのパス
output_folder = "./"  # 出力画像を保存するフォルダのパス

# 出力フォルダが存在しない場合は作成
os.makedirs(output_folder, exist_ok=True)

# フォルダ内のすべての画像ファイルを処理
for filename in os.listdir(input_folder):
    input_path = os.path.join(input_folder, filename)

    # ファイルが画像か確認
    if not filename.lower().endswith((".jpg", ".jpeg", ".png")):
        print(f"スキップ: {filename}（画像ファイルではありません）")
        continue

    try:

        if METHOD == REMBG:
            # Rembgを使用して背景を削除
            remve_background(input_path, os.path.join(output_folder, filename))

        elif METHOD == COLOR_PICK:
            color_pick(input_path, os.path.join(output_folder, filename), color=(255, 255, 255))

    except Exception as e:
        print(f"エラー: {filename} - {e}")
