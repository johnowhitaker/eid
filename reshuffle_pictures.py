# We had been doing cropping and such - these are the various scripts used...


import glob, os, fnmatch, sys
import piexif

# Sort out tags
ogfolder = os.getcwd() + "/../HipID_Photos/"
cropped_folder = os.getcwd() + "/../Cropped/"
ogsubfolders = [name for name in os.listdir(ogfolder) if os.path.isdir(os.path.join(ogfolder, name))]
cropped_subfolders = [name for name in os.listdir(cropped_folder) if os.path.isdir(os.path.join(cropped_folder, name))]
pics = []
cropped_pics = []
for subfolder in ogsubfolders:
    for p in glob.glob(ogfolder+subfolder+"/*.*"):
        pics.append (p)


for subfolder in cropped_subfolders:
    for p in glob.glob(cropped_folder+subfolder+"/*.*"):
        cropped_pics.append (p)

print len(pics)
print len(cropped_pics)
print pics[0]
print cropped_pics[0]
for i in range(len(cropped_pics)):
    if pics[i].split("/")[-1] != cropped_pics[i].split("/")[-1]:
        print pics[i], cropped_pics[i]
    else:
        try:
            piexif.transplant(pics[i], cropped_pics[i])
        except:
            print pics[i]


#copy across exif data
f = open(p, 'rb')
# tags = exifread.process_file(f)
date = ''
# if 'EXIF DateTimeDigitized' in tags.keys():
#     date = str(tags['EXIF DateTimeDigitized'])








# Moving back into folders
# for pic in glob.glob('/media/jonathan/9076-6521/renamed/*.JPG'):
#     folder = pic.split('#')[0]
#     fn = folder + "/" + pic.split('#')[1][:-4]
#     print fn
#     os.system("mv \"" + pic + "\" " + "\"" + fn + "\"")
#
# for pic in glob.glob('/media/jonathan/9076-6521/renamed/*.jpg'):
#     folder = pic.split('#')[0]
#     fn = folder + "/" + pic.split('#')[1][:-4]
#     print fn
#     os.system("mv \"" + pic + "\" " + "\"" + fn + "\"")





#resize:
#find . -iname '*.JPG' | while read file; do convert "$file" -resize 800x400 "$file".small; done






#The original shell script
# for directory in *; do
#   pushd "$directory"
#   index=1
#   for filename in *; do
#     extension="${filename##*.}"
#     if [ "$filename" != "$extension" ]; then
#       extension=".$extension"
#     else
#       # i.e. there is no dot in the file name
#       extension=""
#     fi
#     target_filename="${directory}$(printf "#")${filename}${extension}"
#     if [ -f "$target_filename" ]; then
#       echo "File ${target_filename} exists; aborting."
#       exit 3
#     fi
#     mv "$filename" "../${target_filename}"
#     ((index++))
#   done
#   popd
# done
