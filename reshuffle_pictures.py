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
