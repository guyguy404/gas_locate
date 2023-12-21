import sys
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from interfaces.srv import CarCtrl


class CarCtrlNode(Node):
    def __init__(self, name):
        super().__init__(name)
        self.srv = self.create_service(CarCtrl, 'car_ctrl', self.car_ctrl_callback)
        self.pub = self.create_publisher(Twist, 'cmd_vel', 10)
    
    def car_ctrl_callback(self, request, response):
        self.get_logger().info("callback")
        
        method: str = request.method
        arg1: float = request.arg1

        if method == 'forward':
            self.forward(arg1)
        elif method == 'rotate':
            self.rotate(arg1)
        else:
            self.get_logger().error("Unknown CarCtrl method!")

        return response

    def forward(self, speed: float):
        twist = Twist()
        twist.linear.x = speed
        twist.linear.y = 0.0
        twist.linear.z = 0.0
        twist.angular.x = 0.0
        twist.angular.y = 0.0
        twist.angular.z = 0.0
        
        self.pub.publish(twist)

    def rotate(self, speed: float):
        twist = Twist()
        twist.linear.x = 0.1
        twist.linear.y = 0.0
        twist.linear.z = 0.0
        twist.angular.x = 0.0
        twist.angular.y = 0.0
        twist.angular.z = speed

        self.pub.publish(twist)

def main(args=None):
    rclpy.init(args=args)
    node = CarCtrlNode('car_ctrl_node')
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()