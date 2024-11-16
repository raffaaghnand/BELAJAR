import cv2
import numpy as np
import pyfirmata
import time
from threading import Thread
from servo_control import KondisiAwal, CapitTertutup, CapitNaik, CapitTurun, CapitTerbuka

#==========================#
# Arduino Initialization   #
#==========================#
board = pyfirmata.Arduino('/dev/ttyUSB1')
it = pyfirmata.util.Iterator(board)
it.start()

#==========================#
# Pin Configuration       #
#==========================#
# Motor pins
ENA = board.get_pin('d:3:p')
ENB = board.get_pin('d:6:p')
MotorA1 = board.get_pin('d:4:o')
MotorA2 = board.get_pin('d:5:o')
MotorB1 = board.get_pin('d:12:o')
MotorB2 = board.get_pin('d:7:o')

# Ultrasonic pins
TRIG = board.get_pin('d:2:o')
ECHO = board.get_pin('d:8:i')

#==========================#
# Global Variables        #
#==========================#
current_position = "none"
obstacle_detected = False
object_grabbed = False
DETECTION_DISTANCE = 6  # Distance in cm

#==========================#
# Ultrasonic Functions    #
#==========================#
def get_distance():
    TRIG.write(0)
    time.sleep(0.000002)
    TRIG.write(1)
    time.sleep(0.00001)
    TRIG.write(0)
    
    pulse_start = time.time()
    pulse_end = time.time()
    
    while ECHO.read() == 0:
        pulse_start = time.time()
    while ECHO.read() == 1:
        pulse_end = time.time()
    
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    return round(distance, 2)

#==========================#
# Motor Control Functions #
#==========================#
def move_forward():
    MotorA1.write(1)
    MotorA2.write(0)
    MotorB1.write(0)
    MotorB2.write(1)
    ENA.write(0.5)
    ENB.write(0.5)

def move_left():
    MotorA1.write(1)
    MotorA2.write(0)
    MotorB1.write(1)
    MotorB2.write(0)
    ENA.write(0.5)
    ENB.write(0.5)

def move_right():
    MotorA1.write(0)
    MotorA2.write(1)
    MotorB1.write(0)
    MotorB2.write(1)
    ENA.write(0.5)
    ENB.write(0.5)

def stop():
    MotorA1.write(0)
    MotorA2.write(0)
    MotorB1.write(0)
    MotorB2.write(0)
    ENA.write(0)
    ENB.write(0)

#==========================#
# Gripper Functions       #
#==========================#
def grab_object():
    global object_grabbed
    stop()  # Stop robot before closing gripper
    time.sleep(1)  # Wait for robot to completely stop
    CapitTertutup()
    time.sleep(1)
    CapitNaik()
    object_grabbed = True

#==========================#
# Monitoring Functions    #
#==========================#
def ultrasonic_monitor():
    global obstacle_detected, object_grabbed
    while True:
        distance = get_distance()
        if distance < DETECTION_DISTANCE and not object_grabbed:
            obstacle_detected = True
            stop()  # Stop robot when obstacle detected
            time.sleep(1)  # Wait before grabbing
            grab_object()
        else:
            obstacle_detected = False
        time.sleep(0.1)

#==========================#
# Vision Functions        #
#==========================#
def object_detection():
    global current_position
    
    cap = cv2.VideoCapture(0)
    
    while True:
        # Frame capture and resize
        ret, frame = cap.read()
        frame = cv2.resize(frame, (640, 480))
        
        # Image pre-processing
        blurred = cv2.GaussianBlur(frame, (5, 5), 0)
        adjusted = cv2.convertScaleAbs(blurred, alpha=1.3, beta=10)
        
        # Frame division for position detection
        frame_height, frame_width = adjusted.shape[:2]
        left_line = frame_width // 3
        right_line = (frame_width * 2) // 3
        
        # Color detection and masking
        hsv = cv2.cvtColor(adjusted, cv2.COLOR_BGR2HSV)
        lower_blue = np.array([0, 0, 0])
        upper_blue = np.array([179, 195, 131])
        mask = cv2.inRange(hsv, lower_blue, upper_blue)
        
        # Mask enhancement
        kernel = np.ones((5,5), np.uint8)
        mask = cv2.erode(mask, kernel, iterations=1)
        mask = cv2.dilate(mask, kernel, iterations=2)
        
        # Edge detection and combination
        edges = cv2.Canny(mask, 100, 200)
        combined_mask = cv2.bitwise_or(mask, edges)
        
        # Contour detection and processing
        contours, _ = cv2.findContours(combined_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 500:
                # Contour analysis
                perimeter = cv2.arcLength(contour, True)
                approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
                
                x, y, w, h = cv2.boundingRect(contour)
                aspect_ratio = h/w
                
                if aspect_ratio > 1.5 and len(approx) > 6:
                    # Shape analysis
                    hull = cv2.convexHull(contour)
                    hull_area = cv2.contourArea(hull)
                    solidity = float(area)/hull_area
                    
                    if solidity > 0.7:
                        # Visual feedback
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        center_x = x + w//2
                        center_y = y + h//2
                        cv2.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1)
                        
                        # Position determination
                        if center_x < left_line:
                            current_position = "left"
                        elif center_x > right_line:
                            current_position = "right"
                        else:
                            current_position = "center"
                        
                        cv2.putText(frame, f"Position: {current_position}", (10, 30), 
                                  cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # Display results
        cv2.imshow('Object Tracking', frame)
        cv2.imshow('Mask', combined_mask)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

#==========================#
# Robot Control Function  #
#==========================#
def robot_control():
    while True:
        if not obstacle_detected and not object_grabbed:
            if current_position == "center":
                move_forward()
            elif current_position == "left":
                move_left()
            elif current_position == "right":
                move_right()
            else:
                stop()
        time.sleep(0.1)

#==========================#
# Main Program           #
#==========================#
# Initialize servo position
KondisiAwal()

# Thread initialization
ultrasonic_thread = Thread(target=ultrasonic_monitor)
vision_thread = Thread(target=object_detection)
control_thread = Thread(target=robot_control)

# Set threads as daemon
ultrasonic_thread.daemon = True
vision_thread.daemon = True
control_thread.daemon = True

# Start program
try:
    ultrasonic_thread.start()
    vision_thread.start()
    control_thread.start()
    
    # Keep main thread alive
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Program terminated")
    board.exit()