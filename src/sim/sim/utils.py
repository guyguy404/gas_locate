from math import acos, pi
import rclpy
from sim.car_ctrl_node import CarCtrlNode
from sim.gas_info import GasInfo
from sim.state_info_node import StateInfoNode


class Info:
    pos: list[float]
    """position of the car: (x, y), unit: meter"""

    orien: float
    """orientation of the car (clockwise), range: 0 - 2*PI"""

    gas_conc: float
    """gas concentration"""

    def __init__(
            self, 
            pos: list[float] = [0.0, 0.0],
            orien: float = 0.0,
            gas_conc: float = 0.0
    ) -> None:
        self.pos = pos
        self.orien = orien
        self.gas_conc = gas_conc
    
    def __repr__(self) -> str:
        return f"Info:\n\tpos: {self.pos}\n\torien: {self.orien}\n\tgas_conc: {self.gas_conc}\n"


class Utils:
    def __init__(self):
        self.car_name_list = [
            "car1",
            "car2",
        ]
        self._car_ctrl_node_dict = {
            car_name: CarCtrlNode(car_name)
            for car_name in self.car_name_list
        }
        self._gas_info = GasInfo()
        self._state_info_node = StateInfoNode("state_info_node")

    def forward(self, car_name, speed: float):
        self._car_ctrl_node_dict[car_name].forward(float(speed))
    
    def rotate(self, car_name, speed: float):
        self._car_ctrl_node_dict[car_name].rotate(float(speed))
    
    def get_info(self) -> dict[str, Info]:
        state_dict = self._state_info_node.get()
        ret_dict = {}
        for car_name, state in state_dict.items():
            pos = [state.pose.position.x, state.pose.position.y]
            orien = acos(state.pose.orientation.w) * 2
            gas_conc = self._gas_info.get(pos)
            info = Info(pos, orien, gas_conc)
            ret_dict[car_name] = info

        return ret_dict


def main(args=None):
    rclpy.init(args=args)
    utils = Utils()
    info = utils.get_info()
    print(info)
    utils.forward("car1", 0.2)
    utils.rotate("car2", 0.2)
    rclpy.shutdown()