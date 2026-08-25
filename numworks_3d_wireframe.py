from kandinsky import set_pixel, color

SCR_W = 320
SCR_H = 222

BLACK = color(0, 0, 0)

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

def main():
  bresenham(10, 10, SCR_W - 10, SCR_H - 10)
  bresenham(SCR_W - 10, 10, 10, SCR_H - 10)

main()