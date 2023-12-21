from setuptools import find_packages, setup
import os
from glob import glob


package_name = 'sim'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*.launch.py'))),
        (os.path.join('share', package_name, 'urdf'), glob(os.path.join('urdf', '*.*'))),
        (os.path.join('share', package_name, 'urdf/sensors'), glob(os.path.join('urdf/sensors', '*.*'))),
        (os.path.join('share', package_name, 'worlds'), glob(os.path.join('worlds', '*.*'))),  
        (os.path.join('share', package_name, 'data'), glob(os.path.join('data', '*.*'))),  

    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='hcx',
    maintainer_email='hcx@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'gas_info_node = sim.gas_info_node:main',
            'car_ctrl_node = sim.car_ctrl_node:main',
            'test_node = sim.test_node:main',
            'utils = sim.utils:main',
            'algo = sim.algo:main'
        ],
    },
)
