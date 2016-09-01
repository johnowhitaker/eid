# We had been doing cropping and such - these are the various scripts used...


import glob, os, fnmatch, sys

for pic in glob.glob('/media/jonathan/9076-6521/renamed/*.jpg'):
    folder = pic.split('#')[0]
    fn = folder + "/" + pic.split('#')[1][:-4]
    print fn
    os.system("mv \"" + pic + "\" " + "\"" + fn + "\"")

for pic in glob.glob('/media/jonathan/9076-6521/renamed/*.jpg'):
    folder = pic.split('#')[0]
    fn = folder + "/" + pic.split('#')[1][:-4]
    print fn
    os.system("mv \"" + pic + "\" " + "\"" + fn + "\"")



#Compress:
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
