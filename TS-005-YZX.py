def reward_function(params):
  # Read input parameters
  track_width = params["track_width"]
  distance_from_center = params["distance_from_center"]
  all_wheels_on_track = params["all_wheels_on_track"]
  speed = params["speed"]
  steps = params["steps"]
  progress = params["progress"]
  left = params["is_left_of_center"]
  closest_waypoint = params["closest_waypoints"]
  abs_steering = abs(params["steering_angle"]) 
  is_off_track = params["is_offtrack"]

  # Initial Rewards
  reward = 25.0

  # Variance from center line
  center_variance = distance_from_center / track_width

  # Racing line
  left_lane = [85, 84, 83, 82, 81, 80, 79, 78, 77, 76, 75, 74, 54, 53, 52, 51, 50, 49, 48, 47, 46, 45, 44, 43, 42, 41, 40, 39, 38, 37, 36, 35, 34]
  center_lane = [99, 98, 97, 96, 95, 94, 93, 92, 91, 90, 89, 88, 87, 86, 73, 72, 71, 70, 62, 61, 60, 59, 58, 57, 56, 55, 33, 32, 31, 30]
  right_lane = [111, 110, 109, 108, 107, 106, 105, 104, 103, 102, 101, 100, 69, 68, 67, 66, 65, 64, 63, 29, 28, 27, 26, 25, 24, 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
  
  # Speed while in waypoints
  sprint = [73, 72, 71, 70, 69, 68, 67, 66, 65, 64, 63, 62, 61, 60, 59, 58, 57, 56, 55, 54, 53, 52,51, 50, 49, 48, 47, 46, 45, 26, 25, 24, 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
  fast = [111, 110, 109, 108, 107, 106, 105, 104, 103, 102, 101, 100, 99, 98, 97, 96, 95, 94, 93, 92, 91, 90, 89, 44, 43, 42, 41, 40, 29, 28, 27]
  slow = [88, 87, 86, 85, 84, 83, 82, 81, 80, 79, 78, 77, 76, 75, 74, 39, 38, 37, 36, 35, 34, 33, 32, 31, 30]
  
  # Penalize if wheels off track and off track
  if all_wheels_on_track:
    reward += 5.0
  else:
    reward -= 10.0

  # Fix the best route and train to follow the route
  if closest_waypoint[1] in left_lane and left:
    reward += 10.0
  elif closest_waypoint[1] in right_lane and not left:
    reward += 10.0
  elif closest_waypoint[1] in center_lane and center_variance < 0.4:
    reward += 10.0
  else:
    reward -= 10.0

  # Set the speed 
  if closest_waypoint[1] in sprint:
    if speed == 3:
      reward += 10.0
    else:
      reward -= 10.0
  elif closest_waypoint[1] in fast:
    if speed == 2 :
      reward += 10.0
    else:
      reward -= 10.0
  elif closest_waypoint[1] in slow:
    if speed == 1 :
      reward += 10.0
    else:
      reward -= 10.0

  # Set the steering threshold (Max 20)
  ABS_STEERING_THRESHOLD = 20.0
  # Penalize if car steer too much to prevent zigzag
  if abs_steering > ABS_STEERING_THRESHOLD:
    reward /= 2.0

  # Total num of steps we want the car to finish the lap, it will vary depends on the track length
  TOTAL_NUM_STEPS = 300.0
  # Give additional reward if the car pass every 100 steps faster than expected
  if (steps % 100.0) == 0 and progress > (steps / TOTAL_NUM_STEPS) * 100.0 :
    reward += 20.0
  
  return float(reward)