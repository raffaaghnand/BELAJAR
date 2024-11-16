import cv2
import numpy as np

# Initialize webcam
cap = cv2.VideoCapture(0)

# Known width of the object in centimeters
KNOWN_WIDTH = 5.0
KNOWN_DISTANCE = 20.0
KNOWN_PIXEL_WIDTH = 100
focal_length = (KNOWN_PIXEL_WIDTH * KNOWN_DISTANCE) / KNOWN_WIDTH

def detect_blue_object(frame):
    # Resize and preprocess frame
    frame = cv2.resize(frame, (640, 480))
    blurred = cv2.GaussianBlur(frame, (5, 5), 0)
    adjusted = cv2.convertScaleAbs(blurred, alpha=1.3, beta=10)
    
    # Convert to HSV and create mask
    hsv = cv2.cvtColor(adjusted, cv2.COLOR_BGR2HSV)
    lower_blue = np.array([0, 0, 0])
    upper_blue = np.array([179, 195, 131])
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    
    # Clean up mask
    kernel = np.ones((5,5), np.uint8)
    mask = cv2.erode(mask, kernel, iterations=1)
    mask = cv2.dilate(mask, kernel, iterations=2)
    
    # Find contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    frame_height, frame_width = frame.shape[:2]
    center_x = frame_width // 2
    
    # Check each contour
    for contour in contours:
        if cv2.contourArea(contour) > 500:
            x, y, w, h = cv2.boundingRect(contour)
            contour_center_x = x + w//2
            
            # Return True if object is in center area
            if abs(contour_center_x - center_x) < 50:
                return True
                
    return False

while True:
    ret, frame = cap.read()
    
    # Resize frame untuk optimasi performa
    frame = cv2.resize(frame, (640, 480))
    
    # Pre-processing
    # 1. Gaussian Blur untuk mengurangi noise
    blurred = cv2.GaussianBlur(frame, (5, 5), 0)
    
    # 2. Contrast and brightness adjustment
    alpha = 1.3  # Contrast
    beta = 10    # Brightness
    adjusted = cv2.convertScaleAbs(blurred, alpha=alpha, beta=beta)
    
    # Get frame dimensions
    frame_height, frame_width = adjusted.shape[:2]
    
    # Draw vertical lines
    left_line = frame_width // 3
    right_line = (frame_width * 2) // 3
    cv2.line(adjusted, (left_line, 0), (left_line, frame_height), (255, 255, 255), 2)
    cv2.line(adjusted, (right_line, 0), (right_line, frame_height), (255, 255, 255), 2)
    
    # Add text labels
    cv2.putText(adjusted, "Left Area", (left_line//3, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    cv2.putText(adjusted, "Center Area", (frame_width//2 - 50, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    cv2.putText(adjusted, "Right Area", (right_line + left_line//3, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    
    # Convert BGR to HSV
    hsv = cv2.cvtColor(adjusted, cv2.COLOR_BGR2HSV)
    
    # Define dark blue color range in HSV
    lower_blue = np.array([0, 0, 0])
    upper_blue = np.array([179, 195, 131])
    
    # Create mask for blue color
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    
    # Morphological operations untuk membersihkan noise
    kernel = np.ones((5,5), np.uint8)
    mask = cv2.erode(mask, kernel, iterations=1)
    mask = cv2.dilate(mask, kernel, iterations=2)
    
    # Edge detection untuk membantu identifikasi bentuk
    edges = cv2.Canny(mask, 100, 200)
    
    # Combine mask dengan edges
    combined_mask = cv2.bitwise_or(mask, edges)
    
    # Find contours
    contours, _ = cv2.findContours(combined_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Process each contour
    for contour in contours:
        area = cv2.contourArea(contour)
        
        # Filter contours based on area and shape
        if area > 500:
            # Calculate contour properties
            perimeter = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
            
            x, y, w, h = cv2.boundingRect(contour)
            aspect_ratio = h/w
            
            # Improved bottle detection criteria
            if aspect_ratio > 1.5 and len(approx) > 6:  # More vertices for rounded objects
                # Calculate contour solidity
                hull = cv2.convexHull(contour)
                hull_area = cv2.contourArea(hull)
                solidity = float(area)/hull_area
                
                # Additional check for bottle-like shapes
                if solidity > 0.7:  # Adjust threshold as needed
                    # Draw rectangle
                    cv2.rectangle(adjusted, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    
                    # Calculate distance with moving average for stability
                    distance = (KNOWN_WIDTH * focal_length) / w
                    
                    # Display distance
                    distance_text = f"Distance: {distance:.1f} cm"
                    cv2.putText(adjusted, distance_text, (x, y - 10), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                    
                    # Draw center point
                    center_x = x + w//2
                    center_y = y + h//2
                    cv2.circle(adjusted, (center_x, center_y), 5, (0, 0, 255), -1)
                    
                    # Position detection
                    if center_x < left_line:
                        position = "Left"
                    elif center_x > right_line:
                        position = "Right"
                    else:
                        position = "Center"
                    
                    # Display coordinates and position
                    coord_text = f"Position: {position} ({center_x}, {center_y})"
                    cv2.putText(adjusted, coord_text, (center_x + 10, center_y), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
    # Show results
    cv2.imshow('Blue Object Detection', adjusted)
    cv2.imshow('Mask', combined_mask)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()