import cv2
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import os

def extract_dominant_colors(image_path, n_colors=1):
    # 画像を読み込む
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # OpenCVはBGR形式なのでRGBに変換

    # 画像をリサイズ（処理を高速化するため）
    resized_image = cv2.resize(image, (100, 100))
    reshaped_image = resized_image.reshape((-1, 3))  # 1次元化

    # K-meansクラスタリングで主要な色を抽出
    kmeans = KMeans(n_clusters=n_colors, random_state=42)
    kmeans.fit(reshaped_image)
    dominant_colors = kmeans.cluster_centers_.astype(int)  # クラスタ中心が主要な色

    return dominant_colors

def plot_colors(colors):
    # 色をプロット
    bar = np.zeros((50, 300, 3), dtype="uint8")
    start_x = 0

    for color in colors:
        end_x = start_x + 300 // len(colors)
        bar[:, start_x:end_x] = color
        start_x = end_x

    plt.figure(figsize=(8, 2))
    plt.axis("off")
    plt.imshow(bar)
    plt.show()

icon_dir = './static/pokemon'
all_images = [f for f in os.listdir(icon_dir) if f.endswith(('.png', '.jpg', '.jpeg', '.gif'))]

for image_path in all_images:

    # 画像パスを指定
    print(image_path)
    #image_path = "sample.jpg"  # ここに画像ファイルのパスを指定
    n_colors = 2  # 抽出する色の数

    # 主要な色を抽出して表示
    dominant_colors = extract_dominant_colors(os.path.join(icon_dir,image_path), n_colors)
    print("主要な色 (RGB):", dominant_colors)
    plot_colors(dominant_colors)