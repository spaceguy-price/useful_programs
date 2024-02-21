# Intrinsic matrix extraction function
# original code by Marco Carletti
# found at: https://mcarletti.github.io/articles/blenderintrinsicparams/

# Adapted by Andrew Price
# 21 February 2024
#
# Simple Instructions:
# 1) Launch blender from the command line
# 2) Open the .blend file of interest
# 3) run this script from within blender
# the intrinsic matrix will be printed at the command line 
# and a K.txt file will be created in the current working directory

import bpy
import numpy as np
from datetime import datetime

def get_calibration_matrix_K_from_blender(mode='simple'):

    scene = bpy.context.scene

    scale = scene.render.resolution_percentage / 100
    width = scene.render.resolution_x * scale # px
    height = scene.render.resolution_y * scale # px

    camdata = scene.camera.data

    if mode == 'simple':

        aspect_ratio = width / height
        K = np.zeros((3,3), dtype=np.float32)
        K[0][0] = width / 2 / np.tan(camdata.angle / 2)
        K[1][1] = height / 2. / np.tan(camdata.angle / 2) * aspect_ratio
        K[0][2] = width / 2.
        K[1][2] = height / 2.
        K[2][2] = 1.
        K.transpose()
    
    if mode == 'complete':

        focal = camdata.lens # mm
        sensor_width = camdata.sensor_width # mm
        sensor_height = camdata.sensor_height # mm
        pixel_aspect_ratio = scene.render.pixel_aspect_x / scene.render.pixel_aspect_y

        if (camdata.sensor_fit == 'VERTICAL'):
            # the sensor height is fixed (sensor fit is horizontal), 
            # the sensor width is effectively changed with the pixel aspect ratio
            s_u = width / sensor_width / pixel_aspect_ratio 
            s_v = height / sensor_height
        else: # 'HORIZONTAL' and 'AUTO'
            # the sensor width is fixed (sensor fit is horizontal), 
            # the sensor height is effectively changed with the pixel aspect ratio
            pixel_aspect_ratio = scene.render.pixel_aspect_x / scene.render.pixel_aspect_y
            s_u = width / sensor_width
            s_v = height * pixel_aspect_ratio / sensor_height

        # parameters of intrinsic calibration matrix K
        alpha_u = focal * s_u
        alpha_v = focal * s_v
        u_0 = width / 2
        v_0 = height / 2
        skew = 0 # only use rectangular pixels

        K = np.array([
            [alpha_u,    skew, u_0],
            [      0, alpha_v, v_0],
            [      0,       0,   1]
        ], dtype=np.float32)
    
    return K

if __name__ == "__main__":
    intrinsic = get_calibration_matrix_K_from_blender(mode='simple')
    print(intrinsic)
    #now = datetime.now() 
    #now_str = now.strftime("%Y-%m-%d-%H-%M")
    #np.savetxt('K_'+now_str+'.txt', intrinsic)
    np.savetxt('K.txt', intrinsic)