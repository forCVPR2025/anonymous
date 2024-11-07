#pragma once
#include <../../libraries/myLibs/PIDmethod.h>
#include <Eigen/Eigen>
#include "user_public.h"
#include <../../libraries/myLibs/SecondButterworthLPF.h>

#define Kpitch 4
#define Ipitch 0.02
#define Dpitch -0.001
#define Ipitchmax 0.1
#define Kyaw 4
#define Iyaw 0.02
#define Dyaw -0.001
#define Iyawmax 0.1
#define Kroll 2
#define Iroll 0.02
#define Droll -0.0005
#define Irollmax 0.1

class GimbalControl{
public:
    GimbalControl(double _timeStep);
    ~GimbalControl();
    void stateCb(usrPublic::Odometry state, usrPublic::vector3 gimbal_state);// 更新基本状态
    void cmdCb(usrPublic::vector3 msg);// 进行控制解算，得到输出
    void updateConstrain(double* p);
    usrPublic::Joy gbl2ctrl = {};
    double theta[3] = {0};
private:
    PIDmethod gimbalPid[3];//顺序x-y-z
    SecondOrderButterworthLPF tarF[3];
    Eigen::Matrix3d rotation;// 此旋转矩阵表示为云台末端镜头的旋转矩阵
    Eigen::AngleAxisd rotation_comp;// 由机体倾斜带来的旋转由此矩阵进行补偿
    void GimbalIk();//此处默认已经更新了参数
    Eigen::MatrixXd angle_constrain = Eigen::MatrixXd::Identity(3, 2);
};

/**
 * @description: 构造函数
 * @param {double} _timeStep
 * @return {*}
 */
GimbalControl::GimbalControl(double _timeStep){
    for(int i = 0; i<3; i++){
        gimbalPid[i].PID_Init(Common,_timeStep);
        tarF[i].init(20, 1./_timeStep);
    }
    gimbalPid[0].Params_Config(Kroll,Iroll,Droll,Irollmax,1,-1);
    gimbalPid[1].Params_Config(Kpitch,Ipitch,Dpitch,Ipitchmax,1,-1);
    gimbalPid[2].Params_Config(Kyaw,Iyaw,Dyaw,Iyawmax,1,-1);
    
    // 设置旋转矩阵（这里示意旋转矩阵为单位阵）
    rotation = Eigen::Matrix3d::Identity();

    // 设置三轴角度限幅
    angle_constrain(0, 0) = -1.7;
    angle_constrain(0, 1) = 1.7;
    angle_constrain(1, 0) = -0.5;
    angle_constrain(1, 1) = 1.5;
    angle_constrain(2, 0) = -1.7;
    angle_constrain(2, 1) = 1.7;

}

/**
 * @description: 更新云台转角限制
 * @param: {double*} p
 * @return: {*}
 */
void GimbalControl::updateConstrain(double* p){
    angle_constrain(0, 0) = p[0];
    angle_constrain(0, 1) = p[1];
    angle_constrain(1, 0) = p[2];
    angle_constrain(1, 1) = p[3];
    angle_constrain(2, 0) = p[4];
    angle_constrain(2, 1) = p[5];
}

// 析构函数
GimbalControl::~GimbalControl() {}

/**
 * @description: 状态更新函数，计算了补偿机体倾斜的自稳旋转矩阵
 * @param {Odometry} state
 * @param {vector3} gimbal_state
 * @return {*}
 */
void GimbalControl::stateCb(usrPublic::Odometry state, usrPublic::vector3 gimbal_state){
    gimbalPid[0].current = gimbal_state.x;
    gimbalPid[1].current = gimbal_state.y;
    gimbalPid[2].current = gimbal_state.z;

    // 获取机体的状态并且计算反向旋转矩阵
    Eigen::AngleAxisd rotation_Ix(-state.angle.x, Eigen::Vector3d::UnitX());
    Eigen::AngleAxisd rotation_Iy(-state.angle.y, Eigen::Vector3d::UnitY());
    rotation_comp = rotation_Ix * rotation_Iy;
}

/**
 * @description: 控制函数，计算自稳旋转矩阵，对目标姿态进行逆运动学解算，控制量输出
 * @param {vector3} msg
 * @return {*}
 */
void GimbalControl::cmdCb(usrPublic::vector3 msg){
    // 根据目标旋转结合补偿矩阵求小三轴逆解，并且Pid控制
    Eigen::AngleAxisd rotation_z(msg.z, Eigen::Vector3d::UnitZ());
    Eigen::AngleAxisd rotation_y(msg.y, Eigen::Vector3d::UnitY());
    Eigen::AngleAxisd rotation_x(msg.x, Eigen::Vector3d::UnitX());
    rotation = (rotation_comp * rotation_z * rotation_y * rotation_x).toRotationMatrix();

    GimbalIk();

    for(int i = 0; i<3; i++){
        gimbalPid[i].target = tarF[i].f(upper::constrain(theta[i],angle_constrain(i,0),angle_constrain(i,1)));
        // std::cout<<i<<"  "<<gimbalPid[i].target<<std::endl;
        gbl2ctrl.axes[i] = gimbalPid[i].Adjust(0);
        gbl2ctrl.axes[i+3] = gimbalPid[i].target;
    }
}

/**
 * @description: 以z-y-x为顺序的小三轴逆解
 * @return {*}
 */
void GimbalControl::GimbalIk(){
    double r31 = rotation(2,0);
    double r32 = rotation(2,1);
    double r33 = rotation(2,2);
    double r21 = rotation(1,0);
    double r11 = rotation(0,0);
    theta[1] = atan2(-r31,sqrt(pow(r32,2)+pow(r33,2)));
    upper::constrain(theta[1],angle_constrain(1,0),angle_constrain(1,1));
    theta[2] = atan2(r21/cos(theta[1]),r11/cos(theta[1]));
    upper::constrain(theta[2],angle_constrain(2,0),angle_constrain(2,1));
    theta[0] = atan2(r32/cos(theta[1]),r33/cos(theta[1]));
    upper::constrain(theta[0],angle_constrain(0,0),angle_constrain(0,1));
    // std::cout<<theta[0]<<"  "<<theta[1]<<"  "<<theta[2]<<std::endl;
}

