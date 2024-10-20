#!/usr/bin/env python3

import rospy
import math
from geometry_msgs.msg import Twist
from turtlesim.srv import TeleportAbsolute, TeleportAbsoluteRequest
from turtlesim.srv import SetPen

def draw_raf():
    rospy.init_node('turtle_draw_raf', anonymous=True)
    pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    rospy.wait_for_service('/turtle1/teleport_absolute')
    rospy.wait_for_service('/turtle1/set_pen')
    teleport = rospy.ServiceProxy('/turtle1/teleport_absolute', TeleportAbsolute)
    set_pen = rospy.ServiceProxy('/turtle1/set_pen', SetPen)
    
    def draw_line(duration, linear_x, angular_z):
        move_cmd = Twist()
        move_cmd.linear.x = linear_x
        move_cmd.angular.z = angular_z
        start_time = rospy.Time.now()
        while (rospy.Time.now() - start_time) < rospy.Duration(duration):
            pub.publish(move_cmd)
            rate.sleep()
        move_cmd.linear.x = 0.0
        move_cmd.angular.z = 0.0
        pub.publish(move_cmd)

    def rotate(angle):
        move_cmd = Twist()
        move_cmd.angular.z = angle
        start_time = rospy.Time.now()
        while (rospy.Time.now() - start_time) < rospy.Duration(1):
            pub.publish(move_cmd)
            rate.sleep()
        move_cmd.angular.z = 0.0
        pub.publish(move_cmd)

    def move_without_drawing(x, y, theta):
        set_pen(255, 255, 255, 2, 1) 
        teleport(TeleportAbsoluteRequest(x=x, y=y, theta=theta))
        set_pen(255, 0, 0, 2, 0)  

    rate = rospy.Rate(10) 

    # Gambar 'R'
    move_without_drawing(2, 2, math.pi/2)
    draw_line(2, 1.0, 0)
    rotate(-math.pi/2)
    draw_line(1, 1.0, 0)
    rotate(-math.pi/2)
    draw_line(1, 1.0, 0)
    rotate(-math.pi/4)
    draw_line(math.sqrt(2), 1.0, 0) 

    # Gambar 'A'
    move_without_drawing(4, 2, math.pi/4)
    draw_line(2*math.sqrt(2), 1.0, 0)
    rotate(-3*math.pi/4)
    draw_line(2*math.sqrt(2), 1.0, 0)
    move_without_drawing(4.5, 3, 0)

    # Gambar 'F'
    move_without_drawing(6, 2, math.pi/2)
    draw_line(2, 1.0, 0)
    rotate(-math.pi/2)
    draw_line(1, 1.0, 0)
    move_without_drawing(6, 3, 0)
    draw_line(1, 1.0, 0)

if __name__ == '__main__':
    try:
        draw_raf()
    except rospy.ROSInterruptException:
        pass