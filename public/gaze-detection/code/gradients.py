import cv2, numpy as np

from time import time

__winname = "Eye Centre (gradients)"
__debug_imgs = {}

__inv_intensity_weight_divisor = 100
__fast_width = 25.0

# Algorithm from "ACCURATE EYE CENTRE LOCALISATION BY MEANS OF GRADIENTS - Fabian Timm and Erhardt Barth"
# Based on C++ code from https://github.com/trishume/eyeLike

def test_possible_centers_formula(grad_x0, grad_y0, darkness_weight, grad_x_val, grad_y_val, indicies_grid, shape):
    
    dx = np.ones(shape) * grad_x0 - indicies_grid[1]
    dy = np.ones(shape) * grad_y0 - indicies_grid[0]
    magnitudes = cv2.magnitude(dx + 0.0001, dy)          # 0.0001 is a hack to offset against division by 0
    dx = dx / magnitudes
    dy = dy / magnitudes
    
    diffs = (dx * grad_x_val + dy * grad_y_val) * darkness_weight
    diffs[diffs < 0] = 0   
    
    return diffs


def get_center_map(eye_img_grey):
    
    grad_x_img = cv2.Sobel(eye_img_grey, ddepth=cv2.CV_32F, dx=1, dy=0, ksize=5)
    grad_y_img = cv2.Sobel(eye_img_grey, ddepth=cv2.CV_32F, dx=0, dy=1, ksize=5)
    
    magnitudes = np.sqrt(grad_x_img ** 2 + grad_y_img ** 2).astype(int)
    
    mag_thresh = int(np.std(magnitudes) / 2 + np.mean(magnitudes))
    
    grad_x_img = np.divide(grad_x_img, magnitudes + 1)
    grad_y_img = np.divide(grad_y_img, magnitudes + 1)
    
    grad_x_img[magnitudes < mag_thresh] = 0
    grad_y_img[magnitudes < mag_thresh] = 0   
    
    # inverted image for weighting
    eye_img_inv = 255 - eye_img_grey
    darkness_weights = eye_img_inv / __inv_intensity_weight_divisor
    
    accumulator = np.zeros(eye_img_grey.shape[:2], dtype=np.float32)
    indicies_grid = np.indices(accumulator.shape[:2])
    indicies_shape = indicies_grid.shape[1:3]
    
    for y in range(eye_img_grey.shape[0]):
        for x in range (eye_img_grey.shape[1]):
            if grad_x_img[y][x] == 0 and grad_y_img[y][x] == 0: continue
            accumulator += test_possible_centers_formula(x, y,
                                                         darkness_weights[y][x],
                                                         grad_x_img[y][x], grad_y_img[y][x],
                                                         indicies_grid, indicies_shape)
    
    num_gradients = eye_img_grey.shape[0] * eye_img_grey.shape[1]
    return accumulator / num_gradients


def find_pupil(eye_img_bgr, debug_index=False):
    
    """ Estimates the centre of the pupil using image gradients
    """

    eye_img_r = cv2.split(eye_img_bgr)[2]   # Extract red channel only
    
    # Scale to small image for faster computation
    scale = __fast_width / eye_img_bgr.shape[0]
    small_size = (int((__fast_width / eye_img_bgr.shape[0]) * eye_img_bgr.shape[1]), int(__fast_width))
    eye_img_small = cv2.resize(eye_img_r, small_size)
    
    center_map = get_center_map(eye_img_small)
    
    max_val_index = np.argmax(center_map)
    pupil_y0, pupil_x0 = max_val_index // center_map.shape[1], max_val_index % center_map.shape[1]
    
    # Scale back to original coordinates
    pupil_y0, pupil_x0 = int((pupil_y0 + 0.5) / scale), int((pupil_x0 + 0.5) / scale)
            
    return pupil_x0, pupil_y0