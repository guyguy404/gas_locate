from math import acos, pi
import rclpy
from sim.car_ctrl_node import CarCtrlNode
from sim.gas_info import GasInfo
from sim.state_info_node import StateInfoNode


class Info:
    pos: tuple[float, float]
    """position of the car: (x, y), unit: meter"""

    orien: float
    """orientation of the car (clockwise), range: 0 - 2*PI"""

    gas_conc: float
    """gas concentration"""

    def __init__(
            self, 
            pos: tuple[float, float] = (0, 0), 
            orien: float = 0, 
            gas_conc: float = 0
    ) -> None:
        self.pos = pos
        self.orien = orien
        self.gas_conc = gas_conc
    
    def __str__(self) -> str:
        return f"Info:\n\tpos: {self.pos}\n\torien: {self.orien}\n\tgas_conc: {self.gas_conc}"


class Utils:
    def __init__(self):
        self._car_ctrl_node = CarCtrlNode("car_ctrl_node")
        self._gas_info = GasInfo()
        self._state_info_node = StateInfoNode("state_info_node")

    def forward(self, speed: float):
        self._car_ctrl_node.forward(speed)
    
    def rotate(self, speed: float):
        self._car_ctrl_node.rotate(speed)

    def get_info(self) -> Info:
        state = self._state_info_node.get()
        pos = (state.pose.position.x, state.pose.position.y)
        orien = acos(state.pose.orientation.w) * 2
        gas_conc = self._gas_info.get(pos)
        info = Info(pos, orien, gas_conc)

        return info


def main(args=None):
    rclpy.init(args=args)
    utils = Utils()
    info = utils.get_info()
    print(info)
    rclpy.shutdown()