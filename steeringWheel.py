from PIL import Image
import cv2, math, numpy

__all__ = ("SteeringWheel",)

class SteeringWheel(object):

    def __init__(self, filename, radius, maximum_angle = 180):
        self.__image = Image.open(filename).resize((radius * 2, radius * 2))
        self.__maximum_angle = abs(maximum_angle)
        self.__angle = 0

    def __convert_image(self, image):
        # Makes a mask of where the transparent bits are.
        transparent_mask = image[:,:,3] == 0

        # Replaces areas of transparency with white.
        image[transparent_mask] = [255, 255, 255, 255]

        # Removes alpha channel.
        return cv2.cvtColor(image, cv2.COLOR_RGBA2BGR)

    def get_angle(self):
        return self.__angle

    def get_image(self):
        # Rotates the PIL image and converts it to an OpenCV image.
        rotated_image = self.__image.rotate(self.__angle)
        return self.__convert_image(numpy.array(rotated_image))

    def get_percent(self):
        return 100 / self.__maximum_angle * self.__angle

    def set_angle(self, angle):
        # Checks whether the angle is equal or lower than the limit.
        if abs(angle) > self.__maximum_angle:
            self.__angle = self.__maximum_angle * (-1 if angle < 0 else 1)
        else: self.__angle = angle

    def set_angle_by_ends(self, left_position, right_position):
        """
        Sets the steering wheel angle (-180 -> 180 degrees) by ends (tuples with XY position).
        """
        # Gets the length of the triangle legs to calculate the angle by tangent.
        adjacent_leg = left_position[0] - right_position[0] # Width
        opposite_leg = left_position[1] - right_position[1] # Height

        # Calculates the angle by tangent.
        angle = math.degrees(math.atan(opposite_leg / adjacent_leg)) if adjacent_leg != 0 else 0

        # If the left position is to the right, it means the steering wheel has turned
        # more than 90 degrees. Then the angle is increased by 90 degrees.
        if left_position[0] >= right_position[0]:

            # If X axis is aligned, it means the steering wheel angle is exactly 90 degrees.
            if left_position[0] == right_position[0]:
                angle = 90 if self.__angle > 0 else -90
            else:
                angle += 180 if angle < 0 else -180

            # Limits the steering wheel angle to 180 degrees.
            if left_position[1] == right_position[1] or angle < 0 < self.__angle or self.__angle < 0 < angle:
                angle = 180 if self.__angle >= 0 else -180

        # Sets the new steering wheel angle.
        self.set_angle(angle)
