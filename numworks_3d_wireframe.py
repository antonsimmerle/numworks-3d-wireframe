from kandinsky import color, fill_rect, set_pixel
from math import sin, cos
from time import sleep

# TODO: add 3d projection and rotation matrixes in x, y, z

X_MAX = 320
Y_MAX = 222
X_CEN = X_MAX // 2
Y_CEN = Y_MAX // 2

BLACK = color(0, 0, 0)
WHITE = color(255, 255, 255)

SCALE = 100
FRAME_TIME = 1/30
ang = 0

VERTICES = [
  (-0.5, -0.5),
  (-0.5, 0.5),
  (0.5,  -0.5),
  (0.5,  0.5)
]

EDGES = [
  (0, 1),
  (1, 3),
  (2, 0),
  (2, 3)
]

def r_to_a(p):
  x, y = p
  return (int(x*SCALE + X_CEN),
          int(Y_CEN - y*SCALE))

# TODO: draw_line returns a set of pixels
def draw_line(r1, r2):
  ax1, ay1 = r_to_a(r1)
  ax2, ay2 = r_to_a(r2)
  
  dx = ax2 - ax1
  dy = ay2 - ay1
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
    set_pixel(ax1 + x*prim_x + y*sec_x,
              ay1 + x*prim_y + y*sec_y, BLACK)
    if D < 0:
      D = D + 2*dy
    else:
      y += 1
      D = D + 2*(dy - dx)

def mat_vec(mat, vec):
  return (vec[0]*mat[0][0] + vec[1]*mat[0][1],
          vec[0]*mat[1][0] + vec[1]*mat[1][1])
  
def draw():
  global ang

  # TODO: draw only changed pixels from the previous draw using sets
  fill_rect(0, 0, X_MAX, Y_MAX, WHITE)
  
  s = sin(ang)
  c = cos(ang)
  R = [(c, -s),
       (s, c )]

  rotated_vertices = []
  for p in VERTICES:
    rotated_point = mat_vec(R, p)
    rotated_vertices.append(rotated_point)

  for a, b in EDGES:
    x1, y1 = rotated_vertices[a]
    x2, y2 = rotated_vertices[b]
    draw_line((x1, y1), (x2, y2))

  ang += 0.1

def main():
  for _ in range(200):
    draw()
    sleep(FRAME_TIME)

main()