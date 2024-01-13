import rclpy                                     # ROS2 Python接口库
from rclpy.node import Node                      # ROS2 节点类
import time
from motor_interface.srv import Concentration

class Co2ContractionClient(Node):
    def __init__(self, name):
        super().__init__(name)
        self.client = self.create_client(Concentration, 'concentration')
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('concentration not available, waiting again...')
        self.request = Concentration.Request()

    def send_request(self):
        self.future = self.client.call_async(self.request)


def main(args = None):
    rclpy.init(args = args)
    node_co2 = Co2ContractionClient("co2_client")
    node_co2.send_request()

    while rclpy.ok():                            # ROS2系统正常运行
        rclpy.spin_once(node_co2)                    # 循环执行一次节点

        if node_co2.future.done():                   # 数据是否处理完成
            try:
                response = node_co2.future.result()  # 接收服务器端的反馈数据
            except Exception as e:
                node_co2.get_logger().info(
                    'Service call failed %r' % (e,))
            else:
                node_co2.get_logger().info(          # 将收到的反馈信息打印输出
                    'Concentration now is %d' % response)
            break

    node_co2.destroy_node()
    rclpy.shutdown()