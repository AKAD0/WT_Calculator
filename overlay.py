#---In-game settings:
#   The script is made with respect to the following game settings. It won't work correctly if anything has been setted different.
#       Options -> Main -> Main Parameters -> UI scale = 'Large(100%)'
#       Options -> Graphics -> Resolution = '1920 x 1080'
#       Options -> Main -> Ground Vehicle Battle Settings -> Tactical map Scale = '133%'
#       Options -> Graphics -> Mode = 'Fullscreen'
#       Options -> Main -> Battle Interface -> Safe area in HUD = '100%'
#       Options -> Main -> Battle Interface -> HUD = 'Default'
#---Script settings:
map_scale = 325

#DO NOT TOUCH ANYTHING BELOW
import cv2
import numpy as np
import win32gui
import win32con
point1 = None
point2 = None
selected = False

# Mouse callback function
def select_point(event, x, y, flags, params):
    global point1, point2, selected
    if event == cv2.EVENT_LBUTTONDOWN:
        if not selected:
            point1 = (x, y)
            selected = True
        else:
            point2 = (x, y)
            selected = False

# Create a black image, a window and bind the function to window
image = np.zeros((432, 432, 3), dtype=np.uint8)
cv2.namedWindow("Image")
cv2.setMouseCallback("Image", select_point)

# Calculate distance between two points
def calculate_distance(point1, point2):
    return np.sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2)

# Transparency
def make_transparent(hwnd):
    # Get the window style
    style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
    # Set the window style with WS_EX_LAYERED flag to make it transparent
    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, style | win32con.WS_EX_LAYERED)
    # Set the transparency level (0-255, 0 being fully transparent and 255 being opaque)
    win32gui.SetLayeredWindowAttributes(hwnd, 0, 200, win32con.LWA_ALPHA)

# Find the handle of the window you want to make transparent
# Spy++ to find the window class and title: https://github.com/strobejb/winspy/releases/tag/v1.8.4
hwnd = win32gui.FindWindow("Main HighGUI class", "Image")

# Main loop
while True:
    # Legend
    if hwnd:
        make_transparent(hwnd)
    cv2.putText(image, f"Scale (m): {map_scale:.2f}", (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255),1)
    cv2.putText(image, f"Distance (m):", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255),1)
    cv2.putText(image, f"Hold Tab to Reset", (20, 400), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255),1)
    cv2.putText(image, f"Hold ESC to exit", (20, 420), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255),1)

    # Draw
    cv2.imshow("Image", image)
    if point1 is not None:
        cv2.circle(image, point1, 5, (0, 255, 0), -1)
    if point2 is not None:
        cv2.circle(image, point2, 5, (0, 0, 255), -1)
        distance = calculate_distance(point1, point2) * 3.478 * (map_scale/200)
        cv2.putText(image, f"Distance (m): {distance:.2f}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255),1)
    
    # Reset
    if cv2.waitKey(1) & 0xFF == 9:     # '~' key
        image = np.zeros((432, 432, 3), dtype=np.uint8)
        point1 = None
        point2 = None
        selected = False
    
    # Exit
    if cv2.waitKey(1) & 0xFF == 27:     # 'ESC' key
        break

# Close all OpenCV windows
cv2.destroyAllWindows()