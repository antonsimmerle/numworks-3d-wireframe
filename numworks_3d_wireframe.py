from kandinsky import set_pixel, color, fill_rect
from math import sin, cos
from time import monotonic
from ion import keydown, KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT, KEY_TWO, KEY_FOUR, KEY_SIX, KEY_SEVEN, KEY_EIGHT, KEY_NINE, KEY_FIVE

SCR_W = 320
SCR_H = 222
SCR_CEN_X = SCR_W // 2
SCR_CEN_Y = SCR_H // 2

BLACK = color(0, 0, 0)
WHITE = color(255, 255, 255)

LEFT = 8
RIGHT = 4
BOTTOM = 2
TOP = 1

VP_W = 2.0
FL = 1.0
PROJ_S = FL * SCR_W / VP_W
NEAR = 0.05

ROT_SPEED = 1.0
TRANS_SPEED = 1.0

obj_x = 0.0
obj_y = 0.0
obj_z = 2.0

orient = [
  [1, 0, 0],
  [0, 1, 0],
  [0, 0, 1]
]

VERTS = (
  (-0.5, -0.5, 0.5),
  (0.5, -0.5, 0.5),
  (0.5, -0.5, -0.5),
  (-0.5, -0.5, -0.5),
  (-0.5, 0.5, 0.5),
  (0.5, 0.5, 0.5),
  (0.5, 0.5, -0.5),
  (-0.5, 0.5, -0.5),
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
  (0, 4),
  (1, 5),
  (2, 6),
  (3, 7),
)

cam_verts = [[0.0, 0.0, 0.0] for _ in VERTS]

def bresenham(x0, y0, x1, y1):
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
    set_pixel(x0, y0, BLACK)

    if x0 == x1 and y0 == y1:
      break

    e2 = 2 * err
    if e2 >= dy:
      err += dy
      x0 += sx
    if e2 <= dx:
      err += dx
      y0 += sy

def outcode(x, y):
  code = 0
  
  if x < 0:
    code |= LEFT
  elif x > (SCR_W - 1):
    code |= RIGHT

  if y > SCR_H - 1:
    code |= BOTTOM
  elif y < 0:
    code |= TOP

  return code

def cohen_sutherland(x0, y0, x1, y1):
  while True:
    c0 = outcode(x0, y0)
    c1 = outcode(x1, y1)
    
    if (c0 | c1) == 0:
      return x0, y0, x1, y1
    if (c0 & c1) != 0:
      return None
  
    out = c0 if c0 != 0 else c1

    if out & LEFT:
      t = (0 - x0) / (x1 - x0)
      x = 0
      y = y0 + t * (y1 - y0)

    elif out & RIGHT:
      t = ((SCR_W - 1) - x0) / (x1 - x0)
      x = SCR_W - 1
      y = y0 + t * (y1 - y0)

    elif out & BOTTOM:
      t = ((SCR_H - 1) - y0) / (y1 - y0)
      x = x0 + t * (x1 - x0)
      y = SCR_H - 1

    elif out & TOP:
      t = (0 - y0) / (y1 - y0)
      x = x0 + t * (x1 - x0)
      y = 0

    if out == c0:
      x0, y0 = x, y
    else:
      x1, y1 = x, y

def draw():
  for i, p in enumerate(VERTS):
    x, y, z = p

    # Apply orientation matrix to object vertices
    rot_x = orient[0][0]*x + orient[0][1]*y + orient[0][2]*z
    rot_y = orient[1][0]*x + orient[1][1]*y + orient[1][2]*z
    rot_z = orient[2][0]*x + orient[2][1]*y + orient[2][2]*z

    # Apply translation
    cam_verts[i][0] = rot_x + obj_x
    cam_verts[i][1] = rot_y + obj_y
    cam_verts[i][2] = rot_z + obj_z

  # Near-plane clipping and drawing
  fill_rect(0, 0, SCR_W, SCR_H, WHITE)
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
    
    s_ax = SCR_CEN_X + ax / az * PROJ_S
    s_ay = SCR_CEN_Y - ay / az * PROJ_S
    s_bx = SCR_CEN_X + bx / bz * PROJ_S
    s_by = SCR_CEN_Y - by / bz * PROJ_S

    clipped = cohen_sutherland(s_ax, s_ay, s_bx, s_by)
    if clipped is not None:
      s_ax, s_ay, s_bx, s_by = clipped
      bresenham(s_ax, s_ay, s_bx, s_by)

def update(dt):
  global orient, obj_x, obj_y, obj_z

  rot_dir_x = keydown(KEY_UP) - keydown(KEY_DOWN)
  rot_dir_y = keydown(KEY_LEFT) - keydown(KEY_RIGHT)
  trans_dir_x = keydown(KEY_SIX) - keydown(KEY_FOUR)
  trans_dir_y = keydown(KEY_EIGHT) - keydown(KEY_TWO)
  trans_dir_z = keydown(KEY_NINE) - keydown(KEY_SEVEN)

  updated = False

  if rot_dir_x != 0:
    a = rot_dir_x * dt * ROT_SPEED
    s = sin(a)
    c = cos(a)
  
    for i in range(3):
      y = orient[1][i]
      z = orient[2][i]
  
      orient[1][i] = y*c - z*s
      orient[2][i] = y*s + z*c
  
    updated = True

  if rot_dir_y != 0:
    a = rot_dir_y * dt * ROT_SPEED
    s = sin(a)
    c = cos(a)
  
    for i in range(3):
      x = orient[0][i]
      z = orient[2][i]
  
      orient[0][i] = x*c + z*s
      orient[2][i] = -x*s + z*c
  
    updated = True

  if trans_dir_x:
    obj_x += trans_dir_x * dt * TRANS_SPEED
    updated = True

  if trans_dir_y:
    obj_y += trans_dir_y * dt * TRANS_SPEED
    updated = True

  if trans_dir_z:
    obj_z += trans_dir_z * dt * TRANS_SPEED
    updated = True

  if keydown(KEY_FIVE):
    obj_x = 0.0
    obj_y = 0.0
    obj_z = 2.0

    orient = [
      [1, 0, 0],
      [0, 1, 0],
      [0, 0, 1]
    ]

    updated = True

  return updated

def main():
  draw()
  prev_t = monotonic()
  
  while True:
    t = monotonic()
    dt = t - prev_t
    prev_t = t
    
    if update(dt):
      draw()

main()