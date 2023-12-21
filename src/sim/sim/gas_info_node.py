import sys
import rclpy
from rclpy.node import Node
from interfaces.srv import GasInfo


class GasInfoNode(Node):
    def __init__(self, name):
        super().__init__(name)
        self.srv = self.create_service(GasInfo, 'get_gas_info', self.get_gas_info_callback)
    
    def get_gas_info_callback(self, request, response):
        response.conc = self._get_gas_info(request.x, request.y)
        return response

    def _get_gas_info(self, x, y):
        # TODO
        return 0.5


def main(args=None):
    # print(sys.path)
    rclpy.init(args=args)
    node = GasInfoNode('gas_info_node')
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()