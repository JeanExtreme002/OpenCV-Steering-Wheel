__author__ = "Jean Loui Bernard Silva de Jesus"

from config import app_config, steering_wheel_config
from detection import detect_objects_by_color_range
from mouseController import MouseController
from steeringWheel import SteeringWheel
import cv2, os

# Creates the steering wheel and sets it to the controller.
steering_wheel = SteeringWheel(
    filename = os.path.join("images", app_config["steering_wheel_image_filename"]),
    radius = app_config["steering_wheel_image_radius"],
    maximum_angle = steering_wheel_config["maximum_angle"]
)
mouse_controller = MouseController(steering_wheel)
if app_config["move_mouse"]: mouse_controller.start()

# Inverts the colors (left color becomes right color and right color becomes left color) because
# there is not mirror effect to the webcam image.
steering_wheel_colors = list(steering_wheel_config["color_range"].values())[::-1]

# Text style of the webcam frame.
text_style = (cv2.FONT_HERSHEY_SIMPLEX, 1.0, app_config["text_color"], 2)

# Opens the default webcam.
webcam = cv2.VideoCapture(0)

# Reads the video from the webcam in image frames while the webcam is opened
# and detects the steering wheel by the color range of each end.
while webcam.isOpened():
    webcam_status, webcam_frame = webcam.read()

    # Detects the steering wheel ends.
    steering_wheel_ends = detect_objects_by_color_range(
        webcam_frame, steering_wheel_colors,
        minimum_area = steering_wheel_config["minimum_area"],
        color = app_config["contour_color"]
    )

    # Sets the steering wheel angle through two positions.
    if len(steering_wheel_ends) == 2:
        mouse_controller.resume()
        steering_wheel.set_angle_by_ends(*steering_wheel_ends)
    else:
        mouse_controller.pause()

    # Inserts the steering wheel angle on webcam frame and shows the image.
    if app_config["show_webcam_image"]:
        cv2.putText(webcam_frame, "Angle: %.1f" % steering_wheel.get_angle(), (20, 50), *text_style)
        cv2.imshow("Webcam", webcam_frame)

    # Shows the steering wheel image.
    if app_config["show_steering_wheel_image"]:
        cv2.imshow("Steering Wheel", steering_wheel.get_image())

    # Terminates the program whether the key pressed is "Esc" (keycode 27).
    if cv2.waitKey(1) == 27:
        mouse_controller.stop()
        webcam.release()
        cv2.destroyAllWindows()
