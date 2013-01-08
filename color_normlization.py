#!/usr/bin/env python

from PIL import Image
import numpy as np
import os, sys

PARAM = 255.0

def normalize_pixel(pixels):
	#find min and max values 
	r_min = g_min = b_min = 255;
	r_max = g_max = b_max = 0;

	for i in range(len(pixels)):
		for r,g,b,a in pixels[i]:
			if r_min > r:
				r_min = r
			if g_min > g:
				g_min = g
			if b_min > b:
				b_min = b

			if r_max < r:
				r_max = r
			if g_max < g:
				g_max = g
			if b_max < b:
				b_max = b

  	scala_r = scala_g = scala_b = 0;

  	if r_max != r_min:
  		 scala_r = PARAM/(r_max - r_min) 
  	else:
  		scala_r = 1;

  	if g_max != g_min:
  		scala_g = PARAM/(g_max - g_min)
  	else:
  		scala_g = 1;

  	if b_max != b_min:
  		scala_b = PARAM/(b_max - b_min)
  	else:
  		scala_b = 1;

	normalized_RGBA_image = list()
	for i in range(len(pixels)):
		normalized_RGBA_image.append(list())
		for r,g,b,a in pixels[i]:
			r_new = (r - r_min) * scala_r 
			g_new = (g - g_min) * scala_g
			b_new = (b - b_min) * scala_b
			normalized_RGBA_image[i].append([r_new, g_new, b_new, a])
	return np.array(normalized_RGBA_image)


def process_image(input_image_path, output_image_path):
	image = Image.open(input_image_path).convert('RGBA')
	RGBA_array = np.array(np.asarray(image).astype('float'))

	output_image = Image.fromarray(normalize_pixel(RGBA_array).astype('uint8'), 'RGBA')
	output_image.save(output_image_path)


if __name__ == '__main__':
	if len(sys.argv) < 3:
		sys.exit('Usage: %s inputImage.png outputImage.png' % sys.argv[0])
	if not os.path.exists(sys.argv[1]):
		sys.exit('ERROR: Image %s was not found!' % sys.argv[1])

	process_image(sys.argv[1], sys.argv[2])