import datetime
import numpy as np
import cv2

# -------------------------------------------------------------------
# Parameters
# -------------------------------------------------------------------

CONF_THRESHOLD = 0.5
NMS_THRESHOLD = 0.4
IMG_WIDTH = 416
IMG_HEIGHT = 416

# Default colors
COLOR_BLUE = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_RED = (0, 0, 255)
COLOR_WHITE = (255, 255, 255)
COLOR_YELLOW = (0, 255, 255)

SCALE_THRESHOLDS = {
    "area": [0.35, 0.26, 0.18, 0.1, 0.050, 0.035, 0.02, 0.009, 0.067, 0.0035, 0.001],
    "height": [0.5, 0.35, 0.24, 0.15, 0.075, 0.05, 0.035, 0.014, 0.08, 0.06, 0.02],
    "width": [0.5, 0.35, 0.24, 0.15, 0.075, 0.05, 0.035, 0.014, 0.08, 0.06, 0.02]}
TEXT_PLAN = {0: "Extreme close up", 1: "Extreme<->big",
             2: "Big close up", 3: "Close up", 4: "Medium close up", 5: "Close up<->medium",
             6: "Medium shot", 7: "Medium long shot", 8: "Medium<->long",
             9: "Long shot", 10: "Very long shot"}
PLAN_NAMES = ["Extreme close up", "Extreme<->big",
              "Big close up", "Close up", "Medium close up", "Close up<->medium",
              "Medium shot", "Medium long shot", "Medium<->long",
              "Long shot", "Very long shot"]


def find_crucial_box(boxes_coordinates, method='area'):
    max_param = float('-inf')
    crucial_box_index = 0
    if len(boxes_coordinates) == 0:  # если было обнаружено лишь одно лицо
        return 0

    for box_num, coordinates in enumerate(boxes_coordinates):
        top, left, bottom, right = coordinates
        width = abs(left - right)
        height = abs(top - bottom)

        if method == "area":
            area = height * width
            if area > max_param:
                max_param = area
                crucial_box_index = box_num

        if method == "height":
            if height > max_param:
                max_param = height
                crucial_box_index = box_num

        if method == "width":
            if width > max_param:
                max_param = width
                crucial_box_index = box_num

    return crucial_box_index


def get_thresholds(method="area"):
    if method in ["area", "height", "width"]:
        return SCALE_THRESHOLDS[method]
    else:
        return -1


def detect_plan_scale(
        box,
        frame_height,
        frame_width,
        method="area"):
    top, left, bottom, right = box
    width = abs(left - right)
    height = abs(top - bottom)

    if method == "area":
        frame_area = frame_height * frame_width
        box_area = height * width
        ratio = box_area / frame_area

    elif method == "height":
        ratio = width / frame_width

    elif method == "width":
        ratio = height / frame_height

    else:
        print(" ~ ~ Wrong method ~ ~ ")
        return -1

    return ratio


def decide_plan(ratio, method="area"):
    ths = SCALE_THRESHOLDS
    txt = TEXT_PLAN
    ind, _ = find_nearest(ratio, ths[method])
    if ind in [1, 5, 8]:
        clr = (15, 255, 255)
    elif ind in [0, 2, 3, 4, 6, 7, 9, 10]:
        clr = (15, 255, 15)
    else:
        clr = (255, 255, 255)
    return txt[ind], clr


def find_nearest(value, array):
    array = np.array(array)
    idx = (np.abs(array - value)).argmin()
    return idx, np.abs(array[idx] - value)

# def decide_temp_plan(ratio, method="area"):
#     ths = SCALE_THRESHOLDS[method]
#     idx, dif = find_nearest(ratio, ths)
#     if 0.0007 <= dif < 0.001:
#         temp_text = "Near perfect" + " "
#         color = (5, 145, 5)
#     elif 0.001 <= dif:
#         temp_text = "Not perfect" + " "
#         color = (15, 15, 235)
#     else:
#         temp_text = "Perfect" + " "
#         color = (15, 245, 15)
#
#     return temp_text, color
#
#
# def suggest_scale(ratio, box, frame_height, frame_width, method="area"):
#     ths_for_method = SCALE_THRESHOLDS[method]
#     plan_names = PLAN_NAMES
#     ratios_arr = []
#
#     top, left, bottom, right = box
#     width = abs(left - right)
#     height = abs(top - bottom)
#
#     for name, ths in zip(plan_names, ths_for_method):
#         if method == "area":
#             # perfect_ratio = height * width / (ths * frame_height * frame_width)
#             perfect = ths * frame_height * frame_width
#             ours = height * width
#             ratios_arr.append(round(perfect / ours, 2))
#         elif method == "width":
#             perfect_ratio = width / (ths * frame_width)
#             ratios_arr.append(round(ratio / perfect_ratio, 2))
#         elif method == "height":
#             perfect_ratio = height / (ths * frame_height)
#             ratios_arr.append(round(ratio / perfect_ratio, 2))
#         else:
#             return -1
#     idx1, min1, idx2, min2 = find_two_nearest(ratio, ratios_arr)
#     text1 = plan_names[idx1]
#     text2 = plan_names[idx2]
#     return text1, round(min1, 3), text2, round(min2, 3)
#
#
# def find_two_nearest(value, array):
#     array = np.array(array)
#     dif_array = (np.abs(array - value))
#     idx1 = dif_array.argmin()
#     min1 = dif_array[idx1]
#     min2 = 100
#     idx2 = 0
#     for i in range(len(dif_array)):
#         if dif_array[i] != min1 and dif_array[i] < min2:
#             min2 = dif_array[i]
#             idx2 = i
#     return idx1, array[idx1], idx2, array[idx2]
