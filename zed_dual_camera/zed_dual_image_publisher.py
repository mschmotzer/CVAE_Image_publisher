#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

import pyzed.sl as sl
import cv2
import sys


class ZedDualImagePublisher(Node):

    def __init__(self):
        super().__init__('zed_dual_image_publisher')

        self.pub1 = self.create_publisher(Image, '/zed_cam1/image_raw', 10)
        self.pub2 = self.create_publisher(Image, '/zed_cam2/image_raw', 10)

        self.bridge = CvBridge()

        # ---- Detect cameras ----
        devices = sl.Camera.get_device_list()
        if len(devices) != 2:
            self.get_logger().error(
                f'Expected 2 ZED cameras, found {len(devices)}'
            )
            sys.exit(1)
	
        self.cam1 = self.open_zed(13829658)
        self.cam2 = self.open_zed(33137761)

        self.runtime = sl.RuntimeParameters()
        self.mat = sl.Mat()

        self.timer = self.create_timer(1.0 / 30.0, self.timer_callback)
        self.get_logger().info('ZED dual image publisher started')

    def open_zed(self, serial_number):
        init = sl.InitParameters()
        init.camera_resolution = sl.RESOLUTION.VGA
        init.camera_fps = 50
        init.set_from_serial_number(serial_number)

        cam = sl.Camera()
        status = cam.open(init)
        if status != sl.ERROR_CODE.SUCCESS:
            self.get_logger().error(
                f'Failed to open ZED {serial_number}: {status}'
            )
            sys.exit(1)

        return cam

    def grab_image(self, cam):
        if cam.grab(self.runtime) != sl.ERROR_CODE.SUCCESS:
            return None
        cam.retrieve_image(self.mat, sl.VIEW.LEFT)
        img = self.mat.get_data()
        h, w = img.shape[:2]
        
        # Resize to height 240
        scale = 240 / h
        new_w = int(w * scale)
        img = cv2.resize(img, (new_w, 240))

        # Center crop width to 320
        start_x = (new_w - 320) // 2
        img = img[:, start_x:start_x + 320]
        img = cv2.resize(img, (320, 240))
        img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)
        return img

    def timer_callback(self):
        img1 = self.grab_image(self.cam1)
        img2 = self.grab_image(self.cam2)

        if img1 is None or img2 is None:
            self.get_logger().warn('Failed to grab one or more images')
            return

        msg1 = self.bridge.cv2_to_imgmsg(img1, encoding='rgb8')
        msg2 = self.bridge.cv2_to_imgmsg(img2, encoding='rgb8')

        msg1.header.stamp = self.get_clock().now().to_msg()
        msg2.header.stamp = msg1.header.stamp

        self.pub1.publish(msg1)
        self.pub2.publish(msg2)

    def destroy_node(self):
        self.cam1.close()
        self.cam2.close()
        super().destroy_node()


def main():
    rclpy.init()
    node = ZedDualImagePublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
