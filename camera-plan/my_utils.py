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

SCALE_THRESHOLDS = {"area": [0.2, 0.08, 0.04], "height": [0.48, 0.32, 0.16], "width": [0.44, 0.32, 0.2]}
TEXT_PLAN = {0: "Large plan", 1: "Medium plan", 2: "Little plan"}
PLAN_NAMES = ["large", "medium", "little"]


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

    return txt[ind]


def find_nearest(value, array):
    array = np.array(array)
    idx = (np.abs(array - value)).argmin()
    return idx, np.abs(array[idx] - value)


def suggest_scale(ratio, box, frame_height, frame_width, method="area"):
    ths_for_method = SCALE_THRESHOLDS[method]
    plan_names = PLAN_NAMES
    suggestions = []

    top, left, bottom, right = box
    width = abs(left - right)
    height = abs(top - bottom)

    for name, ths in zip(plan_names, ths_for_method):
        if method == "area":
            # perfect_ratio = height * width / (ths * frame_height * frame_width)
            perfect = ths * frame_height * frame_width
            ours = height * width
            suggestions.append(f"Change for perfect {name} for {round(perfect / ours, 3)} times")
        elif method == "width":
            perfect_ratio = width / (ths * frame_width)
            suggestions.append(f"Change for perfect {name} for {round(ratio / perfect_ratio, 3)} times")
        elif method == "height":
            perfect_ratio = height / (ths * frame_height)
            suggestions.append(f"Change for perfect {name} for {round(ratio / perfect_ratio, 3)} times")
        else:
            return ["ERROR"]
    return suggestions
