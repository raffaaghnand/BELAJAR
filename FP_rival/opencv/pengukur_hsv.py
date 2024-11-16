
import cv2
import numpy as np

def nothing(x):
    pass

# Create a window
cv2.namedWindow('HSV Trackbars')

# Create trackbars for HSV
cv2.createTrackbar('H_min', 'HSV Trackbars', 0, 179, nothing)
cv2.createTrackbar('S_min', 'HSV Trackbars', 0, 255, nothing)
cv2.createTrackbar('V_min', 'HSV Trackbars', 0, 255, nothing)
cv2.createTrackbar('H_max', 'HSV Trackbars', 179, 179, nothing)
cv2.createTrackbar('S_max', 'HSV Trackbars', 255, 255, nothing)
cv2.createTrackbar('V_max', 'HSV Trackbars', 255, 255, nothing)

# Initialize camera
cap = cv2.VideoCapture(0)

while True:
    _, frame = cap.read()
    
    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Get trackbar values
    h_min = cv2.getTrackbarPos('H_min', 'HSV Trackbars')
    s_min = cv2.getTrackbarPos('S_min', 'HSV Trackbars')
    v_min = cv2.getTrackbarPos('V_min', 'HSV Trackbars')
    h_max = cv2.getTrackbarPos('H_max', 'HSV Trackbars')
    s_max = cv2.getTrackbarPos('S_max', 'HSV Trackbars')
    v_max = cv2.getTrackbarPos('V_max', 'HSV Trackbars')
    
    # Define range of color in HSV
    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])
    
    # Create mask
    mask = cv2.inRange(hsv, lower, upper)
    
    # Apply mask to original image
    result = cv2.bitwise_and(frame, frame, mask=mask)
    
    # Show images
    cv2.imshow('Original', frame)
    cv2.imshow('Mask', mask)
    cv2.imshow('Result', result)
    
    # Print current HSV values
    print(f"HSV Range: [{h_min}, {s_min}, {v_min}] to [{h_max}, {s_max}, {v_max}]")
    
    # Break loop with 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
