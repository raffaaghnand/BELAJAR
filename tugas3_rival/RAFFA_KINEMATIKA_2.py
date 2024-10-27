#!/usr/bin/env python3

import numpy as np

def dh_transform(a, alpha, d, theta):
    alpha = np.deg2rad(alpha)
    theta = np.deg2rad(theta)
    return np.array([
        [np.cos(theta), -np.sin(theta)*np.cos(alpha), np.sin(theta)*np.sin(alpha), a*np.cos(theta)],
        [np.sin(theta), np.cos(theta)*np.cos(alpha), -np.cos(theta)*np.sin(alpha), a*np.sin(theta)],
        [0, np.sin(alpha), np.cos(alpha), d],
        [0, 0, 0, 1]
    ])

def main():
    input_data = input().strip().split()
    nama_robot = input_data[0]
    theta1 = float(input_data[1])
    theta2 = float(input_data[2])
    theta3 = float(input_data[3])

    if nama_robot == "L":
        dh_params = [
            [0, 90, 5, theta1],
            [3, 0, 0, theta2],
            [2, 0, 0, theta3]
        ]

    elif nama_robot == "D":
        dh_params = [
            [0, 90, 6, theta1],
            [3, 0, 0, theta2],
            [2, 0, 0, theta3]
        ]

    T = np.eye(4)
    for params in dh_params:
        T = np.dot(T, dh_transform(*params))


    x, y, z = T[0, 3], T[1, 3], T[2, 3]
    print(f"{x:.2f}")
    print(f"{y:.2f}")
    print(f"{z:.2f}")

if __name__ == "__main__":
    main()
