import cv2
import numpy as np

def spot_hot_cold(img_python):
    img= cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

    Tmin_val, Tmax_val, Tmin_loc, Tmax_loc= cv2.minMaxLoc(img)

    # Encircling the  spots
    img_color= cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    cv2.circle(img_color, Tmin_loc, 4, (255, 0, 0), 3)
    cv2.circle(img_color, Tmax_loc, 4, (0, 0, 255), 3)

    # Save the result
    op_img_path= 'op_img.jpg'
    cv2.imwrite(op_img_path, img_color)

    return Tmin_loc, Tmax_loc, op_img_path

Tmin_loc, Tmax_loc, op_img_path= spot_hot_cold(r"C:\Users\sushant.gupta\Desktop\Sushant Gupta\Practice Images\FLIR1429test")
print(f'Coldest Spot: {Tmin_loc}, Hottest Spot: {Tmax_loc}')