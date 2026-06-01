from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.conditions import IfCondition, UnlessCondition
from launch.substitutions import Command, FindExecutable, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


COMPONENT_TYPES = {
    "galbot_gripper",
    "head",
    "hitbot_gripper",
    "left_arm",
    "leg",
    "omniwheel",
    "omni_chassis",
    "right_arm",
    "suction_cup",
    "torso",
    "wrist_camera",
}


def launch_setup(context, *args, **kwargs):
    package_share = FindPackageShare("galbot_one_golf_description")
    rviz_config = PathJoinSubstitution([package_share, "config", "rviz", "model.rviz"])

    model_type = LaunchConfiguration("type").perform(context)
    use_gui = LaunchConfiguration("gui")
    ee_type = LaunchConfiguration("ee_type")
    left_ee_type = LaunchConfiguration("left_ee_type")
    right_ee_type = LaunchConfiguration("right_ee_type")
    arm_camera = LaunchConfiguration("arm_camera")
    collision_type = LaunchConfiguration("collision_type")
    enable_wheel_joints = LaunchConfiguration("enable_wheel_joints")
    enable_joint5 = LaunchConfiguration("enable_joint5")

    if model_type == "full":
        model_path = PathJoinSubstitution([package_share, "xacro", "robot.xacro"])
        xacro_command = [
            FindExecutable(name="xacro"),
            " ",
            model_path,
            " type:=",
            ee_type,
            " left_ee_type:=",
            left_ee_type,
            " right_ee_type:=",
            right_ee_type,
            " arm_camera:=",
            arm_camera,
            " collider:=",
            collision_type,
            " enable_wheel_joints:=",
            enable_wheel_joints,
            " enable_joint5:=",
            enable_joint5,
        ]
    elif model_type in COMPONENT_TYPES:
        model_path = PathJoinSubstitution([package_share, "xacro", "component.xacro"])
        xacro_command = [
            FindExecutable(name="xacro"),
            " ",
            model_path,
            " type:=",
            model_type,
            " arm_camera:=",
            arm_camera,
            " collision_type:=",
            collision_type,
            " enable_wheel_joints:=",
            enable_wheel_joints,
            " enable_joint5:=",
            enable_joint5,
        ]
    else:
        valid_types = ", ".join(["full"] + sorted(COMPONENT_TYPES))
        raise RuntimeError(f"Invalid type: {model_type}. Valid values: {valid_types}")

    robot_description = {
        "robot_description": Command(xacro_command)
    }

    return [
        Node(
            package="robot_state_publisher",
            executable="robot_state_publisher",
            parameters=[robot_description],
            output="screen",
        ),
        Node(
            package="joint_state_publisher_gui",
            executable="joint_state_publisher_gui",
            condition=IfCondition(use_gui),
            output="screen",
        ),
        Node(
            package="joint_state_publisher",
            executable="joint_state_publisher",
            condition=UnlessCondition(use_gui),
            output="screen",
        ),
        Node(
            package="rviz2",
            executable="rviz2",
            arguments=["-d", rviz_config],
            output="screen",
        ),
    ]


def generate_launch_description():
    ee_type = LaunchConfiguration("ee_type")

    return LaunchDescription([
        DeclareLaunchArgument(
            "gui",
            default_value="true",
            description="Use joint_state_publisher_gui when true.",
        ),
        DeclareLaunchArgument(
            "type",
            default_value="full",
            description="Model to display: full, omni_chassis, omniwheel, leg, torso, head, left_arm, right_arm, galbot_gripper, hitbot_gripper, suction_cup, or wrist_camera.",
        ),
        DeclareLaunchArgument(
            "ee_type",
            default_value="galbot_gripper",
            description="Default end effector type for both arms: galbot_gripper, hitbot, suction_cup, or none.",
        ),
        DeclareLaunchArgument(
            "left_ee_type",
            default_value=ee_type,
            description="Left arm end effector type. Defaults to ee_type.",
        ),
        DeclareLaunchArgument(
            "right_ee_type",
            default_value=ee_type,
            description="Right arm end effector type. Defaults to ee_type.",
        ),
        DeclareLaunchArgument(
            "arm_camera",
            default_value="d405",
            description="Wrist camera type for full, left_arm, and right_arm: d405, d415, or none.",
        ),
        DeclareLaunchArgument(
            "collision_type",
            default_value="simple",
            description="Collision geometry type passed to component xacro files.",
        ),
        DeclareLaunchArgument(
            "enable_wheel_joints",
            default_value="false",
            description="Use continuous omni chassis wheel joints when true.",
        ),
        DeclareLaunchArgument(
            "enable_joint5",
            default_value="true",
            description="Include leg_joint5 when true.",
        ),
        OpaqueFunction(function=launch_setup),
    ])
