import cv2
import time
from opencv.blue_object_detection import *
from opencv.qrcode_object_detection_biru import *
from opencv.white_object_detection import *
from opencv.qrcode_object_detection_putih import *
from motor_control import *
from servo_control import *
from ultrasonik_control import *


# Initialize camera
cap = cv2.VideoCapture(0)

def get_object_position(frame, detect_func):
    frame_width = frame.shape[1]
    result, x = detect_func(frame, return_position=True)
    if result:
        if x < frame_width/3:
            return "left"
        elif x > 2*frame_width/3:
            return "right"
        else:
            return "center"
    return None

def main():
    # Variables to track object states
    blue_object_carried = False
    white_object_carried = False
    
    # 1. BLUE OBJECT DETECTION AND PICKUP
    KondisiAwal()  # Open gripper initially
    
    while not blue_object_carried:
        ret, frame = cap.read()
        position = get_object_position(frame, detect_blue_object)
        if position == "center":
            move_forward()
            if deteksi_objek() <= 6:
                stop()
                CapitTertutup()
                CapitNaik()
                blue_object_carried = True
                break
        elif position == "left":
            move_left()
        elif position == "right":
            move_right()
    
    # 2. FIND BLUE PRISON QR CODE
    while blue_object_carried:
        ret, frame = cap.read()
        position = get_object_position(frame, detect_blue_qr)
        if position == "center":
            move_forward()
            if deteksi_objek() <= 6:
                stop()
                CapitTurun()
                CapitTerbuka()
                blue_object_carried = False
                break
        elif position == "left":
            move_left()
        elif position == "right":
            move_right()
    
    # 3. WHITE OBJECT DETECTION AND PICKUP
    KondisiAwal()  # Reset gripper position
    
    while not white_object_carried:
        ret, frame = cap.read()
        position = get_object_position(frame, detect_white_object)
        if position == "center":
            move_forward()
            if deteksi_objek() <= 6:
                stop()
                CapitTertutup()
                CapitNaik()
                white_object_carried = True
                break
        elif position == "left":
            move_left()
        elif position == "right":
            move_right()
    
    # 4. FIND WHITE PRISON QR CODE
    while white_object_carried:
        ret, frame = cap.read()
        position = get_object_position(frame, detect_white_qr)
        if position == "center":
            move_forward()
            if deteksi_objek() <= 6:
                stop()
                CapitTurun()
                CapitTerbuka()
                white_object_carried = False
                break
        elif position == "left":
            move_left()
        elif position == "right":
            move_right()
    
    # End program
    stop()
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        stop()
        cap.release()
        cv2.destroyAllWindows()