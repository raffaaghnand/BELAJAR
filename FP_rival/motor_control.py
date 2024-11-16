import pyfirmata
import time

# Setup board connection
board = pyfirmata.Arduino('/dev/ttyUSB0')
print("Connected to Arduino")

# Setup iterator thread
iterator = pyfirmata.util.Iterator(board)
iterator.start()

# Pin definitions for motors only
ENA = board.get_pin('d:3:p')
ENB = board.get_pin('d:6:p')
MotorA1 = board.get_pin('d:4:o')
MotorA2 = board.get_pin('d:5:o')
MotorB1 = board.get_pin('d:12:o')
MotorB2 = board.get_pin('d:7:o')

def move_forward():
    MotorA1.write(1)
    MotorA2.write(0)
    MotorB1.write(0)
    MotorB2.write(1)
    ENA.write(0.4)
    ENB.write(0.4)

def move_left():
    MotorA1.write(1)
    MotorA2.write(0)
    MotorB1.write(1)
    MotorB2.write(0)
    ENA.write(0.45)
    ENB.write(0.45)

def move_right():
    MotorA1.write(0)
    MotorA2.write(1)
    MotorB1.write(0)
    MotorB2.write(1)
    ENA.write(0.6)
    ENB.write(0.6)

def stop():
    MotorA1.write(0)
    MotorA2.write(0)
    MotorB1.write(0)
    MotorB2.write(0)
    ENA.write(0)
    ENB.write(0)

def main():
    i = 0
    while True:
        if i % 5 == 0:
            move_right()
        else:
            stop()
    i +=1 

if __name__ == '__main__':
    main()

