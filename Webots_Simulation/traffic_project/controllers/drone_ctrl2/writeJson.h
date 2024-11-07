#pragma once
#include <iostream>
#include <fstream>
#include <jsoncpp/json/json.h>
#include "user_public.h"
#include <string.h>
using namespace std;

void stateWriteJson(usrPublic::Odometry state)
{
    Json::Value root;
    // 组装json内容
    root["X"] = Json::Value(state.position.x);
    root["Y"] = Json::Value(state.position.y);
    root["Z"] = Json::Value(state.position.z);
    root["Wx"] = Json::Value(state.angular.x);
    root["Wy"] = Json::Value(state.angular.y);
    root["Wz"] = Json::Value(state.angular.z);
    root["Vx"] = Json::Value(state.linear.x);
    root["Vy"] = Json::Value(state.linear.y);
    root["Vz"] = Json::Value(state.linear.z);
    root["orientationW"] = Json::Value(state.orientation.w);
    root["orientationX"] = Json::Value(state.orientation.x);
    root["orientationY"] = Json::Value(state.orientation.y);
    root["orientationZ"] = Json::Value(state.orientation.z);
    root["roll"] = Json::Value(state.angle.x);
    root["pitch"] = Json::Value(state.angle.y);
    root["yaw"] = Json::Value(state.angle.z);
    root["reward"] = Json::Value(state.reward);
    root["done"] = Json::Value(state.done);

    // 将json内容（缩进格式）输出到文件
    Json::StyledWriter writer;
    ofstream os;
    os.open("/home/lu/Git_Project/github/webots_autodriving_drone/traffic_project_bridge/cache/test.json",std::ios::out | std::ios::app);
    os << writer.write(root);
    os.close();
}
