from kandinsky import set_pixel, color, fill_rect
from math import sin, cos
from time import monotonic
from ion import *

# TODO: add reset button KEY_FIVE

CAN_W = 320
CAN_H = 222
CAN_CEN_X = CAN_W // 2
CAN_CEN_Y = CAN_H // 2

BLACK = color(0, 0, 0)
WHITE = color(255, 255, 255)

VP_W = 2.0
VP_H = VP_W * CAN_H / CAN_W
obj_z = 2
FOCAL_LEN = 1
PROJ_SCALE = (FOCAL_LEN * CAN_W) / VP_W
NEAR = 0.05

ROT_SPEED = 1.0
MOVE_SPEED_Z = 1.0

rot_x = 0
rot_y = 0

sin_x = 0.0
cos_x = 1.0
sin_y = 0.0
cos_y = 1.0

VERTS = (
  (-0.5, -0.5, 0.5),
  (0.5, -0.5, 0.5),
  (0.5, -0.5, -0.5),
  (-0.5, -0.5, -0.5),
  (-0.5, 0.5, 0.5),
  (0.5, 0.5, 0.5),
  (0.5, 0.5, -0.5),
  (-0.5, 0.5, -0.5),
  (-0.25, 0, 0.25),
  (0.25, 0, 0.25),
  (0.25, 0, -0.25),
  (-0.25, 0, -0.25),
)

EDGES = (
  (0, 1),
  (1, 2),
  (2, 3),
  (3, 0),
  (4, 5),
  (5, 6),
  (6, 7),
  (7, 4),
  (8, 9),
  (9, 10),
  (10, 11),
  (11, 8),
  (0, 8),
  (1, 9),
  (2, 10),
  (3, 11),
  (4, 8),
  (5, 9),
  (6, 10),
  (7, 11),
)

cam_verts = [[0, 0, 0] for _ in VERTS]

def draw_line(x0, y0, x1, y1, col):
  x0 = int(x0)
  y0 = int(y0)
  x1 = int(x1)
  y1 = int(y1)
  
  dx = abs(x1 - x0)
  dy = -abs(y1 - y0)
  sx = 1 if x0 < x1 else -1
  sy = 1 if y0 < y1 else -1
  
  err = dx + dy
  while True:
    set_pixel(x0, y0, col)

    if x0 == x1 and y0 == y1:
      break

    e2 = 2 * err
    if e2 >= dy:
      err += dy
      x0 += sx
    if e2 <= dx:
      err += dx
      y0 += sy

def draw():
  for i, p in enumerate(VERTS):
    x, y, z = p
    
    # Rotate around X
    r_xx = x
    r_xy = y * cos_x - z * sin_x
    r_xz = y * sin_x + z * cos_x
    # Rotate around Y
    r_yx = r_xx * cos_y + r_xz * sin_y
    r_yy = r_xy
    r_yz = -r_xx * sin_y + r_xz * cos_y

    cam_verts[i][0] = r_yx
    cam_verts[i][1] = r_yy
    cam_verts[i][2] = r_yz + obj_z

  # Near-plane clipping and drawing
  fill_rect(0, 0, CAN_W, CAN_H, WHITE)
  for a, b in EDGES:
    ax, ay, az = cam_verts[a]
    bx, by, bz = cam_verts[b]

    if az < NEAR and bz < NEAR:
      continue

    if az < NEAR:
      t = (NEAR - az) / (bz - az)
      ax = ax + t * (bx - ax)
      ay = ay + t * (by - ay)
      az = NEAR
      
    elif bz < NEAR:
      t = (NEAR - az) / (bz - az)
      bx = ax + t * (bx - ax)
      by = ay + t * (by - ay)
      bz = NEAR
    
    p_ax = (ax / az) * PROJ_SCALE
    p_ay = (ay / az) * PROJ_SCALE
    p_bx = (bx / bz) * PROJ_SCALE
    p_by = (by / bz) * PROJ_SCALE
  
    c_ax = p_ax + CAN_CEN_X
    c_ay = CAN_CEN_Y - p_ay
    c_bx = p_bx + CAN_CEN_X
    c_by = CAN_CEN_Y - p_by

    draw_line(c_ax, c_ay, c_bx, c_by, BLACK)

def update(dt):
  global rot_x, rot_y, sin_x, cos_x, sin_y, cos_y, obj_z

  rot_dir_x = keydown(KEY_TWO) - keydown(KEY_EIGHT)
  rot_dir_y = keydown(KEY_SIX) - keydown(KEY_FOUR)
  move_dir_z = keydown(KEY_SEVEN) - keydown(KEY_NINE)

  updated = False

  if rot_dir_x != 0:
    rot_x += rot_dir_x * dt * ROT_SPEED
    sin_x = sin(rot_x)
    cos_x = cos(rot_x)
    updated = True

  if rot_dir_y != 0:
    rot_y += rot_dir_y * dt * ROT_SPEED
    sin_y = sin(rot_y)
    cos_y = cos(rot_y)
    updated = True

  if move_dir_z != 0:
    obj_z += move_dir_z * dt * MOVE_SPEED_Z
    updated = True

  return updated

def main():
  draw()
  prev_start = monotonic()
  
  while True:
    start = monotonic()
    dt = start - prev_start
    prev_start = start
    
    if update(dt):
      draw()

main()