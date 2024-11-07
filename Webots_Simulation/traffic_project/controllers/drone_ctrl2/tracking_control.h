#pragma once
#include <../../libraries/myLibs/Upper_Public.h>
#include <Eigen/Eigen>
#include "user_public.h"
#include <../../libraries/myLibs/PIDmethod.h>
#include <../../libraries/myLibs/SecondButterworthLPF.h>
#include <Eigen/Dense>

#define BODY2GIMBAL_D 0.13   //机体中心到三轴云台基座中心的距离
#define GIMBAL2CAMERA_D 0.04 //云台基座中心到摄像头中心的距离

class TrackingCtrl
{
public:
    TrackingCtrl(double _timeStep);
    ~TrackingCtrl();
    void stateCb(usrPublic::Odometry state, usrPublic::vector3 gimbal_state);// 需要更新的包括无人机的状态以及云台的状态
    void cmdCb(usrPublic::vector4 msg);// 计算对应输出时需要传入图像中的四维输入量
    usrPublic::vector4 track2joy = {};
private:
    PIDmethod drone_pid[4];// 无人机使用的pid，包括三轴平动以及z轴转动
    Eigen::Transform<double, 3, Eigen::Affine> transform; // 齐次变换矩阵
    Eigen::Matrix3d rotation;
    usrPublic::Odometry state;
    double state_period; // 控制周期
    double linear_speed[3] = {0};
    SecondOrderButterworthLPF tracking_f[4];// 跟踪滤波器

};

/**
 * @description: 构造函数，初始化模块
 * @param {double} _timeStep
 * @return {*}
 */
TrackingCtrl::TrackingCtrl(double _timeStep): state_period(_timeStep) {

    // 设置平移向量
    Eigen::Translation3d translation(BODY2GIMBAL_D, 0, -GIMBAL2CAMERA_D);
    // 设置旋转矩阵（这里示意旋转矩阵为单位阵）
    rotation = Eigen::Matrix3d::Identity();
    // 构建齐次变换阵
    transform = translation * rotation;
    // 初始化PID类型
    for(int i = 0; i < 4 ; i++){
        drone_pid[i].PID_Init(Common, state_period);
        tracking_f[i].init(25,1000 / state_period);
    }
    // drone_pid[0].Params_Config(25, 0.001, 200, 0., 25, -25);//x轴平动控制
    // drone_pid[0].d_of_current = false;
    // drone_pid[1].Params_Config(-15, -0.01, -400, 0., 15, -15);//y轴平动控制
    // drone_pid[1].d_of_current = false;
    drone_pid[0].Params_Config(12, 0.01, -0.025, 2., 12, -12);//x轴平动控制
    drone_pid[1].Params_Config(-12, -0.01, -0.025, 2., 12, -12);//y轴平动控制
    drone_pid[2].Params_Config(0.02, 0, -0.001, 0, 0.01, -0.01);//z轴平动控制
    drone_pid[3].Params_Config(-60.,0.,-4,0,100,-100);//z轴旋转控制
    

}

TrackingCtrl::~TrackingCtrl() {}

/**
 * @description: 更新tracking的状态量，并且得到工作坐标系与基坐标系之间的变换矩阵
 * @param {Odometry} _state
 * @param {vector3} gimbal_state
 * @return {*}
 */
void TrackingCtrl::stateCb(usrPublic::Odometry _state, usrPublic::vector3 gimbal_state){
    usrPublic::Odometry state = _state;
    linear_speed[0] = state.linear.x;
    linear_speed[1] = state.linear.y;
    linear_speed[2] = state.linear.z;
    // 更新齐次变换矩阵（这里定义了从基坐标系到工作坐标系的所有旋转）
    Eigen::Translation3d translation(BODY2GIMBAL_D * cos(state.angle.y) - GIMBAL2CAMERA_D * sin(state.angle.y), 0, -GIMBAL2CAMERA_D * cos(state.angle.y) - BODY2GIMBAL_D * sin(state.angle.y));
    // Eigen::AngleAxisd rotation_bz(state.angle.z, Eigen::Vector3d::UnitZ());
    Eigen::AngleAxisd rotation_by(state.angle.y, Eigen::Vector3d::UnitY());
    Eigen::AngleAxisd rotation_bx(state.angle.x, Eigen::Vector3d::UnitX());
    Eigen::AngleAxisd rotation_z(gimbal_state.z, Eigen::Vector3d::UnitZ());
    Eigen::AngleAxisd rotation_y(gimbal_state.y, Eigen::Vector3d::UnitY());
    Eigen::AngleAxisd rotation_x(gimbal_state.x, Eigen::Vector3d::UnitX());
    rotation = (rotation_by * rotation_bx * rotation_z * rotation_y * rotation_x).toRotationMatrix();
    // rotation = (rotation_z * rotation_y * rotation_x).toRotationMatrix();
    transform = translation * rotation;

}

/**
 * @description: 执行tracking控制指令，包括向量映射，pid执行
 * @param {vector4} msg
 * @return {*}
 */
void TrackingCtrl::cmdCb(usrPublic::vector4 msg){
    Eigen::Vector3d v1_vector(tracking_f[0].f(0), tracking_f[1].f(msg.y), tracking_f[2].f(msg.z + 0.25 * cos(msg.w))); // 工作坐标系下的线速度向量
    // Eigen::Vector3d v1_vector(tracking_f[0].f(0), tracking_f[1].f(msg.y), tracking_f[2].f(msg.z)); // 工作坐标系下的线速度向量
    // std::cout<<"v1: \n"<<v1_vector.matrix()<<std::endl;
    Eigen::Vector3d v0_vector = rotation * v1_vector; // 基坐标系下的线速度向量
    v0_vector(2) = 0;
    // std::cout<<"v2: \n"<<v0_vector.matrix()<<std::endl;

    for(int i = 0; i < 3 ; i++){
        drone_pid[i].target = v0_vector(i);
        drone_pid[i].current = 0;
        // if(i == 0 || i == 1){
        //     drone_pid[i].Adjust(0);
        //     // std::cout<<"error:  "<<drone_pid[0].error<<" "<< "i_term:  "<< drone_pid[0].I_Term<<"  "<<"d_tern: "<<drone_pid[0].D_Term<<std::endl;
        // }
        // else{
            drone_pid[i].Adjust(0, linear_speed[i]);
        // }
    }

    track2joy.x = drone_pid[0].out;
    track2joy.y = drone_pid[1].out;
    track2joy.z = drone_pid[2].out;
    track2joy.w = drone_pid[3].out;
}

