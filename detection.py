import cv2
import numpy

def create_mask_by_range(hsvFrame, color_range):
    """
    Gets a color range and returns a OpenCV mask.
    """
    color_lower = numpy.array(color_range[0], numpy.uint8)
    color_upper = numpy.array(color_range[1], numpy.uint8)
    return cv2.inRange(hsvFrame, color_lower, color_upper)

def detect_objects_by_color_range(frame, color_range_list, minimum_area = 500, draw_contour = True, color = (255, 0, 0)):
    """
    Detects the biggest object of each color range and draws its contour on the frame.
    """
    # Converts the frame in BGR to HSV (hue-saturation-value).
    hsvFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    object_detector = lambda color_range: get_object_bbox(hsvFrame, color_range)
    detected_objects = []

    # Looks for the objects getting their bbox (x1, y1, x2, y2, area) and drawing their contour.
    for object_bbox in map(object_detector, color_range_list):
        if len(object_bbox) == 5 and object_bbox[-1] >= minimum_area:
            if draw_contour: cv2.rectangle(frame, object_bbox[0 : 2], object_bbox[2 : 4], color, 2)
            detected_objects.append(object_bbox)
    return detected_objects

def find_biggest_contour(mask):
    """
    Finds contours on the mask and returns the biggest contour found.
    """
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return sorted(contours, key = cv2.contourArea)[-1] if len(contours) != 0 else None

def get_contour_bbox(contour):
    """
    Returns (x1, y1, x2, y2, area) of the contour.
    """
    x, y, width, height = cv2.boundingRect(contour)
    return (x, y, x + width, y + height, cv2.contourArea(contour))

def get_object_bbox(hsvFrame, color_range):
    """
    Finds the biggest object on the frame by a color range and returns its bbox.
    """
    color_mask = create_mask_by_range(hsvFrame, color_range)

    # Morphological Transformation...
    kernel = numpy.ones((5, 5), numpy.uint8)
    color_mask = cv2.dilate(color_mask, kernel)

    # Finds the object contour and returns its bbox.
    object_contour = find_biggest_contour(color_mask)
    return list() if object_contour is None else get_contour_bbox(object_contour)
