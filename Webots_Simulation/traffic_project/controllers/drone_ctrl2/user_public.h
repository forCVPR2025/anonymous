#pragma once
#include <iostream>
#include <stdint.h>


namespace usrPublic{
    #pragma pack(1)
    typedef struct _vector3{
        double x;
        double y;
        double z;
    }vector3;
    #pragma pack()

    #pragma pack(1)
    typedef struct _vector4{
        double w;
        double x;
        double y;
        double z;
    }vector4;
    #pragma pack()

    // sensor data and reward and done ---- double * 22
    #pragma pack(1)
    typedef struct _Odometry{
        double t;
        vector3 position;//三轴位置m
        vector3 linear;//三轴线速度m/s
        vector3 acc;//三轴加速度m/s^2
        vector3 angular;//三轴角速度rad
        vector4 orientation;//四元数
        vector3 angle;//欧拉角
        double reward;//reward
        double done;//是否结束仿真
    }Odometry;
    #pragma pack()

    // make reward data ---- double * 60 + string
    #pragma pack(1)
    typedef struct _rewardData{
        double cameraWidth;// 图像宽度（像素）
        double cameraHeight;// 图像高度（像素）
        double cameraFov;// 摄像头视场角 （rad）
        double cameraF;// 摄像头焦距估算（像素）
        double cameraPitch;// 摄像头俯仰角 (rad)
        double trackerHeight;// 跟踪器高度 (m) 
        double initDirection;// 初始跟踪角度 (rad)
        double T_ct[16];// 摄像头相对于世界坐标系的齐次变换矩阵
        // vector3 BMW;// 车辆的长宽高
        // vector3 Citroen;
        // vector3 Lincoln;
        // vector3 Benz;
        // vector3 Rover;
        // vector3 Tesla;
        // vector3 Toyota;
        double T_tw[16];// 车辆相对于世界坐标系的齐次变换矩阵
        vector3 cameraMidGlobalPos;// 摄像头中心映射到地面在世界坐标系下的三维坐标
        vector3 carMidGlobalPos;// 车辆中心在世界坐标系下的三维坐标
        vector3 cameraMidPos; // 摄像头中心世界坐标系的坐标
        vector4 carDronePosOri; // 车辆中心在无人机坐标系下的3D坐标和1D姿态
        vector3 carDroneVel; // 车辆中心在无人机坐标系下的3D速度
        vector3 carDroneAcc; // 车辆中心在无人机坐标系下的3D加速度
        double crash; // 无人机是否与建筑物碰撞
        double carDir;// 车辆运行方向(0停止，1前进，2左转，3右转)
        std::string carTypename = std::string("BmwX5Simple");// 对象类型
    }rewardData;
    #pragma pack()

    #pragma pack(1)
    typedef struct _Pose{
        vector4 orientation;
        vector3 position;
    }Pose;
    #pragma pack()

    #pragma pack(1)
    typedef struct _Joy{
        double axes[10];
    }Joy;
    #pragma pack()
}
