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
rot_x = 0.0
rot_y = 0.0

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

    # Rotate around X
    x1 = x
    y1 = y * cos_x - z * sin_x
    z1 = y * sin_x + z * cos_x
    # Rotate around Y
    x2 = x1 * cos_y + z1 * sin_y
    y2 = y1
    z2 = -x1 * sin_y + z1 * cos_y

    cam_verts[i][0] = x2 + obj_x
    cam_verts[i][1] = y2 + obj_y
    cam_verts[i][2] = z2 + obj_z

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
  global rot_x, rot_y, sin_x, cos_x, sin_y, cos_y, obj_x, obj_y, obj_z

  rot_dir_x = keydown(KEY_UP) - keydown(KEY_DOWN)
  rot_dir_y = keydown(KEY_LEFT) - keydown(KEY_RIGHT)
  trans_dir_x = keydown(KEY_SIX) - keydown(KEY_FOUR)
  trans_dir_y = keydown(KEY_EIGHT) - keydown(KEY_TWO)
  trans_dir_z = keydown(KEY_NINE) - keydown(KEY_SEVEN)

  updated = False

  if rot_dir_x:
    rot_x += rot_dir_x * dt * ROT_SPEED
    sin_x = sin(rot_x)
    cos_x = cos(rot_x)
    updated = True
  
  if rot_dir_y:
    rot_y += rot_dir_y * dt * ROT_SPEED
    sin_y = sin(rot_y)
    cos_y = cos(rot_y)
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
    rot_x = 0.0
    rot_y = 0.0
    obj_x = 0.0
    obj_y = 0.0
    obj_z = 2.0

    sin_x = 0.0
    cos_x = 1.0
    sin_y = 0.0
    cos_y = 1.0

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