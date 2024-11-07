# README

```json
{
        "Simulation_Mode": "video",		
    	// Simulation environment mode, including "video", "train", "demo".
    	// video: Drones automatically track vehicles and save video images.
    	// train: Single-step training mode.
    	// demo: Use the keyboard to control the drone for observing REWARD parameters, maps.
        "Drone_Supervisor_Ctrl": true,  
    	// Controlling the drone with a supervisor is equivalent to a controller without latency.
        "Config_Agen_Num_Port":7789,	
    	// Udp port number to receive the set number of intelligences in the initialization.
        "Train_Total_Steps": 500,		
    	// Total steps for each episode.
        "Init_No_Done_Steps": 100,		
    	// No DONE steps at the beginning of the training process.
        "No_Reward_Done_Steps": 100,	
    	// The number of consecutive steps without valid rewards generates a DONE.
        "Control_Frequence": 50,		
    	// Control frequency of the control algorithm.(simulation time)
        "Customized_Rewards": true,		
    	// If the customization parameter is enabled, the data used to calculate the reward is sent.
        "Lidar_Enable": false,			
    	// Whether to enable radar data.
        "Done_Range": {					
        // Drones create physical boundaries of DONE because of various factors.
                "max_height": 50,		
                "min_height": 2,
            	// Height range.(m)
                "velocity": 60,		    
            	// Velocity.(m/s)
                "omiga": 6.283,			
            	// Rotational angular speed.(rad/s)
                "roll": 1.22,			
            	// Pose angle.(rad)
                "pitch": 1.22,
                "distance_error": 50	
            	// The error between the desired position and the current position.(m)
        },
        "Reward_Config": {				
        // The tuning parameter for the default REWARD.
                "reward_mode": "discrete",	
            	// discrete: binarizing 0 and 1; continuous: A continuous parameter between [0, 1].
                "distance_scale": 0.01,	
            	// Reward's decay rate (decay nonlinearity).
                "reward_range": 7		
            	// The maximum range(m)
        },
    	"Tracking_Object": "SUMO_VEHICLE",
    	// Defines which object to track. "SUMO_VEHICLE" refers to automobile vehiles controlled by sumo. Other example objects include "Pedestrian", "Shrimp", "Create", "Sojourner", "Mantis". What's more, customized objects are supported, which can be referenced in the user manual.
        "Sumo_Random_Mode": 2,			
    	// The sumo line has a randomization mode that allows you to choose 1 or 2, with 2 being more recommended.
        "Sumo_Params": {
        // Adjust the parameters of "SUMO_VEHICLE" random initialization.
                "max_sumo_car": 20,
            	// Maximum vehecles imported into the world.
                "car_import_interval": 60.0,
            	// The time interval between each batch of vehicles entering the map.(s)
                "car_type": "private",
            	// The type of vehicle to be tracked, including "passenger", "bus", "truck", "trailer", "motorcycle"
                "fixed_color": true,
            	// If true, then use color below. If false, random color.(motorcycle is always random color)
                "normalize_color": [1,0,0],
                "max_car_speed": 15,
            	// (m/s)
                "max_car_accel": 5,
                "max_car_decel": 5,
            	// (m/s^2)
                "max_rou_distance": 3000,
            	// The route distance is between [min, max]. If the gap between min and max is too small, the routes might not be generated.
                "min_rou_distance": 200,
                "route_num": 30000
        },
    	"Other_Params": {
        // Adjust the parameters except "SUMO_VEHICLE" random initialization.
                "max_obj_num": 10,
            	// Maximum objects imported into the world.
                "obj_import_interval": 0.5,
            	// The time interval between each batch of objects entering the map.(s)
                "import_group_num": 4,
            	// The number of objects in a batch, which is realted to the number of agents expected to be trained.
                "obj_edge_distribution_random": false,
            	// Whether objects should be randomly distrubuted perpendicular to the roads. If false, use the fixed value below. If true, random between min and max.
                "obj_edge_distribution_multilateral": false,
            	// If true, the random form becomes to [min, max]∪[-max,-min].
                "obj_edge_distribution_fixed": 0,
                "obj_edge_distribution_max":10,
                "obj_edge_distribution_min":-10
        },
        "Socket_Ip": "127.0.0.1",
    	// Ip for udp communication.
        "Out_Video": {
        // Parameters in video mode.
                "channels": 4,
            	// Number of video channels, i.e. how many drones.
                "fps": 50.0,
                "start_time": 1.0,
                "total_time": 50.0
            	// Simulation time.(s)
        },
        "Drone_Random_Config": {
        // Random configs for drone.
                "start_time_bias_ms": 310,
				// Initialization bias time, the longer the time, the more stable the scene is with more vehicles.(ms)
                "view_pitch_random": true,
            	// Drone camera pitch angle.(rad)
            	// If false, then use fixed value below. If true, random between min and max.
                "view_pitch_fixed": 1,
                "view_pitch_random_max": 1.57,
                "view_pitch_random_min": 0.7,

                "height_random": false,
            	// Drone height.(m)
            	// If false, then use fixed value below. If true, random between min and max.
                "height_fixed": 15.0,
                "height_random_max": 20.0,
                "height_random_min": 13.0,

                "direction_random": false,
            	// Drone follow direction.(rad)
            	// If false, then use fixed value below. If true, random between min and max.
                "direction_fixed": 1,
                "direction_random_max": 0.1,
                "direction_random_min": -0.1,

                "horizon_bias_random": true,
            	// Initial drone follow bias.(m)
            	// If false, then use fixed value below. If true, random between min and max.
                "horizon_bias_multilateral": true,
            	// If true, the random form becomes to [min, max]∪[-max,-min].
                "horizon_bias_fixed": 0,
                "horizon_bias_random_max": 3,
                "horizon_bias_random_min": 2,
                
                "verticle_bias_random": true,
            	// Initial drone follow bias.(m)
            	// If false, then use fixed value below. If true, random between min and max.
                "verticle_bias_multilateral": true,
            	// If true, the random form becomes to [min, max]∪[-max,-min].
                "verticle_bias_fixed": 0,
                "verticle_bias_random_max": 3,
                "verticle_bias_random_min": 2
        }
}
```

