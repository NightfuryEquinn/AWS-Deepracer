import math

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
  heading = params['heading']
  waypoints = params['waypoints']
  closest_waypoints = params['closest_waypoints']

  # Intial reward
  reward = 20.0

  # Set the minimum speed threshold based your action space
  SPEED_THRESHOLD = 1.0

  # Set the maximum steering threshold
  ABS_STEERING_THRESHOLD = 22.5

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
    reward -= 20.0
  else:
    reward += 20.0

  # Penalize if the car goes too slow
  if speed < SPEED_THRESHOLD:
    reward -= 20.0
  else:
    reward += 20.0
  
  # Penalize if the car goes to the left
  if not on_left_side:
    reward -= 20.0
  else:
    reward += 20.0

  # Give higher reward if the car is closer to center line and vice versa
  if distance_from_center <= center_marker_close:
    reward += 10.0
  elif distance_from_center <= center_marker_avg:
    reward += 5.0
  elif distance_from_center <= center_marker_far:
    reward += 2.5
  else:
    reward -= 10.0

  # Penalize if car didn't stay inside the track borders
  if distance_from_border >= 0.04:
    reward += 10.0
  else:
    reward -= 10.0

  # Penalize if car steer too much to prevent zigzag
  if abs_steering > ABS_STEERING_THRESHOLD:
    reward /= 2.0
  
  # Calculate the direction of the center line based on the closest waypoints
  next_point = waypoints[closest_waypoints[1]]
  prev_point = waypoints[closest_waypoints[0]]

  # Calculate the direction in radius, arctan2(dy, dx), the result is (-pi, pi) in radians
  track_direction = math.atan2(next_point[1] - prev_point[1], next_point[0] - prev_point[0])
  # Convert to degree
  track_direction = math.degrees(track_direction)

  # Calculate the difference between the track direction and the heading direction of the car
  direction_diff = abs(track_direction - heading)
  if direction_diff > 180:
    direction_diff = 360 - direction_diff

  # Penalize the reward if the difference is too large
  DIRECTION_THRESHOLD = 8.125
  if direction_diff > DIRECTION_THRESHOLD:
    reward *= 0.5

  # Give additional reward if the car pass every 100 steps faster than expected
  if (steps % 100.0) == 0 and progress > (steps / TOTAL_NUM_STEPS) * 100.0 :
    reward += 30.0

  return float(reward)