# Set the range [lower, upper] according to the color of your controller.
steering_wheel_config = {
    "color_range": { # Color range must be in HSV (H: 0-179, S: 0-255, V: 0-255).
        "left": ([94, 80, 2], [120, 255, 255]),     # Blue Range
        "right": ([25, 52, 72], [102, 255, 255]),   # Green Range
    },
    "minimum_area": 1500,
    "maximum_angle": 180, # Max value must be 180 degrees.
}

app_config = {
    "move_mouse": True,
    "contour_color": (255, 0, 0), # Colors of "contour_color" and "text_color" must be
    "text_color": (255, 0, 0),    # in BGR (blue-green-red) color space.
    "show_steering_wheel_image": True,
    "show_webcam_image": True,
    "steering_wheel_image_filename": "steering_wheel.png",
    "steering_wheel_image_radius": 200
}
