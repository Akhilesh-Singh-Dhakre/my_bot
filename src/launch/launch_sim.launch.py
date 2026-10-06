import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node


def generate_launch_description():


        package_name='my_bot'

        # Including launch description for the bot

        rsp = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                        get_package_share_directory(package_name), 'launch', 'rsp.launch.py'
                )]),    launch_arguments={'use_sim_time':'true'}.items()
        )

        # Include the Gazebo launch file, provided by the ros_gz_sim package

        gazebo = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                        get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py'
                )]),
                launch_arguments={'gz_args': '-r empty.sdf'}.items()
        )

        #bridge to connect teleop twist keyboard and gazebo

        gz_bridge = Node(
                package='ros_gz_bridge',
                executable='parameter_bridge',
                name='ros_gz_bridge',
                output='screen',
                # if you want to use a yaml file enable below code
                #parameters=[{'config_file': os.path.join(get_package_share_directory('ros_gz_bridge'),'config', 'ros_gz_bridge_config.yaml')}],
                arguments=[
                        '/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist',
                        '/odom@nav_msgs/msg/Odometry[gz.msgs.Odometry', # Optional: bridges odometry back to ROS 2
                        '/tf@tf2_msgs/msg/TFMessage[gz.msgs.Pose_V'     # Optional: bridges transforms back to ROS 2
                ]
        )

        # Run the create node from ros_gz_sim package to spawn the bot in evironment. The bot name can be set as anything.
        
        create_entity = Node(package='ros_gz_sim', executable='create',
                             arguments=['-topic', 'robot_description',
                                        '-name', 'my_bot'],
                             output='screen')

        # Launching all of them

        return LaunchDescription([
                rsp,
                gazebo,
                gz_bridge,
                create_entity,
        ])