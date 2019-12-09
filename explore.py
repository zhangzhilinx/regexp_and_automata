import io

import cv2
import numpy as np
from graphviz import Source
from matplotlib import pyplot as plt

if __name__ == '__main__':
    with open('./var/main_min_dfa.dot', 'r', encoding='utf-8') as f:
        s = Source(f.read())
    png_buf = s.pipe('png')
    png_mem_file = io.BytesIO(png_buf)
    png_np = np.frombuffer(png_buf, dtype=np.uint8)
    img = cv2.imdecode(png_np, flags=1)
    plt.imshow(img)
    plt.show()
