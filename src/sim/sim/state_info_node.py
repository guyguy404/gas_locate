import sys
import rclpy
from rclpy.node import Node
from gazebo_msgs.srv import GetEntityState


class StateInfoNode(Node):
    def __init__(self, name):
        super().__init__(name)
        self.client = self.create_client(GetEntityState, '/gazebo/get_entity_state')
        self.request = GetEntityState.Request()
    
    def send_request(self):
        self.request.name = "mbot"
        self.request.reference_frame = "world"
        self.future = self.client.call_async(self.request)

    def get(self):
        self.send_request()

        while rclpy.ok():
            rclpy.spin_once(self)

            if self.future.done():
                try:
                    response = self.future.result()
                except Exception as e:
                    self.get_logger().info(
                        'Service call failed %r' % (e,))
                else:
                    # print(response.state)
                    return response.state
                break
