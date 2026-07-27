from kandinsky import color, set_pixel

x_max = 320
y_max = 222
x_cen = 160
y_cen = 111

black = color(0, 0, 0)
white = color(255, 255, 255)

def draw_line(rx1, ry1, rx2, ry2, scale):
  ax1 = int(rx1*scale + x_cen)
  ax2 = int(rx2*scale + x_cen)
  ay1 = int(y_cen - ry1*scale)
  ay2 = int(y_cen - ry2*scale)
  
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
              ay1 + x*prim_y + y*sec_y, black)
    if D < 0:
      D = D + 2*dy
    else:
      y += 1
      D = D + 2*(dy - dx)

draw_line(-0.5, -0.5, 0.5, 0.5, 100)