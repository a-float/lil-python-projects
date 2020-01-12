from PIL import Image 

width, height = 480,360
canv = Image.new("HSV", (width, height))
 
zoom = 1.3
lx, ly = 4, 3
cx, cy = -0.761574,-0.0847596
max_iter = 50
frames_count = 24

def calc_frac(x, y):
  c = ((x/width - 0.5) * (lx/zoom) ,(y/height - 0.5) * (ly/zoom))
  z = (0,0)
  for i in range(max_iter):
    z = (cx + z[0]**2 - z[1]**2 + c[0], cy +  2*z[0]*z[1] + c[1])
    if(z[0] == 0 and z[1] == 0):
      return (255,255,255)
    elif(abs(z[0]) > 2 or abs(z[1]) > 2):
      return (int(i/max_iter *255),0,0)
  return (255,255,255)

for f in range(frames_count):
    for i in range(height):
        for j in range(width):
            canv.putpixel((j,i), calc_frac(j,i))
    zoom*=(1+(f+1)/3)
    max_iter+=6
    print("saving {} out of {}".format(f, frames_count))
    canv.save("othermandelbrot{}.png".format(f))
    #canv.show()
