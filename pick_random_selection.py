# For your given directory and given number of images wanted,
# This program makes a random selection of that number of images,
# and stores them in a file called chosen.
# To accomplish this, the program first renames the images by ascending number
# and stores them in a directory called numbered.
# Inputs:
# -i <Your directory>
# -n <Number of images wanted>


#!/usr/local/bin/python3
from PIL import Image
import os
import cv2
import sys, getopt
import random


def listdir_nohidden(path):
	for f in os.listdir(path):
		if not f.startswith('.'):
			yield f



def main(argv):
	try:
		opts, args = getopt.getopt(argv, "hi:n:", ["idir=","num="])
	except getopt.GetoptError:
		print('resize.py -i <imagedir>')
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print('resize.py -i <imagedir>')
			sys.exit()
		elif opt in ("-i", "--idir"):
			image_dir = arg
		elif opt in ("-n", "--num"):
			no_wanted = arg
			print(no_wanted)

	# Rename images
	c = 0
	files=listdir_nohidden(image_dir)
	if files is not None:
		for filename in files:
			img = cv2.imread(os.path.join(image_dir, filename))
			if img is not None:
				c +=1
				new_name = str(c) + ".jpg"
				new_path = os.path.join(image_dir, 'numbered')
				if not os.path.exists(new_path):
					os.makedirs(new_path)
				cv2.imwrite(os.path.join(new_path,new_name), img)

	# Create a list with random integers from 1 to the number of images
	k = 0
	int_used = list()
	while k<int(no_wanted):
		rand_int = random.randint(1,c)
		if rand_int not in int_used:
			int_used.append(rand_int)
			k+=1

	# Write random selection of images to new file
	for img_no in int_used:
		img_name = str(img_no) + ".jpg"
		new_path = os.path.join(image_dir, 'chosen')
		if not os.path.exists(new_path):
			os.makedirs(new_path)
		from_path = os.path.join(image_dir, 'numbered')
		img =cv2.imread(os.path.join(from_path, img_name))
		cv2.imwrite(os.path.join(new_path, img_name), img)




if __name__ == "__main__":
	main(sys.argv[1:])