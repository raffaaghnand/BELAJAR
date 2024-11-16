import pyfirmata
import time

# Setup board connection
board = pyfirmata.Arduino('/dev/ttyUSB1')  
print("Connected to Arduino")

# Create servo objects
servo_nangkep = board.get_pin('d:11:s')  
servo_ngangkat = board.get_pin('d:10:s')   

# Setup iterator thread
iterator = pyfirmata.util.Iterator(board)
iterator.start()

def KondisiAwal():
    servo_nangkep.write(50)    # Capit terbuka
    servo_ngangkat.write(80)   # Capit turun
    time.sleep(4)  

def CapitTertutup():
    servo_nangkep.write(120)   # Capit tertutup
    time.sleep(4)

def CapitNaik():
    servo_ngangkat.write(180)  # Capit naik
    time.sleep(4)

def CapitTurun():
    servo_ngangkat.write(80)   # Capit turun
    time.sleep(4)

def CapitTerbuka():
    servo_nangkep.write(50)    # Capit terbuka
    time.sleep(4)
