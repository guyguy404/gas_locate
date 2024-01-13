import os

from ament_index_python.packages import get_package_share_directory


from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node


def generate_launch_description():


    # Include the robot_state_publisher launch file, provided by our own package. Force sim time to be enabled
    # !!! MAKE SURE YOU SET THE PACKAGE NAME CORRECTLY !!!

    package_name='sim' #<--- CHANGE ME
    world_file_path = 'worlds/sim_env_2m.world'
    
    pkg_path = os.path.join(get_package_share_directory(package_name))
    world_path = os.path.join(pkg_path, world_file_path)  
    
    # Pose where we want to spawn the robot
    spawn_x_val = '0.0'
    spawn_y_val = '0.0'
    spawn_z_val = '0.0'
    spawn_yaw_val = '0.0'
  
    mbot = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory(package_name),'launch','mbot.launch.py'
                )]), launch_arguments={'use_sim_time': 'true', 'world':world_path}.items()
    )

    # Include the Gazebo launch file, provided by the gazebo_ros package
    gazebo = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')]),
             )

    # Run the spawner node from the gazebo_ros package. The entity name doesn't really matter if you only have a single robot.
    def spawn_entity(name, x=0.0, y=0.0, z=0.0, yaw=0.0):
        return Node(package='gazebo_ros', executable='spawn_entity.py',
                    # namespace=name,
                    arguments=['-topic', 'robot_description',
                                '-entity', name, '-robot_namespace', name,
                                '-x', str(x),
                                '-y', str(y),
                                '-z', str(z),
                                '-Y', str(yaw)],
                    output='screen')
    car1 = spawn_entity('car1', -0.5, -0.5, 0.0, 0.0)
    car2 = spawn_entity('car2', 0.5, 0.5, 0.0, 0.0)



    # Launch them all!
    return LaunchDescription([
        mbot,
        gazebo,
        car1,
        car2,
    ])
