
# from receiveSocket import RecvPointCloud
# from receiveSocket import RecvRewardParams

# pc = RecvPointCloud()
# rp = RecvRewardParams()

# import cv2

# import ctypes

# # 定义c_void_p类型
# address_type = ctypes.c_void_p

# # 获取变量的内存地址
# x = 10
# address = address_type(id(x))

# # 将内存地址转为16进制字符串
# address_str = hex(address.value)

# print(address_str)

# # 定义c_int类型
# data_type = ctypes.c_int8

# # 创建指向c_int类型的指针
# data = data_type(10)
# data_pointer = ctypes.POINTER(data_type)(data)

# # 修改内存中的数据
# data_pointer.contents.value = 20

# print(data)
# print(ctypes.cast(id(data), ctypes.py_object).value)

# with open("./test.txt",'rb') as file:
#     byte_list = file.read().decode('utf-8').rstrip().split(',')
#     file.close()
# print(byte_list)

# import os
# img_path = "/home/lu/Git_Project/github/webots_autodriving_drone/traffic_project_bridge/Files2Alg/" + "DRONE0" + "_VideoFrame.jpeg"
# print(os.path.exists(img_path))

# -*- coding: utf-8 -*-
# import logging

# logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s',
#                     level=logging.INFO,
#                     filename='./logs/test.log')

# logging.info('info Level,Normal Actions')

import math

print(float('nan'))
