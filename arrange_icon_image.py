import cv2
import os

# 画像を読み込んで、指定したサイズになるように縦横にパディングを追加する関数
# 画像が透過情報を持っている場合、RGBA形式で読み込み、透過下地を追加する
# 画像がRGB形式の場合は、白色のパディングを追加する
def add_padding_to_image(image_path, target_size=(800,600)):
    # 画像を読み込む
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

    # 画像のサイズを取得
    height, width = image.shape[:2]

    # 縦横の比率を計算
    aspect_ratio = width / height

    # ターゲットサイズに合わせてパディングを追加するための新しいサイズを計算
    if aspect_ratio > 1:  # 横長の場合
        new_width = target_size[0]
        new_height = int(target_size[0] / aspect_ratio)
    else:  # 縦長または正方形の場合
        new_width = int(target_size[1] * aspect_ratio)
        new_height = target_size[1]

    # リサイズされた画像を作成
    resized_image = cv2.resize(image, (new_width, new_height))

    # 新しい画像のサイズを取得
    new_height, new_width = resized_image.shape[:2]

    # パディングのサイズを計算
    top_padding = max(0, (target_size[1] - new_height) // 2)
    bottom_padding = max(0, target_size[1] - new_height - top_padding)
    left_padding = max(0, (target_size[0] - new_width) // 2)
    right_padding = max(0, target_size[0] - new_width - left_padding)

    # パディングを追加するための新しい画像を作成
    if len(resized_image.shape) == 3 and resized_image.shape[2] == 4:  # RGBA形式の場合
        padded_image = cv2.copyMakeBorder(resized_image, top_padding, bottom_padding, left_padding, right_padding,
                                           cv2.BORDER_CONSTANT, value=(255, 255, 255, 0))  # 白色の透過下地
    else:  # RGB形式の場合
        padded_image = cv2.copyMakeBorder(resized_image, top_padding, bottom_padding, left_padding, right_padding,
                                           cv2.BORDER_CONSTANT, value=(255, 255, 255))  # 白色のパディング

    return padded_image

if __name__ == "__main__":
    # 画像ディレクトリのパスを指定
    icon_dir = './temp'
    output_dir = './static/anpan'
    all_images = [f for f in os.listdir(icon_dir) if f.endswith(('.png', '.jpg', '.jpeg', '.gif'))]

    # 画像をパディングして保存
    for image_path in all_images:
        image_full_path = os.path.join(icon_dir, image_path)
        padded_image = add_padding_to_image(image_full_path)

        # 保存先のパスを指定
        save_path = os.path.join(output_dir, image_path)
        cv2.imwrite(save_path, padded_image)