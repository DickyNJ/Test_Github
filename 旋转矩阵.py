import math

import numpy as np
from scipy.spatial.transform import Rotation
import math

def rotation_matrix_to_quaternion(matrix):
    tr = matrix[0][0] + matrix[1][1] + matrix[2][2]
    if tr > 0:
        S = math.sqrt(tr + 1.0) * 2.0
        w = 0.25 * S
        x = (matrix[2][1] - matrix[1][2]) / S
        y = (matrix[0][2] - matrix[2][0]) / S
        z = (matrix[1][0] - matrix[0][1]) / S
    elif matrix[0][0] > matrix[1][1] and matrix[0][0] > matrix[2][2]:
        S = math.sqrt(1.0 + matrix[0][0] - matrix[1][1] - matrix[2][2]) * 2.0
        w = (matrix[2][1] - matrix[1][2]) / S
        x = 0.25 * S
        y = (matrix[0][1] + matrix[1][0]) / S
        z = (matrix[0][2] + matrix[2][0]) / S
    elif matrix[1][1] > matrix[2][2]:
        S = math.sqrt(1.0 + matrix[1][1] - matrix[0][0] - matrix[2][2]) * 2.0
        w = (matrix[0][2] - matrix[2][0]) / S
        x = (matrix[0][1] + matrix[1][0]) / S
        y = 0.25 * S
        z = (matrix[1][2] + matrix[2][1]) / S
    else:
        S = math.sqrt(1.0 + matrix[2][2] - matrix[0][0] - matrix[1][1]) * 2.0
        w = (matrix[1][0] - matrix[0][1]) / S
        x = (matrix[0][2] + matrix[2][0]) / S
        y = (matrix[1][2] + matrix[2][1]) / S
        z = 0.25 * S

        x = round(x, 8)
        y = round(y, 8)
        z = round(z, 8)
        w = round(w, 8)
    return np.array([x, y, z, w])


# 示例使用
rotation_matrix = [[0.866, -0.5, 0],
                   [0.5, 0.866, 0],
                   [0, 0, 1]]

quaternion = rotation_matrix_to_quaternion(rotation_matrix)
print("四元数表示:", quaternion)


def caculate_angle(x, y) -> float :
    # 使用math.atan2()计算角度（弧度）
    angle_radians = math.atan2(y, x)

    # 将弧度转换为度数
    angle_degrees = -math.degrees(angle_radians)

    print("角度（以度数表示),",angle_degrees)
    return angle_degrees
angle_yaw = caculate_angle(0.2941,0.2466)

R = [[math.cos(angle_yaw), -math.sin(angle_yaw), 0],
     [math.sin(angle_yaw), math.cos(angle_yaw), 0],
     [0, 0, 1]]

rotation = Rotation.from_matrix(R)
quaternion1 = rotation_matrix_to_quaternion(R)
quaternion = rotation.as_quat()

# 现在你有了表示旋转的四元数
print("四元数表示：", quaternion)
print("四元数表示：", quaternion1)