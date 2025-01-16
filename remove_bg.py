import os
from rembg import remove
from PIL import Image

# 画像を透過する

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
        # 画像を開く
        with open(input_path, "rb") as file:
            input_image = file.read()
        
        # 背景削除処理
        output_image = remove(input_image)

        # 出力画像を保存
        output_image_path = os.path.join(output_folder, os.path.splitext(filename)[0] + ".png")
        with open(output_image_path, "wb") as file:
            file.write(output_image)

        print(f"保存完了: {output_image_path}")
    except Exception as e:
        print(f"エラー: {filename} - {e}")
