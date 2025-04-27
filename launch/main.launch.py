# usage:
#
# Default parameter launch...
# ros2 launch slam-workshop-description main.launch.py
#
# Just running rviz...
# ros2 launch slam-workshop-description main.launch.py use_sim_time:=false
#
# Custom Parameters Launch...
# ros2 launch slam-workshop-description main.launch.py \
# use_sim_time:=true \
# rviz_config:=/path/to/rviz/config/file.rivz \
# use_joint_state_gui:=true

import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from ament_index_python.packages import get_package_share_directory
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, Command

def generate_launch_description(): 
    description_dir = get_package_share_directory('slam-workshop-description')
    state_publishers_launch_path = os.path.join(description_dir, 'launch', 'state_publisher.launch.py')
    rviz_config_file = os.path.join(description_dir, 'config', 'display.rviz')
    rviz_launch_path = os.path.join(description_dir, 'launch', 'rviz2.launch.py')
    urdf_file = os.path.join(description_dir, 'urdf', 'mobRob.urdf')

    declare_urdf_file = DeclareLaunchArgument(name='urdf_file', default_value=urdf_file, description='URDF file to load')
    declare_use_sim_time = DeclareLaunchArgument(name='use_sim_time', default_value='true', description='Flag to enable use_sim_time')
    declare_rviz_config = DeclareLaunchArgument(name='rviz_config', default_value=rviz_config_file, description='RViz config file')
    declare_use_joint_state_gui = DeclareLaunchArgument(name='use_joint_state_gui', default_value='false', description='Flag to enable joint_state_publisher_gui')
    declare_update_rate = DeclareLaunchArgument(name='update_rate', default_value='30.0', description='Update rate of publishers')

    use_joint_state_gui = LaunchConfiguration('use_joint_state_gui')
    use_rviz_config = LaunchConfiguration('rviz_config')
    use_sim_time = LaunchConfiguration('use_sim_time')
    update_rate = LaunchConfiguration('update_rate')    
    use_urdf_file = LaunchConfiguration('urdf_file')
    robot_description = Command(['cat ', use_urdf_file])

    start_rviz = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(rviz_launch_path),
        launch_arguments={'use_sim_time': use_sim_time, 'rviz_config': use_rviz_config}.items(),
    )

    start_state_publishers = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(state_publishers_launch_path),
            launch_arguments={
                'use_sim_time': use_sim_time, 'use_joint_state_gui': use_joint_state_gui,
                'update_rate': update_rate, 'robot_description': robot_description}.items(), 
    )

    return LaunchDescription([
        declare_urdf_file,
        declare_rviz_config,
        declare_use_sim_time,
        declare_use_joint_state_gui,
        declare_update_rate,
        start_rviz,
        start_state_publishers,
    ])