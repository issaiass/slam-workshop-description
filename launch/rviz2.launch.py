# usage:
#
# Default parameter launch...
# ros2 launch slam-workshop-description rviz2.launch.py
#
# Custom Parameters Launch...
# ros2 launch slam-workshop-description rviz2.launch.py \
# rviz_config:=/path/to/rviz/config/file.rivz

from ament_index_python import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
import os


def generate_launch_description():
    description_dir = get_package_share_directory('slam-workshop-description')
    rviz_config_file = os.path.join(description_dir, 'config', 'display.rviz')

    declare_use_sim_time = DeclareLaunchArgument(name='use_sim_time', default_value='false', description='Use simulation time')
    declare_rviz_config = DeclareLaunchArgument(name='rviz_config', default_value=rviz_config_file, description='RViz config file')
    use_rviz_config = LaunchConfiguration('rviz_config')
    use_sim_time = LaunchConfiguration('use_sim_time')

    rviz2_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        parameters=[{'use_sim_time': use_sim_time}],
        arguments=["-d", use_rviz_config]
    )

    return LaunchDescription([
        declare_rviz_config,
        declare_use_sim_time,
        rviz2_node
    ])