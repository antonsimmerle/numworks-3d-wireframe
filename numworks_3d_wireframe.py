from kandinsky import set_pixel, color, draw_string
from math import sin, cos
from time import sleep, monotonic
from ion import keydown, KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT

CAN_W = 320
CAN_H = 222
CAN_CEN_X = CAN_W // 2
CAN_CEN_Y = CAN_H // 2

BLACK = color(0, 0, 0)
WHITE = color(255, 255, 255)

FRAME_DUR = 1/60

VP_W = 2.0
VP_H = VP_W * CAN_H / CAN_W
CAM_Z = 2
FOCAL_LEN = 1
PROJ_SCALE = (FOCAL_LEN * CAN_W) / VP_W

ROT_SPEED = 1.0

rot_x = 0
rot_y = 0

sx = 0.0
cx = 1.0
sy = 0.0
cy = 1.0

VERTS = [
  (-0.5, -0.5, 0.5),
  (0.5, -0.5, 0.5),
  (0.5, -0.5, -0.5),
  (-0.5, -0.5, -0.5),
  (-0.5, 0.5, 0.5),
  (0.5, 0.5, 0.5),
  (0.5, 0.5, -0.5),
  (-0.5, 0.5, -0.5),
  (-0.2, 0, 0.2),
  (0.2, 0, 0.2),
  (0.2, 0, -0.2),
  (-0.2, 0, -0.2),
]

EDGES = [
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
]

proj_verts = [[0, 0] for _ in VERTS]

def log(msg):
  draw_string(str(msg), 10, 10, BLACK)

def draw_line(x0, y0, x1, y1, col):  
  dx = x1 - x0
  dy = y1 - y0
  x_dir = 1 if dx >= 0 else -1
  y_dir = 1 if dy >= 0 else -1
  dx = abs(dx)
  dy = abs(dy)
  
  if dx > dy:
    prim_x, prim_y, sec_x, sec_y = x_dir, 0, 0, y_dir
  else:
    dx, dy = dy, dx
    prim_x, prim_y, sec_x, sec_y = 0, y_dir, x_dir, 0

  D = 2*dy - dx
  x = x0
  y = y0
  for _ in range(dx + 1):
    set_pixel(x, y, col)
    x += prim_x
    y += prim_y
    
    if D >= 0:
      x += sec_x
      y += sec_y
      D = D + 2*(dy - dx)
    else:
      D = D + 2*dy

def draw_edges(col):
  for a, b in EDGES:
    pa = proj_verts[a]
    pb = proj_verts[b]
    draw_line(pa[0], pa[1], pb[0], pb[1], col)

def draw():
  # TODO: erase lines after calculating new vertices
  draw_edges(WHITE)
  
  for i, p in enumerate(VERTS):
    x, y, z = p
    
    # Rotate around X
    r_xx = x
    r_xy = y * cx - z * sx
    r_xz = y * sx + z * cx
    # Rotate around Y
    r_yx = r_xx * cy + r_xz * sy
    r_yy = r_xy
    r_yz = -r_xx * sy + r_xz * cy

    # Project
    depth = r_yz + CAM_Z
    if depth <= 0:
      continue
    
    proj_x = (r_yx / depth) * PROJ_SCALE
    proj_y = (r_yy / depth) * PROJ_SCALE
    
    p = proj_verts[i]
    p[0] = int(proj_x + CAN_CEN_X)
    p[1] = int(CAN_CEN_Y - proj_y)

  draw_edges(BLACK)

def update(dt):
  global rot_x, rot_y, sx, cx, sy, cy

  rot_dir_x = keydown(KEY_DOWN) - keydown(KEY_UP)
  rot_dir_y = keydown(KEY_RIGHT) - keydown(KEY_LEFT)

  if rot_dir_x == 0 and rot_dir_y == 0:
    return False

  if rot_dir_x != 0:
    rot_x += rot_dir_x * dt * ROT_SPEED
    sx = sin(rot_x)
    cx = cos(rot_x)

  if rot_dir_y != 0:
    rot_y += rot_dir_y * dt * ROT_SPEED
    sy = sin(rot_y)
    cy = cos(rot_y)

  return True

def main():
  draw()
  prev_start = monotonic()
  
  while True:
    start = monotonic()
    dt = start - prev_start
    prev_start = start
    
    if update(dt):
      draw()

    elapsed = monotonic() - start
    remaining = FRAME_DUR - elapsed
    if remaining > 0:
      sleep(remaining)

main()