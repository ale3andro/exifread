#!/usr/bin/python3
# -*- coding: utf-8 -*-

# revision 04 - 25/12/2022
# Python3 script

import piexif, shutil,os, glob

filename = "IMG_0625.JPG"
directory_name = "alec"
no_exif_directory_name = "no_exif"
png_directory_name = "png"

if not os.path.exists(directory_name):
    os.makedirs(directory_name)
if not os.path.exists(no_exif_directory_name):
    os.makedirs(no_exif_directory_name)
if not os.path.exists(png_directory_name):
    os.makedirs(png_directory_name)

all_files = glob.glob("*.PNG")
for item in all_files:
    shutil.move(item, png_directory_name)

all_files = glob.glob("*.JPG")
files_counter=0
for item in all_files:
    print("Processing:", item)
    exif_dict = piexif.load(item)
    ifd="0th"
    isFound=False
    for tag in exif_dict[ifd]:
        if (piexif.TAGS["0th"][tag]["name"]=="DateTime"):
            isFound=True
            #print item
            #print(piexif.TAGS[ifd][tag]["name"], exif_dict[ifd][tag])
            date_taken = exif_dict[ifd][tag][0:10].decode("utf-8")
            new_date = date_taken.replace(":","-")
            month_folder_name = new_date[:7]
            os.chdir(directory_name)
            if not os.path.exists(month_folder_name):
                os.makedirs(month_folder_name)
            os.chdir('..')
            shutil.move(item, directory_name+'/'+month_folder_name+'/'+new_date+'__'+item)
    if (not isFound):
        print("Δεν βρέθηκε tag στο αρχείο: " + item)
        shutil.move(item, no_exif_directory_name)
    else:
        files_counter+=1

print(str(files_counter) + " copied and renamed")
