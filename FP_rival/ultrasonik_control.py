import pyfirmata
import time

# Inisialisasi board Arduino
board = pyfirmata.Arduino('/dev/ttyUSB0')
it = pyfirmata.util.Iterator(board)
it.start()

# Setup pin ultrasonik
TRIG = board.get_pin('d:2:o')
ECHO = board.get_pin('d:8:i')

def deteksi_objek():
    try:
        while True:
            # Trigger ultrasonik
            TRIG.write(0)
            time.sleep(0.000002)
            TRIG.write(1)
            time.sleep(0.00001)
            TRIG.write(0)
            
            # Baca waktu pantulan
            pulse_start = time.time()
            pulse_end = time.time()
            
            while ECHO.read() == 0:
                pulse_start = time.time()
            while ECHO.read() == 1:
                pulse_end = time.time()
            
            # Hitung jarak
            pulse_duration = pulse_end - pulse_start
            distance = pulse_duration * 17150
            
            # Deteksi objek pada jarak <= 6 cm
            if distance <= 6:
                print(f"Objek terdeteksi! Jarak: {round(distance, 2)} cm")
            
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("\nProgram dihentikan")
    finally:
        board.exit()

# Jalankan program
print("Program deteksi objek dimulai...")
print("Tekan Ctrl+C untuk menghentikan program")
deteksi_objek()