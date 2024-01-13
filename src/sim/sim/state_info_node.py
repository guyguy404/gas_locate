import sys
import rclpy
from rclpy.node import Node
from gazebo_msgs.srv import GetEntityState


class StateInfoNode(Node):
    def __init__(self, name):
        super().__init__(name)
        self.client = self.create_client(GetEntityState, '/gazebo/get_entity_state')
    
    def send_request(self, car_name):
        request = GetEntityState.Request()
        request.name = car_name
        request.reference_frame = "world"
        return self.client.call_async(request)

    def get(self):
        future_dict = {
            "car1": self.send_request("car1"),
            "car2": self.send_request("car2")
        }
        done_num = 0
        done_dict = {
            car_name: False
            for car_name, _ in future_dict.items()
        }
        ret_dict = {}

        while rclpy.ok():
            rclpy.spin_once(self)

            for car_name, future in future_dict.items():
                if done_dict[car_name]:
                    continue
                if future.done():
                    try:
                        response = future.result()
                    except Exception as e:
                        self.get_logger().info(
                            'Service call failed %r' % (e,))
                    else:
                        done_num += 1
                        done_dict[car_name] = True
                        ret_dict[car_name] = response.state

                        if done_num == len(future_dict):
                            return ret_dict
            