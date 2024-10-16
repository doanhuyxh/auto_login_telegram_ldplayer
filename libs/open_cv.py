import cv2
import numpy as np
from matplotlib import pyplot as plt

def find_template_in_image(template_image_path,large_image_path, debug=False):
    large_image = cv2.imread(large_image_path, cv2.IMREAD_COLOR)
    template = cv2.imread(template_image_path, cv2.IMREAD_COLOR)
    large_image_gray = cv2.cvtColor(large_image, cv2.COLOR_BGR2GRAY)
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    w, h = template_gray.shape[::-1]  
    res = cv2.matchTemplate(large_image_gray, template_gray, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where(res >= threshold)    
    
    for pt in zip(*loc[::-1]):
        center_x = int(pt[0] + w // 2)
        center_y = int(pt[1] + h // 2)
        if debug:
            cv2.rectangle(large_image, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 2)
            plt.imshow(cv2.cvtColor(large_image, cv2.COLOR_BGR2RGB))
            plt.title('Detected Template')
            plt.show()
        return (center_x, center_y)
    
    return None
