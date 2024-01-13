import sys

import rclpy                      # ROS2 Python接口库
from rclpy.node   import Node     # ROS2 节点类
from std_msgs.msg import String

from motor_interface.srv import SetMotorSrv

class MotorRequest:
    get: bool
    direction: str
    speed: int
    angle: int

class MotorPublisher(Node):
    def __init__(self, name):
        super().__init__(name)
        
        self.client = self.create_client(SetMotorSrv,
                                       'set_motor',)
        
        while not self.client.wait_for_service(timeout_sec=1.0):     # 循环等待服务器端成功启动
            self.get_logger().info('service not available, waiting again...') 
        self.request = SetMotorSrv.Request()                          # 创建服务请求的数据对象

        
    def send_request(self):
        self.request.direction = MotorRequest.direction
        self.request.speed = MotorRequest.speed
        self.request.angle = MotorRequest.angle
        self.future = self.client.call_async(self.request)


def main(args = None):
    rclpy.init(args = args)
    node_motor = MotorPublisher("motor_client")
    node_motor.send_request()

    while rclpy.ok():                            # ROS2系统正常运行
        rclpy.spin_once(node_motor)                    # 循环执行一次节点

        if node_motor.future.done():                   # 数据是否处理完成
            try:
                response = node_motor.future.result()  # 接收服务器端的反馈数据
            except Exception as e:
                node_motor.get_logger().info(
                    'Service call failed %r' % (e,))
            else:
                node_motor.get_logger().info(          # 将收到的反馈信息打印输出
                    'Car move %s %d speed %d angle successfully! %d'
                    (node_motor.request.direction, node_motor.request.speed,
                     node_motor.request.angle ,response.success))
            break

    node_motor.destroy_node()
    rclpy.shutdown()