#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2016 Massachusetts Institute of Technology

"""Extract images from a ROS bag file.

Requires:
cv2
> conda install -c conda-forge opencv
rosbag
> conda install -c conda-forge ros-rosbag
sensor_msgs
> conda install -c conda-forge ros-sensor-msgs
cv_bridge
> conda install -c conda-forge ros-cv-bridge

To summarize the contents of a .bag file, in the command line try:
rosbag info <bagfile>

"""

import os
import argparse

import cv2

import rosbag
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

def main():
    """Extract a folder of images from a rosbag.
    """
    
    parser = argparse.ArgumentParser(description="Extract images from a ROS bag file.")
    parser.add_argument('-b',
                        '--bag_file',
                        type = str,
                        default = 'experiment3.bag',
                        help="Input ROS bag file name.")
    parser.add_argument('-o',
                        '--output_dir',
                        type = str,
                        default = 'extracted_images',
                        help="Output directory name. Make sure the directory already exists!")
    parser.add_argument('-t',
                        '--image_topic',
                        type = str,
                        default = '/device_0/sensor_1/Color_0/image/data',
                        help="Image topic.")

    args = parser.parse_args()

    print("Extract images from {} on topic {} into {}".format(args.bag_file,
                                                              args.image_topic, 
                                                              args.output_dir))

    bag = rosbag.Bag(args.bag_file, "r")
    bridge = CvBridge()
    count = 0
    for topic, msg, t in bag.read_messages(topics=[args.image_topic]):
        cv_img = bridge.imgmsg_to_cv2(msg, desired_encoding="passthrough")

        cv2.imwrite(os.path.join(args.output_dir, "frame%06i.png" % count), cv_img)
        print("Wrote image {}".format(count))

        count += 1

    bag.close()

    return

if __name__ == '__main__':
    main()