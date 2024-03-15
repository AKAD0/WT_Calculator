#To keep the windows on top of every other you can use 'Always on Top' function within 'Microsoft PowerToys' available in microsoft store for free.

#---In-game settings:
#   The script was tested with following game setting:
#       Options -> Main -> Main Parameters -> UI scale = 'Large(100%)'
#       Options -> Graphics -> Resolution = '1920 x 1080'
#       Options -> Main -> Ground Vehicle Battle Settings -> Tactical map Scale = '133%'
#       Options -> Graphics -> Mode = 'Fullscreen'
#       Options -> Main -> Battle Interface -> Safe area in HUD = '100%'
#       Options -> Main -> Battle Interface -> HUD = 'Default'
#---Script settings:
scale_map = 200

#DO NOT TOUCH ANYTHING BELOW
import cv2
import numpy as np
import win32gui
import win32con
point1 = None
point2 = None
selected = False
calibrate = 1 
scale_unit = 1
scale_coef = 1
distance_unit = 1
distance_map = 1

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
image = np.zeros((520, 440, 3), dtype=np.uint8)
cv2.namedWindow("Image")
cv2.setMouseCallback("Image", select_point)

# Calculate distance between two points
def calculate_distance(point1, point2):
    if (point1 != None) and (point2 != None):
        return np.sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2)
    else:
        return False

# Transparency
def make_transparent(hwnd):
    # Get the window style
    style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
    # Set the window style with WS_EX_LAYERED flag to make it transparent
    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, style | win32con.WS_EX_LAYERED)
    # Set the transparency level (0-255, 0 being fully transparent and 255 being opaque)
    win32gui.SetLayeredWindowAttributes(hwnd, 0, 100, win32con.LWA_ALPHA)

# Find the handle of the window you want to make transparent
# Spy++ to find the window class and title: https://github.com/strobejb/winspy/releases/tag/v1.8.4
hwnd = win32gui.FindWindow("Main HighGUI class", "Image")

# Main loop
while True:
    # Legend
    if hwnd:
        make_transparent(hwnd)
    if scale_coef == 1:
        cv2.putText(image, f"Calibration:        <Calibration is needed>", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255),1)
    cv2.putText(image, f"Map scale (m): {scale_map:.2f}", (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255),1)
    cv2.putText(image, f"Calibration: {scale_coef:.2f}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255),1)
    cv2.putText(image, f"Distance (m):", (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255),1)
    cv2.putText(image, f"Hold Tab to Reset", (20, 480), cv2.FONT_HERSHEY_SIMPLEX, 0.25, (255, 255, 255),1)
    cv2.putText(image, f"Hold ESC to Exit", (20, 490), cv2.FONT_HERSHEY_SIMPLEX, 0.25, (255, 255, 255),1)
    cv2.putText(image, f"Hold Tilda (~) to Calibrate", (20, 500), cv2.FONT_HERSHEY_SIMPLEX, 0.25, (255, 255, 255),1)
    cv2.putText(image, f"Calibration: set 'scale_map'; measure 5 map squares with 2 dots; depress Tilda; depress Tab.", (20, 510), cv2.FONT_HERSHEY_SIMPLEX, 0.25, (255, 255, 255),1)

    # Draw
    cv2.imshow("Image", image)
    if point1 is not None:
        cv2.circle(image, point1, 5, (0, 255, 0), -1)
    if point2 is not None:
        cv2.circle(image, point2, 5, (0, 0, 255), -1)
        distance_unit = calculate_distance(point1, point2)
        distance_map = distance_unit*scale_coef
        cv2.putText(image, f"Distance (m): {distance_map:.2f}", (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255),1)
    
    # Reset
    if cv2.waitKey(1) & 0xFF == 9:     # 'Tab' key
        image = np.zeros((520, 440, 3), dtype=np.uint8)
        point1 = None   
        point2 = None
        selected = False

    # Calibrate
    if cv2.waitKey(1) & 0xFF == 96:     # '~' key
        calibrate = calculate_distance(point1, point2)
        if calibrate!=False:
            scale_unit = calibrate/5
            scale_map = scale_map
            scale_coef = scale_map/scale_unit
    
    # Exit
    if cv2.waitKey(1) & 0xFF == 27:     # 'ESC' key
        break

# Close all OpenCV windows
cv2.destroyAllWindows()
