def reward_function(params):
  # Read input parameters
  track_width = params['track_width']
  distance_from_center = params['distance_from_center']
  all_wheels_on_track = params['all_wheels_on_track']
  speed = params['speed']
  steps = params['steps']
  progress = params['progress']
  abs_steering = abs(params['steering_angle']) 
  on_left_side = params['is_left_of_center']
  car_x = params['x']
  car_y = params['y']

  # Initial reward
  reward = 1e-3

  # Set the minimum speed threshold based your action space
  SPEED_THRESHOLD = 1.0

  # Total num of steps we want the car to finish the lap, it will vary depends on the track length
  TOTAL_NUM_STEPS = 300.0

  # Calculate the distance from each border
  distance_from_border = 0.5 * track_width - distance_from_center

  # Penalize if the car goes off track
  if all_wheels_on_track:
    reward += 20.0
  else:
    reward = 1e-3

  # Penalize if the car goes left
  if not on_left_side:
    reward += 20.0
  else:
    reward = 1e-3

  # Penalize if the car too close to border
  if (distance_from_border >= 0.025):
    reward += 20.0
  else:
    reward = 1e-3

  # Penalize if the car goes too slow
  if speed > SPEED_THRESHOLD:
    reward += 20.0
  else:
    reward = 1e-3

  # Default Steering 
  if abs_steering > 25.0:
    reward -= 40.0

  # Give additional reward if the car pass every 100 steps faster than expected
  if (steps % 100.0) == 0 and progress > (steps / TOTAL_NUM_STEPS) * 100.0 :
    reward += 30.0

  # Track Segments
  # Abbey / Starting Corner
  if (car_x > 0.7 and car_x < 2.4) and (car_y > 0.2 and car_y < 1.8):
    if abs_steering > 15.0:
      reward += 10.0
    else:
      reward -= 10.0

  # Hamilton Straight / Starting Sprint
  if (car_x > 0.3 and car_x < 2.0) and (car_y > 1.8 and car_y < 2.5):
    if abs_steering < 15.0:
      reward += 10.0
    else:
      reward -= 10.0

  # Luffield Corner / More than 90-degree Corner
  # Approaching
  if (car_x > 0.4 and car_x < 1.8) and (car_y > 3.6 and car_y < 5.2):
    if abs_steering > 22.5:
      reward += 10.0
    else:
      reward -= 10.0

  # Exiting
  if (car_x > 1.8 and car_x < 3.0) and (car_y > 3.7 and car_y < 5.2):
    if abs_steering < 15.0:
      reward += 10.0
    else:
      reward -= 10.0

  # Becketts / The S-track
  if (car_x > 3.2 and car_x < 4.8) and (car_y > 2.3 and car_y < 5.1):
    if abs_steering < 15.0:
      reward += 10.0
    else:
      reward -= 10.0

  # Transitioning
  if (car_x > 4.8 and car_x < 5.8) and (car_y > 2.2 and car_y < 3.6):
    if abs_steering < 20.0:
      reward += 12.5
    else:
      reward -= 10.0

  # Vale / Entering U-turn
  if (car_x > 5.8 and car_x < 7.8) and (car_y > 2.0 and car_y < 3.4):
    if abs_steering > 22.5:
      reward += 12.5
    else:
      reward -= 10.0

  # Club / Exiting U-turn
  if (car_x > 6.2 and car_x < 7.8) and (car_y > 0.3 and car_y < 2.0):
    if abs_steering < 17.5:
      reward += 10.0
    else:
      reward -= 10.0

  # Wellington Straight / Sprint to Finish Line
  if (car_x > 2.2 and car_x < 6.1) and (car_y > 0.35 and car_y < 1.6):
    if abs_steering < 10.0:
      reward += 20.0
    else:
      reward -= 20.0

    if speed > 2.0:
      reward += 20.0
    else:
      reward = 1e-3

  return float(reward)