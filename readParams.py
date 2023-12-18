import numpy as np
import open3d as o3d
from scipy.spatial.transform import Rotation

import cv2
import csv
import re
import os

def read_ext_parameters(image_file):
    camera_infos = []
    rotation_matrices = []
    translation_vectors = []
    with open(image_file, 'r') as f:
        lines = f.readlines()

    for i in range(0, len(lines), 2):
        quaternion_line = lines[i].strip()
        
        if i<4:
            continue

        # 提取四元数值
        quaternion_values = re.findall(r"[-+]?\d*\.\d+|[-+]?\d+", quaternion_line)
        qw, qx, qy, qz = quaternion_values[1], quaternion_values[2], quaternion_values[3], quaternion_values[4]
        # 提取平移向量值
        tx, ty, tz = quaternion_values[5], quaternion_values[6], quaternion_values[7]
        
        qw, qx, qy, qz, tx, ty, tz = map(float, [qw, qx, qy, qz, tx, ty, tz])
        
        # 构建相机转换信息字典
        pose = {
            'quaternion': [qw, qx, qy, qz],
            'translation': [tx, ty, tz]
        }
        camera_infos.append(pose)

        # Create the rotation matrix from quaternion
        rotation_matrix = Rotation.from_quat([qx, qy, qz, qw]).as_matrix()

        # Create the translation vector
        translation_vector = np.array([tx, ty, tz])

        rotation_matrices.append(rotation_matrix) 
        translation_vectors.append(translation_vector)
    return camera_infos, rotation_matrices, translation_vectors



def read_inner_parameters(camera_file_path):
    with open(camera_file_path, 'r') as f:
        lines = f.readlines()

    num_cameras = int(lines[2].split()[-1])

    camera_matrices = []
    for i in range(num_cameras):
        camera_line = lines[3 + i].split()
        camera_params = [float(param) for param in camera_line[4:]]
        print(camera_line)
        fx = camera_params[0]
        fy = camera_params[1]
        cx = camera_params[2]
        cy = camera_params[3]

        camera_matrix = np.array([[fx, 0, cx], [0, fy, cy], [0, 0, 1]])
        camera_matrices.append(camera_matrix)

    return camera_matrices


image_file = '.\\images.txt'
camera_file = '.\\cameras.txt'

# 相机外参
camera_info, rotation_matrices, translation_vectors = read_ext_parameters(image_file)
# 相机内参
intrinsic_matrix = read_inner_parameters(camera_file)

print(len(camera_info), intrinsic_matrix)