def reward_function(params):
  # Read input parameters
  track_width = params['track_width']
  distance_from_center = params['distance_from_center']
  all_wheels_on_track = params['all_wheels_on_track']
  speed = params['speed']
  steps = params['steps']
  progress = params['progress']
  is_left_of_center = params['is_left_of_center']
  heading = params['heading']

  # Intial reward
  reward = 20.0

  # Set the speed threshold based your action space
  SPEED_THRESHOLD = 2.0

  # Total num of steps we want the car to finish the lap, it will vary depends on the track length
  TOTAL_NUM_STEPS = 300.0

  # Calculate 3 markers that are at varying distances away from the center line
  marker_1 = 0.1 * track_width
  marker_2 = 0.25 * track_width
  marker_3 = 0.5 * track_width

  # Calculate the distance from each border
  distance_from_border = 0.5 * track_width - distance_from_center

  # Read input variable
  # We don't care whether it is left or right steering
  abs_steering = abs(params['steering_angle']) 

  # Penalize if the car goes off track
  if not all_wheels_on_track:
    reward -= 10.0
  # Penalize if the car goes too slow
  elif speed < SPEED_THRESHOLD:
    reward -= 10.0
  # High reward if the car stays on track and goes fast
  else:
    reward += 12.5

  # Give higher reward if the car is closer to center line and vice versa
  if distance_from_center <= marker_1:
    reward += 12.5
  elif distance_from_center <= marker_2:
    reward += 7.5
  elif distance_from_center <= marker_3:
    reward += 2.5
  # Likely crashed / close to off track
  else:
    reward -= 10.0

  # Reward higher if the car stays inside the track borders
  if distance_from_border >= 0.05:
    reward += 12.5
  # Low reward if too close to the border or goes off the track
  else:
    reward -= 10.0

  # Penalize if car is not on the track and more to left
  if not all_wheels_on_track and is_left_of_center:
    reward -= 10.0
  elif all_wheels_on_track and is_left_of_center:
    reward += 5.0
  elif all_wheels_on_track and not is_left_of_center:
    reward += 7.5

  # Speed run on straight line away from y-axis
  if all_wheels_on_track and is_left_of_center and heading == 180:
    reward += 7.5
  elif all_wheels_on_track and is_left_of_center and heading == 180 and speed == SPEED_THRESHOLD:
    reward += 12.5
  else:
    reward -= 10.0
  
  # Speed run on straight line towards from y-axis
  if all_wheels_on_track and not is_left_of_center and heading == 0:
    reward += 7.5
  elif all_wheels_on_track and not is_left_of_center and heading == 0 and speed == SPEED_THRESHOLD:
    reward += 12.5
  else:
    reward -= 10.0

  U_TURN_SWEEP_CORNER = -45.0
  U_TURN_EXIT_CORNER = -135.0

  # Speed slower on u-turn 
  if all_wheels_on_track and is_left_of_center and heading >= U_TURN_SWEEP_CORNER and speed == 1.0:
    reward += 7.5
  elif all_wheels_on_track and is_left_of_center and heading == U_TURN_SWEEP_CORNER and speed == 1.0:
    reward += 12.5
  else:
    reward -= 10.0

  # Mid transit
  if all_wheels_on_track and distance_from_center <= marker_1 and heading == -90:
    reward += 12.5
  else:
    reward -= 10.0

  # Exiting u-turn
  if all_wheels_on_track and not is_left_of_center and heading >= U_TURN_EXIT_CORNER and speed == 1.5:
    reward += 7.5
  elif all_wheels_on_track and not is_left_of_center and heading == U_TURN_EXIT_CORNER and speed == 1.5:
    reward += 12.5
  else: 
    reward -= 10.0

  # Penalize if car steer too much to prevent zigzag
  ABS_STEERING_THRESHOLD = 22.5
  
  if abs_steering > ABS_STEERING_THRESHOLD:
    reward /= 2.0

  # Give additional reward if the car pass every 100 steps faster than expected
  if (steps % 100.0) == 0 and progress > (steps / TOTAL_NUM_STEPS) * 100.0 :
    reward += 12.5

  return float(reward)