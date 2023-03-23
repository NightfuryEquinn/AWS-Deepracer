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
  is_offtrack = params["is_offtrack"]

  # Initial Rewards
  reward = 20.0

  # Variance from center line
  center_variance = distance_from_center / track_width

  # Racing line
  left_lane = [27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71]
  center_lane = [13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 72, 73, 74, 75]
  right_lane = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111]
  
  # Speed while in waypoints
  sprint = [40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111]
  fast = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 69, 70, 71, 72, 73, 85, 86, 87]
  slow = [24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84]
  
  # Penalize if wheels off track
  if all_wheels_on_track:
    reward += 10.0
  else:
    reward -= 10.0

  # Penlize if car off track
  if not is_offtrack:
    reward += 10.0
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