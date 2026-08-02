from kandinsky import color, fill_rect, set_pixel
from math import sin, cos
from time import sleep
from ion import *

X_MAX = 320
Y_MAX = 222
X_CEN = X_MAX // 2
Y_CEN = Y_MAX // 2

BLACK = color(0, 0, 0)
WHITE = color(255, 255, 255)

angx = 0
angy = 0
#angz = 0
FRAME_TIME = 1/30
ROT_SPEED = 0.3

SCALE = 100

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

# TODO: draw_line returns a set of pixels
def draw_line(x1, y1, x2, y2):  
  dx = x2 - x1
  dy = y2 - y1
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
  y = 0
  for x in range(dx + 1):
    set_pixel(x1 + x*prim_x + y*sec_x,
              y1 + x*prim_y + y*sec_y, BLACK)
    if D < 0:
      D = D + 2*dy
    else:
      y += 1
      D = D + 2*(dy - dx)

# TODO: make rotation world axis for x and y
def rotate_vert(p, sx, cx, sy, cy):
  x, y, z = p
  # Rotate X
  y1 = y*cx - z*sx
  z1 = y*sx + z*cx
  
  # Rotate Y
  x1 = x*cy + z1*sy
  z1 = x*(-sy) + z1*cy
  
  return (x1, y1, z1)

def proj_vert(p):
  x, y, z = p
  return (int(x*SCALE + X_CEN),
          int(Y_CEN - y*SCALE))
  
def draw():
  # TODO: draw only changed pixels from the previous draw using sets
  fill_rect(0, 0, X_MAX, Y_MAX, WHITE)
  
  sx = sin(angx)
  cx = cos(angx)
  sy = sin(angy)
  cy = cos(angy)

  # TODO: use fixed size arrays
  rot_verts = [
    rotate_vert(p, sx, cx, sy, cy)
    for p in VERTS
  ]
  proj_verts = [
    proj_vert(p)
    for p in rot_verts
  ]
  
  for a, b in EDGES:
    draw_line(proj_verts[a][0],
              proj_verts[a][1],
              proj_verts[b][0],
              proj_verts[b][1])

def update():
  global angx, angy, ROT_SPEED
  updated = False
  # TODO: add deltatime rotation and radians per second
  # TODO: normalize angles if they exeed 2Pi
  if (keydown(KEY_UP)):
    angx -= ROT_SPEED
    updated = True
  if (keydown(KEY_DOWN)):
    angx += ROT_SPEED
    updated = True
  if (keydown(KEY_LEFT)):
    angy -= ROT_SPEED
    updated = True
  if (keydown(KEY_RIGHT)):
    angy += ROT_SPEED
    updated = True

  return updated  

def main():
  draw()
  for _ in range(500):
    if (update()):
      draw()
    # TODO: sleep the actual time difference
    # TODO: Manage overshooting the deadline
    sleep(FRAME_TIME)

main()