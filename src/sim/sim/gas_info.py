import os
import numpy as np
from scipy.spatial import KDTree
from ament_index_python.packages import get_package_share_directory


class GasInfo:
    def __init__(self):
        data_file_path = 'data/gas_conc_data.csv'
        pkg_path = os.path.join(get_package_share_directory('sim'))
        data_path = os.path.join(pkg_path, data_file_path)

        self.raw = np.loadtxt(data_path, delimiter=',')
        self.pos2conc = {}
        for i in range(self.raw.shape[0]):
            self.pos2conc[(self.raw[i, 0], self.raw[i, 2])] = self.raw[i, 3]
        self.points= self.raw[:, [0, 2]]
        self.kdtree = KDTree(self.points)
    
    def get(self, pos: tuple[float, float]) -> float:
        pos = (pos[0] / 4, pos[1] / 4)
        dist, idx = self.kdtree.query(pos)
        point = self.points[idx]
        return self.pos2conc[(point[0], point[1])]
