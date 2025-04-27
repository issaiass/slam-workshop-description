# usage:
#
# Default parameter launch...
# ros2 launch slam-workshop-description state_publisher.launch.py
#
# Custom Parameters Launch...
# ros2 launch slam-workshop-description state_publisher.launch.py \
# use_sim_time:=true \
# use_urdf:=/path/to/urdf/file.urdf \
# use_joint_state_gui:=true
# update_rate:=30.0

from ament_index_python import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, Command
from launch_ros.descriptions import ParameterValue
from launch.conditions import IfCondition, UnlessCondition
from launch_ros.actions import Node
import os


def generate_launch_description():
    description_dir = get_package_share_directory('slam-workshop-description')
    urdf_file = os.path.join(description_dir, 'urdf', 'mobRob.urdf')

    declare_urdf_file = DeclareLaunchArgument(name='urdf_file', default_value=urdf_file, description='URDF file to load')
    declare_use_sim_time = DeclareLaunchArgument(name='use_sim_time', default_value='False', description='Flag to enable use_sim_time')
    declare_use_joint_state_gui = DeclareLaunchArgument(name='use_joint_state_gui', default_value='False', description='Flag to enable joint_state_publisher_gui')
    declare_update_rate = DeclareLaunchArgument(name='update_rate', default_value='30.0', description='Update rate of publishers')

    use_urdf_file = LaunchConfiguration('urdf_file')
    robot_description = ParameterValue(Command(['cat ', use_urdf_file]), value_type=str)
    use_sim_time = LaunchConfiguration('use_sim_time')
    use_joint_state_gui = LaunchConfiguration('use_joint_state_gui')
    update_rate = LaunchConfiguration('update_rate')

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_description, 'use_sim_time': use_sim_time}]
    )

    joint_state_publisher_node = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        output='screen',
        parameters=[{'use_sim_time': use_sim_time, 'update_rate':update_rate}],
        condition=UnlessCondition(use_joint_state_gui)
    )

    joint_state_publisher_gui_node = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui',
        output='screen',
        parameters=[{'use_sim_time': use_sim_time, 'update_rate':update_rate}],
        condition=IfCondition(use_joint_state_gui)
    )

    return LaunchDescription([
        declare_use_sim_time,
        declare_use_joint_state_gui,
        declare_urdf_file,
        declare_update_rate,
        robot_state_publisher_node,
        joint_state_publisher_node,
        joint_state_publisher_gui_node
    ])