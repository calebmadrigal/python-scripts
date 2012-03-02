# Answer: integrity
# Note: I cropped out the gray bar to a separate image.
import Image

#img = Image.open("oxygen_bar.png")
img = Image.open("oxygen.png")


y_offset = 0
for i in range(img.size[1]):
   color = img.getpixel((50, i))
   if color[0] == color[1] == color[2]:
      y_offset = i
      break

colors = [ord(' ')] # Need something in here so I can do colors[-1] below.
for i in range(img.size[0]):
   color = img.getpixel((i, y_offset))
   if color[0] == color[1] == color[2]:
      if colors[-1] != color[0]:
         colors.append(color[0])

print ''.join([chr(i) for i in colors])

print ''.join([chr(i) for i in [105, 110, 116, 101, 103, 114, 105, 116, 121]])
