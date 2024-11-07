# Recurrent PPO

## Reference to Algorithm

[sb3](https://sb3-contrib.readthedocs.io/en/master/modules/ppo_recurrent.html)

[ppo-implementation-details](https://iclr-blog-track.github.io/2022/03/25/ppo-implementation-details/)

## Experimental setup

working directory

```bash
......./UAV_Follow_Env/Alg_Base/rl_a3c_pytorch_benchmark
```

run

```bash
python ./models/Recurrent_PPO/RPPO.py -w 24 -m citystreet-day.wbt -tp 6006
```

help info

```bash
python ./models/Recurrent_PPO/RPPO.py -h
```

### Map: simpleway.wbt

number of agents

```python
workers = 30
```

config.json

```json
{
  "Benchmark":{
    "Need_render":0,
    "Action_dim":7,
    "State_size":84,
    "State_channel":3,
    "Norm_Type":0,
    "Forward_Speed":40,
    "Backward_Speed":-40,
    "Left_Speed":40,
    "Right_Speed":-40,
    "CW_omega":0.2,
    "CCW_omega":-0.2,
    "Control_Frequence":100,
    "port_process":7789,
    "end_reward":false,
    "end_reward_list":[-20,20],
    "scene":"farmland",
    "weather":"day",
    "auto_start":false,
    "Other_State":false,
    "CloudPoint":false,
    "RewardParams":true,
    "RewardType":"default"
  },
  "LunarLander":{
    "Need_render":1,
    "Action_dim":4,
    "State_size":84,
    "State_channel":3,
    "Norm_Type":0
  }
}
```

env_config.json
```json
{
        "Simulation_Mode": "train",
        "Drone_Supervisor_Ctrl": true,
        "Socket_Ip": "127.0.0.1",
        "Config_Agen_Num_Port":7789,
        "Train_Total_Steps": 1500,
        "Init_No_Done_Steps": 100,
        "No_Reward_Done_Steps": 100,
        "Control_Frequence": 100,
        "Customized_Rewards": true,
        "Lidar_Enable": false,
        "Tracking_Object": "SUMO_VEHICLE",
        "Done_Range": {
                "max_height": 50,
                "min_height": 2,
                "velocity": 10000,
                "omiga": 6.283,
                "roll": 1.22,
                "pitch": 1.22,
                "distance_error": 50
        },
        "Reward_Config": {
                "reward_mode": "continuous",
                "distance_scale": 0.01,
                "reward_range": 7
        },
        "Sumo_Params": {
                "max_sumo_car": 40,
                "car_import_interval": 50.0,
                "car_type": "passenger",
                "fixed_color": false,
                "normalize_color": [1,0,0],
                "max_car_speed": 15,
                "max_car_accel": 15,
                "max_car_decel": 15,
                "max_rou_distance": 7000,
                "min_rou_distance": 250,
                "route_num": 100000
        },
        "Other_Params": {
                "max_obj_num": 10,
                "obj_import_interval": 0.5,
                "import_group_num": 4,
                "obj_edge_distribution_random": false,
                "obj_edge_distribution_multilateral": false,
                "obj_edge_distribution_fixed": 0,
                "obj_edge_distribution_max":10,
                "obj_edge_distribution_min":-10

        },
        "Out_Video": {
                "channels": 4,
                "fps": 50.0,
                "start_time": 1.0,
                "total_time": 50.0
        },
        "Drone_Random_Config": {
                "start_time_bias_ms": 510,

                "view_pitch_random": true,
                "view_pitch_fixed": 1,
                "view_pitch_random_max": 1,
                "view_pitch_random_min": 0.4,

                "height_random": true,
                "height_fixed": 15.0,
                "height_random_max": 15.0,
                "height_random_min": 10.0,

                "direction_random": true,
                "direction_random_multilateral": false,
                "direction_fixed": 0,
                "direction_random_max": 3.1415926535,
                "direction_random_min": -3.1415926535,

                "horizon_bias_random": true,
                "horizon_bias_multilateral": true,
                "horizon_bias_fixed": 0,
                "horizon_bias_random_max": 3,
                "horizon_bias_random_min": 2,
                
                "verticle_bias_random": true,
                "verticle_bias_multilateral": true,
                "verticle_bias_fixed": 0,
                "verticle_bias_random_max": 3,
                "verticle_bias_random_min": 2
        }
}
```