# Utility for the pachydentify app, to generate smaller images
# Copyright (c) 2016 Jonathan Whitaker, johnowhitaker@gmail.com
# Licenced under the GPL, available at https://www.gnu.org/licenses/gpl-3.0.en.html

import glob, xlrd, os, sys, re
import exifread
import argparse
import os, sys
import Image


#************************************************************************************
#   THE IMPORTANT BITS - WILL ADD OTHER PARAMETERS HERE FOR EASY CONFIGURATION     **
#************************************************************************************
SPREADSHEET = "/home/jonathan/Elephant_MAY/raw_data/Elephants.xlsx"#os.getcwd() + "/../eid_sample_data/elephants.xlsx" #
SHEETNUM = 0
PHOTODIR = "/home/jonathan/Elephant_MAY/HIP_ID_PHOTOS_TIM_MAY"

PHOTO_HEIGHT = 400 #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< EDIT THIS <<<<<<

# Store features, elephant ID and so on
class Elephant:
    # So many of these getters and setters are unneccesary - the vars
    # are mostly public. Slowly replacing them.
    def __init__(self):
        #self.photo_folder = photof
        self.photo_folder = ""#"../photos/BH003"
        self.photos = []
        self.small_photos = []
        self.eid = "" # Elephant ID
        self.features = {}
        self.notes = {}
        self.photos = []#glob.glob(self.photo_folder+"/*.jpg")
        self.mismatches = 0
        self.hidden = False # Allow hiding the elephants

    # def zeroMismatches(self):
    #     self.mismatches = 0
    # def incMismatches(self):
    #     self.mismatches += 1
    # def getMisMatches(self):
    #     return self.mismatches

    def setPhotoFolder(self, folder):
        self.photo_folder = folder
        # Are these enough extensions? Who knows...
        for ext in ['*.gif', '*.png', '*.PNG', '*.jpg', '*.JPG', '*.JPEG', '*.jpeg']:
            self.photos.extend(glob.glob(self.photo_folder+'/'+ext))

    def setSmallPhotoFolder(self, folder): # merge into setPhotoFolder?
        self.small_photos = glob.glob(folder+'/*.small')
        for p in self.small_photos:
            p = p[:-6] #remove the .small part

    # def getPhotos(self): # Is this needed? Or am i being a java guy?... Java guy :)
    #     return self.photos

    # def getSmallPhotos(self):
    #     return self.small_photos

    def printSelf(self):
        print(self.photos)
        for f in self.features:
            if self.features[f]!= '':
                print(f + ": " + self.features[f])

    def setFeature(self, fname, value):
        self.features[fname] = str(value)

    def getFeature(self, fname):
        return self.features[fname]

    # def getFeatures(self):
    #     return self.features

    def setNote(self, fname, value):
        self.notes[fname] = str(value)

    def getNote(self, fname):
        return self.notes[fname]

    def getNotes(self): #?
        return self.notes

    def setID(self, id):
        self.eid = id

    def getID(self):
        return self.eid

# A collection of elephants, can be filtered etc
class Herd:
    # Herd stores all elephants, and a filtered subset. Can apply different filters etc
    def __init__(self, filename, sheet_num, photo_folder):
        # Read the data from the spreadsheet into an array of elephants
        self.elephants = self.load_from_spreadsheet(filename, sheet_num, photo_folder)
        self.filtered_elephants = [e for e in self.elephants]
        self.sorted_elephants = []
        self.features = self.elephants[0].features.keys()
        self.possible_values = {f:[] for f in self.features}
        # for each feature, possible values has a corresponding list of values that feature can take on
        for f in self.features:
            self.possible_values[f].append("")
            for e in self.elephants:
                if e.getFeature(f) not in self.possible_values[f]:
                     self.possible_values[f].append(e.getFeature(f))

    def load_from_spreadsheet(self, sheet_file, sheet_of_interest, photo_folder):
        elephants = []
        workbook = xlrd.open_workbook(sheet_file)
        sheet = workbook.sheet_by_index(sheet_of_interest) # Could also do by name <<<
        # iterate over rows with elephants
        row = 1
        while row<sheet.nrows: # Column 0 is the elephant ID. If it's empty, we've reached the end <<
            # Next elephant (next row)
            e = Elephant()
            e.setID(sheet.cell(row, 0).value)
            # Go through columns.
            column = 1
            while column<sheet.ncols:
                val = sheet.cell(row, column).value
                heading = sheet.cell(0, column).value # First row has headings
                if not "*" in heading: # Add a * to a heading for special treatment
                    e.setFeature(str(heading), val)
                else:
                    e.setNote(str(heading), val)
                column +=1
            # :(
            if os.path.isdir(photo_folder+"/" + e.getID().upper()):
                e.setPhotoFolder(photo_folder+"/" + e.getID().upper())
            elif os.path.isdir(photo_folder+"/" + e.getID()):
                e.setPhotoFolder(photo_folder+"/" + e.getID())

            # Same for small (assuming they're in the same folder)- could make this cleaner <<
            if os.path.isdir(photo_folder+"/" + e.getID().upper()):
                e.setSmallPhotoFolder(photo_folder+"/" + e.getID().upper())
            elif os.path.isdir(photo_folder+"/" + e.getID()):
                e.setSmallPhotoFolder(photo_folder+"/" + e.getID())

            elephants.append(e)
            row += 1
        return elephants

    # def getFeatures(self):
    #     return self.features
    def getPossibleValues(self, f):
        return self.possible_values[f]
    def getElephants(self):
        return self.elephants

    def filter(self, constraints): # {feature:[options]}
        print constraints
        # Loop though, adding matches
        self.filtered_elephants = []
        for e in self.elephants:
            e.mismatches = 0
            for f in constraints.keys():
                if not ((e.getFeature(f) in constraints[f]) or constraints[f] == []):
                        e.mismatches += 1
            if e.mismatches == 0:
                self.filtered_elephants.append(e)
        # Loop through again, adding ones that match *
        for e in self.elephants:
            e.mismatches = 0
            for f in constraints.keys():
                if not ((e.getFeature(f) in constraints[f]) or constraints[f] == [] or "*" in constraints[f] or "*" in constraints[f]):
                        e.mismatches += 1
            if e.mismatches == 0 and e not in self.filtered_elephants:
                self.filtered_elephants.append(e)
        return self.filtered_elephants

    def filterLoose(self, constraints, n):
        self.filter(constraints)
        self.sorted_elephants = [e for e in self.filtered_elephants]
        near = 0
        for i in range(n):
            for e in self.elephants:
                if e.mismatches == n:
                    self.sorted_elephants.append(e)
                    near += 1
        print "including "+str(near)+" near misses"
        return self.sorted_elephants

    def clearFilters():
        for e in self.elephants:
            e.hidden = False # Un-hide all
        self.filtered_elephants = [e for e in self.elephants]

herd = Herd(SPREADSHEET, SHEETNUM, PHOTODIR)

for e in herd.getElephants():
    for p in e.photos:

        size = PHOTO_HEIGHT, PHOTO_HEIGHT
        outfile = p+ ".small" #os.path.splitext(p)[0] + ".small"
        if p != outfile:
            try:
                im = Image.open(p)
                im.thumbnail(size, Image.ANTIALIAS)
                im.save(outfile, "JPEG")
                print "Saved: ", outfile
            except IOError:
                print "cannot create thumbnail for '%s'" % p
