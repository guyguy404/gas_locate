import sys
import rclpy
from rclpy.node import Node
# from rclpy.qos import qos_profile_default
from geometry_msgs.msg import Twist
from interfaces.srv import CarCtrl


class TestNode(Node):
    def __init__(self, name):
        super().__init__(name)
        self.client = self.create_client(CarCtrl, 'car_ctrl')
        self.request = CarCtrl.Request()

    def send_request(self):
        self.request.method = 'rotate'
        self.request.arg1 = 1.0
        self.future = self.client.call_async(self.request)


def main(args=None):
    rclpy.init(args=args)                        # ROS2 Python接口初始化
    node = TestNode("test_node")   # 创建ROS2节点对象并进行初始化
    node.send_request()                          # 发送服务请求

    while rclpy.ok():                            # ROS2系统正常运行
        rclpy.spin_once(node)                    # 循环执行一次节点

        if node.future.done():                   # 数据是否处理完成
            try:
                response = node.future.result()  # 接收服务器端的反馈数据
            except Exception as e:
                node.get_logger().info(
                    'Service call failed %r' % (e,))
            else:
                pass
            break

    node.destroy_node()                          # 销毁节点对象
    rclpy.shutdown()                             # 关闭ROS2 Python接口