import cv2
import numpy as np
import os

def create_labeled_image(filename, label, color):
    img = np.zeros((480, 640, 3), dtype=np.uint8)
    img[:] = (255, 255, 255)
    # 画一个代表病害的区域
    cv2.circle(img, (320, 240), 100, color, -1)
    # 添加文字
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img, f"Simulated {label}", (50, 400), font, 1, (0, 0, 0), 2)
    
    output_path = os.path.join('data/raw', filename)
    cv2.imwrite(output_path, img)
    print(f"Generated {output_path}")

if __name__ == "__main__":
    os.makedirs('data/raw', exist_ok=True)
    # 模拟三种常见病虫害，文件名触发 visual_module/inference.py 的逻辑
    samples = [
        ("strawberry_powdery_mildew.jpg", "Powdery Mildew", (200, 200, 200)), # 白色粉末状
        ("blueberry_aphid.jpg", "Aphid Infestation", (50, 150, 50)),         # 绿色蚜虫
        ("raspberry_gray_mold.jpg", "Gray Mold", (100, 100, 100))            # 灰色霉层
    ]
    for f, l, c in samples:
        create_labeled_image(f, l, c)
