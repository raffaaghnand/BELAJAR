
import pyfirmata
import time

# Setup board connection
board = pyfirmata.Arduino('/dev/ttyUSB0')  # Change to your Arduino port
print("Connected to Arduino")

# Create servo objects
#servo_nangkep = board.get_pin('d:10:s')  # Servo nangkep on digital pin 10
servo_ngangkat = board.get_pin('d:10:s')   # Servo ngangkat on digital pin 2

# Setup iterator thread
iterator = pyfirmata.util.Iterator(board)
iterator.start()

def KondisiAwal():
    # Set initial positions
    #servo_nangkep.write(45)
    servo_ngangkat.write(80)
    time.sleep(4)  # 4 seconds delay

def KondisiSetelahnya():
    while True:
        # Nangkep sequence
        #servo_nangkep.write(120)  # Close gripper
        #time.sleep(4)
        
        # Ngangkat sequence
        servo_ngangkat.write(180)  # Lift up
        time.sleep(4)
        
        # Return to initial positions
        servo_ngangkat.write(80)   # Lower down
        time.sleep(4)
        
        #servo_nangkep.write(45)    # Open gripper
        #time.sleep(4)

if __name__ == '__main__':
    KondisiAwal()
    KondisiSetelahnya()
