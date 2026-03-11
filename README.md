# CVAE_Image_publisher

# zed_dual_camera

ROS 2 package for publishing synchronized streams from two ZED cameras.

---

## Prerequisites

- [ZED SDK](https://www.stereolabs.com/developers/release) installed
- Two ZED cameras connected
- Camera IDs must match the values defined in `zed_dual_image_publisher.py`

---

## Installation

Clone the repository into your workspace:
```bash
cd ~/franka_ros2_ws/src
git clone <repo-url>
```

---

## Build
```bash
cd ~/franka_ros2_ws
colcon build --packages-select zed_dual_camera --cmake-args -DCMAKE_BUILD_TYPE=Release
```

---

## Source
```bash
source ~/franka_ros2_ws/install/setup.bash
```

---

## Run
```bash
cd ~/franka_ros2_ws
ros2 run zed_dual_camera dual_zed_publisher
```

---

## Notes

> ⚠️ The camera serial IDs in `zed_dual_image_publisher.py` must match the IDs of your physically connected cameras. Update the file if needed before running.
