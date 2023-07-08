import time
import cv2
import pyautogui
import keyboard
import numpy as np

time.sleep(5)

def find_and_move_cursor(target_image):
    # Define the ROI
    roi_top_left = (970, 378)
    roi_bottom_right = (1080, 827)

    roi_x = roi_top_left[0]
    roi_y = roi_top_left[1]
    roi_width = roi_bottom_right[0] - roi_top_left[0]
    roi_height = roi_bottom_right[1] - roi_top_left[1]

    # Initialize the paused flag variable
    paused = False

    while True:
        # Check if the "l" key is pressed to pause/start the script
        if keyboard.is_pressed('l'):
            paused = not paused
            if paused:
                print("Script paused. Press 'l' to resume.")
            else:
                print("Script resumed.")

            # Wait until the 'l' key is released
            while keyboard.is_pressed('l'):
                pass

        # Break the loop if the "q" key is pressed
        if keyboard.is_pressed('q'):
            break

        if not paused:
            try:
                # Capture the screen frame within the ROI
                screen_frame = pyautogui.screenshot(region=(roi_x, roi_y, roi_width, roi_height))

                # Convert the screenshot to a numpy array representation
                screen_frame = cv2.cvtColor(np.array(screen_frame), cv2.COLOR_RGB2BGR)

                # Perform template matching within the ROI
                result = cv2.matchTemplate(screen_frame, target_image, cv2.TM_CCOEFF_NORMED)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

                # Set a threshold for the match value to consider it a valid detection
                threshold = 0.1

                if max_val >= threshold:
                    # Extract the top-left corner coordinates of the target image within the ROI
                    top_left_x = max_loc[0]
                    top_left_y = max_loc[1]

                    # Calculate the center coordinates of the target image within the ROI
                    target_width = target_image.shape[1]
                    target_height = target_image.shape[0]
                    target_center_x = roi_x + top_left_x + target_width // 2
                    target_center_y = roi_y + top_left_y + target_height // 2 - 37

                    # Move the mouse cursor to the desired location
                    pyautogui.moveTo(target_center_x, target_center_y)

            except Exception as e:
                print("An error occurred:")
                print(e)
            time.sleep(0.001)


# Load the target image (Pong)
target_image = cv2.imread('C:/Users/User/Desktop/pong.png')

# Pause/Start functionality
print("Press 'l' to pause/start the script. Press 'q' to quit.")

# Call the find_and_move_cursor function
find_and_move_cursor(target_image)

# Keep the script running until manually closed
while True:
    pass
