#!/usr/bin/env python3

import numpy as np

def kinematika_roda(kecepatan_robot, radius_roda, jarak_ke_pusat, sudut_roda):
    matriks_kinematika = np.array([
        [np.cos(np.deg2rad(sudut_roda[0])), np.sin(np.deg2rad(sudut_roda[0])), -jarak_ke_pusat],
        [np.cos(np.deg2rad(sudut_roda[1])), np.sin(np.deg2rad(sudut_roda[1])), -jarak_ke_pusat],
        [np.cos(np.deg2rad(sudut_roda[2])), np.sin(np.deg2rad(sudut_roda[2])), -jarak_ke_pusat]
    ])
    
    kecepatan_roda = np.dot(matriks_kinematika, kecepatan_robot) / radius_roda
    return kecepatan_roda

def main():
    nama_robot = input().strip()
    kecepatan_robot = []
    for i in range(3):
        kecepatan_robot.append(list(map(float, input(f"Masukkan kecepatan robot baris {i+1}: ").strip().split())))
    kecepatan_robot = np.array(kecepatan_robot)
    perintah = input().strip()

    if nama_robot == "LILDAN":
        radius_roda = 0.0635  
        sudut_roda = [90, 135, 135]  
    elif nama_robot == "DHARMI":
        radius_roda = 0.024  
        sudut_roda = [120, 120, 120]  
    jarak_ke_pusat = 0.15  

    if perintah == "GAS":
        for i in range(3):
            kecepatan_roda = kinematika_roda(kecepatan_robot[i], radius_roda, jarak_ke_pusat, sudut_roda)
            
            tanda_konfigurasi = "∇" if nama_robot == "LILDAN" else "Δ"
            
            print(tanda_konfigurasi)
            for j in range(3):
                print(f"M{j}: {kecepatan_roda[j]:.2f}")

if __name__ == "__main__":
    main()
