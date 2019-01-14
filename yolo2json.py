#!/usr/local/bin/python
import sys, getopt
import os, glob
import cv2
import random
from random import choice
import shutil
import decimal

def main(argv):
   try:
      opts, args = getopt.getopt(argv,"hd:x:y:n:r:",["todir=","xdim=", "ydim=","numclass", "ratio="])
   except getopt.GetoptError:
      print('-r <ratio>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print('-r <ratio>')
         sys.exit()
      elif opt in ("-d", "--todir"):
         todir = arg
      elif opt in ("-x", "--xdim"):
         dim_x = arg
      elif opt in("-y", "--ydim"):
         dim_y = arg
      elif opt in ("-n", "--numclass"):
         n_class = arg
      elif opt in ("-r", "--ratio"):
         ratio = arg
   
   # Input the class names
   n_class = int(n_class)
   classes = ""
   print("Enter classes in order of 0 to the number of classes")
   for i in range(0,n_class):
      #print("Enter next category")
      #next_input = raw_input()
      next_input = input("Enter next class: \n")
      classes = classes + next_input + " "

   # Create directories
   os.makedirs("train")
   os.makedirs("validation")
   os.makedirs("train_annotation")
   os.makedirs("validation_annotation")

   # Create an indexed list of all image files
   r_ordered_list = []
   img_dir_path = "data/obj/"
   index = 0
   for file in glob.glob(img_dir_path + "*.JPG"):
      r_ordered_list.append(str(index) + " " + file)
      index += 1

   # Randomly organise the list of all image files
   r_shuffled_list = random.sample(r_ordered_list, len(r_ordered_list))
   del r_ordered_list  # Do the right thing and free the memory

   # Create separate lists for training data and validation data. Split using provided ratio
   maximum=int(round(len(r_shuffled_list)*float(ratio)))
   r_train_list = r_shuffled_list[0:maximum]
   r_val_list = r_shuffled_list[maximum:]
   del r_shuffled_list # Free up memory

   # Read the YOLO output located in imagedir
   # For each image listed in train.txt and val.txt
   # Determine the dimensions of the image (height,width)
   # Read the txt file for the image and determine the bounding boxes
   # Write LST file in the format: index 4 5 0.0 xmin ymin xmax ymax ... img_file
   
   # Get the number of training and validation files
   num_train = len(r_train_list)
   num_val = len(r_val_list)

   # Create a jpeg and json file for every image in the training list
   # and save them to train and train_annotation folders respectively:
   for k in range(0, num_train):
      from_list = r_train_list[k]
      from_path = from_list.split()[1]
      from_path_txt = from_path[:len(from_path)-3]
      from_path_txt = from_path_txt + "txt"
      fname = from_path[9:len(from_path)-4]
      to_file = fname + ".json"

      # Copy jpeg into new folder called sample_image:
      to_photo = fname + ".jpg"
      to_folder = "train/"
      new_file_name = os.path.join(to_folder, to_photo)
      print(from_path)
      print(new_file_name)
      shutil.copy(from_path, new_file_name)

      # Now create the json file:
      # Write the file header
      from_file = open(from_path_txt, "r")
      to_path = "train_annotation/"
      to_file = fname + ".json"
      new_json_file_name = os.path.join(to_path, to_file)
      to_file = open(new_json_file_name, 'w+')
      to_file.write('{\n\t\"file\": \"' + todir + '/' + fname + '.jpg\",\n\t\"image_size\": [\n\t\t{\n\t\t\t\"width\": '+ str(dim_x) + ',\n')
      to_file.write('\t\t\t\"height\": '+str(dim_y) +',\n\t\t\t\"depth\": 3\n\t\t}\n\t],\n')

      # Write the annotations
      to_file.write('\t\"annotations\": [\n')
      data = from_file.readlines()
      num_lines = sum(1 for line in data)
      i = 1
      for line in data:
         class_id, mid_x, mid_y, width_x, width_y = line.split()
         class_id = int(class_id)
         mid_x = float(mid_x)
         mid_y = float(mid_y)
         width_x = float(width_x)
         width_y = float(width_y)
         left = int((mid_x - width_x/2) * float(dim_x))
         top = int((mid_y - width_y/2) * float(dim_y))
         width = int(width_x * float(dim_x))
         height = int(width_y * float(dim_y))
         to_file.write('\t\t{\n\t\t\t\"class_id\": ' + str(class_id) + ',\n\t\t\t\"left\": ' + str(left) +',\n\t\t\t\"top\": ' + str(top) + ',\n')
         to_file.write('\t\t\t\"width\": ' + str(width) + ',\n\t\t\t\"height\": ' + str(height) + '\n\t\t}' )
         if i is not num_lines:
            to_file.write(',')
            i = i + 1
         else:
            to_file.write('\n\t],\n')
      to_file.write('\t\"categories\": [\n')
      j = 1
      for c in classes.split(' ', n_class):
         if c is not "":
            to_file.write('\t\t{\n\t\t\t\"class_id\": ' + str(j-1) + ',\n\t\t\t\"name\": \"' + str(c) + '\"\n\t\t}')
            if j is not n_class:
               to_file.write(',\n')
            else:
               to_file.write('\n')
            j = j + 1
      to_file.write('\t]\n}')


   # Create a jpeg and json file for every image in the validation list
   # and save them to train and train_annotation folders respectively:
   for k in range(0, num_val):
      from_list = r_val_list[k]
      from_path = from_list.split()[1]
      from_path_txt = from_path[:len(from_path)-3]
      from_path_txt = from_path_txt + "txt"
      fname = from_path[9:len(from_path)-4]
      to_file = fname + ".json"

      # Copy jpeg into new folder called sample_image:
       # Copy jpeg into new folder called sample_image:
      to_photo = fname + ".jpg"
      to_folder = "validation/"
      new_file_name = os.path.join(to_folder, to_photo)
      shutil.copy(from_path, new_file_name)

      # Now create the json file:
      # Write the file header
      from_file = open(from_path_txt, "r")
      to_path = "validation_annotation/"
      to_file = fname + ".json"
      new_json_file_name = os.path.join(to_path, to_file)
      to_file = open(new_json_file_name, 'w+')
      to_file.write('{\n\t\"file\": \"' + todir + '/' + fname + '.jpg\",\n\t\"image_size\": [\n\t\t{\n\t\t\t\"width\": '+ str(dim_x) + ',\n')
      to_file.write('\t\t\t\"height\": '+str(dim_y) +',\n\t\t\t\"depth\": 3\n\t\t}\n\t],\n')

      # Write the annotations
      to_file.write('\t\"annotations\": [\n')
      data = from_file.readlines()
      num_lines = sum(1 for line in data)
      i = 1
      for line in data:
         class_id, mid_x, mid_y, width_x, width_y = line.split()
         class_id = int(class_id)
         mid_x = float(mid_x)
         mid_y = float(mid_y)
         width_x = float(width_x)
         width_y = float(width_y)
         left = int((mid_x - width_x/2) * float(dim_x))
         top = int((mid_y - width_y/2) * float(dim_y))
         width = int(width_x * float(dim_x))
         height = int(width_y * float(dim_y))
         to_file.write('\t\t{\n\t\t\t\"class_id\": ' + str(class_id) + ',\n\t\t\t\"left\": ' + str(left) +',\n\t\t\t\"top\": ' + str(top) + ',\n')
         to_file.write('\t\t\t\"width\": ' + str(width) + ',\n\t\t\t\"height\": ' + str(height) + '\n\t\t}' )
         if i is not num_lines:
            to_file.write(',')
            i = i + 1
         else:
            to_file.write('\n\t],\n')
      to_file.write('\t\"categories\": [\n')
      j = 1
      for c in classes.split(' ', n_class):
         if c is not "":
            to_file.write('\t\t{\n\t\t\t\"class_id\": ' + str(j-1) + ',\n\t\t\t\"name\": \"' + str(c) + '\"\n\t\t}')
            if j is not n_class:
               to_file.write(',\n')
            else:
               to_file.write('\n')
            j = j + 1
      to_file.write('\t]\n}')





#def create_lst_file(fname_lst,list):
#   f_file_lst = open(fname_lst, "w")  # f_file_lst will need to be closed later, this is the file we will write to
#   for entry in list:
#      index, img_file = entry.split(" ")
#      img=cv2.imread(img_file)
#      height, width = img.shape[:2]
#      lst_entry = str(index) + " 4 5 " + str(width) + " " + str(height)
#      individual_image_txt_file=os.path.splitext(img_file)[0] + '.txt'
#      with open(individual_image_txt_file) as f_ind_txt_file: #f_ind_txt_file will auto-close, this is the text file containing BB information for an individual image
 #        for object_bb in f_ind_txt_file: # Each individual txt file will contain one or more bounding box objects. We must parse each one.
#            if object_bb[-1:] == "\n":
#               object_bb = object_bb[:-1]
#            obj_class, xmid, ymid, bb_width, bb_height = object_bb.split(" ") # Split each BB information line into its components
#            # Convert BB details to format required by LST
#            xmin = float(xmid) - (float(bb_width) / 2)
#            ymin = float(ymid) - (float(bb_height) / 2)
#            xmax = float(xmid) + (float(bb_width) / 2)
#            ymax = float(ymid) + (float(bb_height) / 2)
#            lst_entry = lst_entry + " " + obj_class + ".0 " + str(xmin) + " " + str(ymin) + " " + str(xmax) + " " + str(ymax) # Append current BB object to lst_entry
#      lst_entry = lst_entry + " " + img_file
#      f_file_lst.write(lst_entry + '\n')
#   f_file_lst.close() # We have finished writing to this LST file. Close it now

if __name__ == "__main__":
   main(sys.argv[1:])




