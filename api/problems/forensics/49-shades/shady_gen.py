import random
from PIL import Image

# random.seed(3741177)
random.seed(48275)
im = Image.new("RGB", (512, 512), "white")
pix = im.load()

colors = []
for i in range(0, 250, 5):
	colors.append(i)
	
odd = random.choice(colors)
colors.remove(odd)

file = open("solution", "w")
file.write("%x%x%x\n" % (odd, odd, odd))
file.close()

print len(colors), colors

for i in range(512):
	for j in range(512):
		chosen = random.choice(colors)
		# print chosen
		pix[i, j] = (chosen, chosen, chosen)

im.save("static/shades.png", "PNG")