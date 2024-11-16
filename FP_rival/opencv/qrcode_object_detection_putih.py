import cv2
import numpy as np

# Initialize webcam
cap = cv2.VideoCapture(0)

# Known width of the QR code in centimeters
KNOWN_WIDTH = 5.0
KNOWN_DISTANCE = 20.0
KNOWN_PIXEL_WIDTH = 100
focal_length = (KNOWN_PIXEL_WIDTH * KNOWN_DISTANCE) / KNOWN_WIDTH

# Initialize QR code detector
qr_detector = cv2.QRCodeDetector()

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
    
    # Detect QR code
    retval, decoded_info, points, straight_qrcode = qr_detector.detectAndDecodeMulti(adjusted)
    
    if retval:
        for i, points_set in enumerate(points):
            if points_set is not None and decoded_info[i] == "PENJARA PUTIH":
                # Convert points to integer
                points_set = points_set.astype(np.int32)
                
                # Draw QR code boundary
                cv2.polylines(adjusted, [points_set], True, (0, 255, 0), 2)
                
                # Calculate center point
                center_x = int(np.mean(points_set[:, 0]))
                center_y = int(np.mean(points_set[:, 1]))
                cv2.circle(adjusted, (center_x, center_y), 5, (0, 0, 255), -1)
                
                # Calculate width of QR code
                w = np.linalg.norm(points_set[0] - points_set[1])
                
                # Calculate distance
                distance = (KNOWN_WIDTH * focal_length) / w
                
                # Position detection
                if center_x < left_line:
                    position = "Left"
                elif center_x > right_line:
                    position = "Right"
                else:
                    position = "Center"
                
                # Display information
                # Show decoded information
                cv2.putText(adjusted, f"Data: {decoded_info[i]}", (center_x + 10, center_y - 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                
                # Show distance
                distance_text = f"Distance: {distance:.1f} cm"
                cv2.putText(adjusted, distance_text, (center_x + 10, center_y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                
                # Show position
                coord_text = f"Position: {position} ({center_x}, {center_y})"
                cv2.putText(adjusted, coord_text, (center_x + 10, center_y + 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
    # Show results
    cv2.imshow('QR Code Detection', adjusted)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

def detect_white_qr(frame):
    # Initialize QR detector
    qr_detector = cv2.QRCodeDetector()
    
    # Resize frame for optimization
    frame = cv2.resize(frame, (640, 480))
    
    # Pre-processing
    blurred = cv2.GaussianBlur(frame, (5, 5), 0)
    alpha = 1.3  # Contrast
    beta = 10    # Brightness
    adjusted = cv2.convertScaleAbs(blurred, alpha=alpha, beta=beta)
    
    # Get frame dimensions
    frame_height, frame_width = adjusted.shape[:2]
    
    # Define area boundaries
    left_line = frame_width // 3
    right_line = (frame_width * 2) // 3
    
    # Detect QR code
    retval, decoded_info, points, straight_qrcode = qr_detector.detectAndDecodeMulti(adjusted)
    
    if retval:
        for i, points_set in enumerate(points):
            if points_set is not None and decoded_info[i] == "PENJARA PUTIH":
                # Calculate center point
                points_set = points_set.astype(np.int32)
                center_x = int(np.mean(points_set[:, 0]))
                
                # Determine position
                if center_x < left_line:
                    return "left"
                elif center_x > right_line:
                    return "right"
                else:
                    return "center"
    
    return "none"  # Return none if no white prison QR code is detected
