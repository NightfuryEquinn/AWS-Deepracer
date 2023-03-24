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

  # Intial reward
  reward = 20.0

  # Set the minimum speed threshold based your action space
  SPEED_THRESHOLD = 1.0

  # Set the maximum steering threshold
  ABS_STEERING_THRESHOLD = 30.0

  # Total num of steps we want the car to finish the lap, it will vary depends on the track length
  TOTAL_NUM_STEPS = 300.0

  # Calculate 3 markers that are at varying distances away from the center line
  center_marker_close = 0.1 * track_width
  center_marker_avg = 0.25 * track_width
  center_marker_far = 0.5 * track_width

  # Calculate the distance from each border
  distance_from_border = 0.5 * track_width - distance_from_center

  # Penalize if the car goes off track
  if not all_wheels_on_track:
    reward -= 10.0
  # Penalize if the car goes too slow
  elif speed < SPEED_THRESHOLD:
    reward -= 10.0
  # High reward if the car stays on track and goes fast
  else:
    reward += 10.0

  # Give higher reward if the car is closer to center line and vice versa
  if distance_from_center <= center_marker_close:
    reward += 10.0
  elif distance_from_center <= center_marker_avg:
    reward += 5.0
  elif distance_from_center <= center_marker_far:
    reward += 2.5
  # Likely crashed / close to off track
  else:
    reward -= 10.0

  # Reward higher if the car stays inside the track borders
  if distance_from_border >= 0.05:
    reward += 10.0
  # Low reward if too close to the border or goes off the track
  else:
    reward -= 10.0

  # Penalize if car steer too much to prevent zigzag
  if abs_steering > ABS_STEERING_THRESHOLD:
    reward /= 2.0

  # Give additional reward if the car pass every 100 steps faster than expected
  if (steps % 100.0) == 0 and progress > (steps / TOTAL_NUM_STEPS) * 100.0 :
    reward += 20.0

  # Track Segments
  # Abbey / Starting Corner
  if (car_x > 0.7 and car_x < 2.4) and (car_y > 0.2 and car_y < 1.8):
    if not on_left_side and (abs_steering > 15.0) and (speed > SPEED_THRESHOLD):
      reward += 10.0
    else:
      reward -= 10.0

  # Hamilton Straight / Starting Sprint
  if (car_x > 0.5 and car_x < 1.8) and (car_y > 1.8 and car_y < 3.7):
    if not on_left_side and (speed > 1.25):
      reward += 10.0
    else:
      reward -= 10.0

  # Luffield Corner / More than 90-degree Corner
  # Approaching
  if (car_x > 0.5 and car_x < 1.8) and (car_y > 3.7 and car_y < 5.2):
    if not on_left_side and (abs_steering > 22.5) and (speed > SPEED_THRESHOLD):
      reward += 10.0
    else:
      reward -= 10.0
  # Exiting
  if (car_x > 1.8 and car_x < 3.0) and (car_y > 3.7 and car_y < 5.2):
    if not on_left_side and (speed > 1.25):
      reward += 10.0
    else:
      reward -= 10.0

  # Becketts / The S-track
  if (car_x > 3.0 and car_x < 4.8) and (car_y > 2.3 and car_y < 5.2):
    if (distance_from_center <= center_marker_close) and (speed > 1.25):
      reward += 10.0
    else:
      reward -= 10.0

  # Transitioning
  if (car_x > 4.8 and car_x < 5.8) and (car_y > 2.2 and car_y < 3.4):
    if on_left_side and (speed > SPEED_THRESHOLD):
      reward += 10.0
    else:
      reward -= 10.0

  # Vale / Entering U-turn
  if (car_x > 5.8 and car_x < 7.8) and (car_y > 2.0 and car_y < 3.4):
    if on_left_side and (abs_steering > 22.5) and (speed > SPEED_THRESHOLD) and (distance_from_border >= 0.05):
      reward += 12.5
    else:
      reward -= 10.0

  # Club / Exiting U-turn
  if (car_x > 6.2 and car_x < 7.8) and (car_y > 0.3 and car_y < 2.0):
    if not on_left_side and (speed > 1.25) and (distance_from_border >= 0.05):
      reward += 10.0
    else:
      reward -= 10.0

  # Wellington Straight / Sprint to Finish Line
  if (car_x > 2.4 and car_x < 6.2) and (car_y > 0.3 and car_y < 1.8):
    if not on_left_side and (speed > 1.5) and (distance_from_border >= 0.05):
      reward += 10.0
    else:
      reward -= 10.0

  return float(reward)