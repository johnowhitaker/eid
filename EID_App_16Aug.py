# App for rapid photo identification of elephants
# Copyright (c) 2016 Jonathan Whitaker, johnowhitaker@gmail.com
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


import glob, xlrd, os, sys
from PyQt4 import QtCore, QtGui
from test_ui import Ui_Form

#************************************************************************************
#   THE IMPORTANT BITS - WILL ADD OTHER PARAMETERS HERE FOR EASY CONFIGURATION     **
#************************************************************************************
SPREADSHEET = os.getcwd() + "/../photo_id_29_aug.xlsm"
SHEETNUM = 3
PHOTODIR = os.getcwd() + "/../HipID_Photos"

# Store features, elephant ID and so on
class Elephant:

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

    def zeroMismatches(self):
        self.mismatches = 0
    def incMismatches(self):
        self.mismatches += 1
    def getMisMatches(self):
        return self.mismatches

    def setPhotoArr(self, photos):
        self.photos = photos

    def setPhotoFolder(self, folder):
        self.photo_folder = folder
        # Are these enough extensions? Who knows...
        for ext in ['*.gif', '*.png', '*.PNG', '*.jpg', '*.JPG', '*.JPEG', '*.jpeg']:
            self.photos.extend(glob.glob(self.photo_folder+'/'+ext))

    def setSmallPhotos(self, folder):
        self.small_photos = glob.glob(folder+"/" + self.getID().upper()+'/*.small')
        for p in self.small_photos:
            p = p[:-6] #remove the .small part

    def getPhotos(self):
        return self.photos

    def getSmallPhotos(self):
        return self.small_photos

    def printSelf(self):
        print(self.photos)
        for f in self.features:
            if self.features[f]!= '':
                print(f + ": " + self.features[f])

    def showPhoto(self, n):
        im = Image.open(self.photos[n])
        im.show()

    def setFeature(self, fname, value):
        self.features[fname] = str(value)

    def getFeature(self, fname):
        return self.features[fname]

    def getFeatures(self): #make safe <<<<<<<
        return self.features

    def setNote(self, fname, value):
        self.notes[fname] = str(value)

    def getNote(self, fname):
        return self.notes[fname]

    def getNotes(self): #make safe <<<<<<<
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
        self.features = self.elephants[0].getFeatures().keys()
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
            e.setPhotoFolder(photo_folder) ##<<<< WRONG, remove...
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
            e.setPhotoFolder(photo_folder+"/" + e.getID().upper())
            elephants.append(e)
            row += 1
        return elephants

    def getFeatures(self):
        return self.features
    def getPossibleValues(self, f):
        return self.possible_values[f]
    def getElephants(self):
        return self.elephants

    def filter(self, constraints): # {feature:[options]}
        print constraints
        # Loop though, adding matches
        self.filtered_elephants = []
        for e in self.elephants:
            e.zeroMismatches()
            for f in constraints.keys():
                if not ((e.getFeature(f) in constraints[f]) or constraints[f] == []):
                        e.incMismatches()
            if e.getMisMatches() == 0:
                self.filtered_elephants.append(e)
        # Loop through again, adding ones that match *
        for e in self.elephants:
            e.zeroMismatches()
            for f in constraints.keys():
                if not ((e.getFeature(f) in constraints[f]) or constraints[f] == [] or "*" in constraints[f] or "*" in constraints[f]):
                        e.incMismatches()
            if e.getMisMatches() == 0 and e not in self.filtered_elephants:
                self.filtered_elephants.append(e)
        return self.filtered_elephants

    def filterLoose(self, constraints, n):
        self.filter(constraints)
        self.sorted_elephants = [e for e in self.filtered_elephants]
        near = 0
        for i in range(n):
            for e in self.elephants:
                if e.getMisMatches() == n:
                    self.sorted_elephants.append(e)
                    near += 1
        print "including "+str(near)+" near misses"
        return self.sorted_elephants

    def clearFilters():
        self.filtered_elephants = [e for e in self.elephants]

# The GUI side of things, currently holding most of the logic
class EID_FORM(QtGui.QWidget):

    picture_elephants = {}
    pic_area_widgets = [] # Cheap late night hack - will fix at some point

    def __init__(self, spreadsheet, sheet_num,  photo_folder, parent=None):
        # UI from designer
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.herd = Herd(spreadsheet, 3, photo_folder)

        # Connect btn_load_herd to function
        self.ui.btn_apply_filter.clicked.connect(self.filterClicked)
        self.ui.btn_clear_filter.clicked.connect(self.clearFilters)

        self.load_herd(self.herd.getElephants())
        for e in self.herd.getElephants():
            e.setSmallPhotos(photo_folder)
        self.init_picture_area(self.herd.getElephants())

    # GO through every item in the tree view and set to un-checked. Doeasn't apply filter
    def clearFilters(self, btn):
        root = self.model.invisibleRootItem() # get model properly?
        filter_values= {}
        i = 0
        while True:
            item = root.child(i)
            if item is None:
                break
            v = 0
            while True:
                value = item.child(v)
                if value is None:
                    break
                value.setCheckState(0)
                v += 1
            i += 1

    #Ignore - UI stuff
    def clickable(self, widget):
        class Filter(QtCore.QObject):
            clicked = QtCore.pyqtSignal(QtGui.QWidget)
            def eventFilter(self, obj, event):

                if obj == widget:
                    if event.type() == QtCore.QEvent.MouseButtonRelease:
                        if obj.rect().contains(event.pos()):
                            self.clicked.emit(obj)
                            # The developer can opt for .emit(obj) to get the object within the slot.
                            return True

                return False
        filter = Filter(widget)
        widget.installEventFilter(filter)
        return filter.clicked

    # Run when the "Apply Filter" button is clicked
    def filterClicked(self, btn):
        self.filter_elephants()

    # Loads data from a spreadsheet into a herd, and create the filter options.
    def load_herd(self, elephants):
        # Loading the data
        features = elephants[0].getFeatures().keys()
        possible_values = {f:[] for f in features}
        # for each feature, possible values has a corresponding list of values that feature can take on
        for f in features:
            possible_values[f].append("*")
            for e in elephants:
                if e.getFeature(f) not in possible_values[f]:
                     possible_values[f].append(e.getFeature(f))
        print "loading: " + str(len(elephants))

        #Clear the UI
        while self.ui.scrlw.layout().count():
            item = self.ui.scrlw.layout().takeAt(0)
            widget = item.widget()
            widget.deleteLater()

        tree = self.ui.treeView
        model = QtGui.QStandardItemModel(tree)
        self.model = model
        for f in features:
            item = QtGui.QStandardItem()
            item.setText(f)
            for p in possible_values[f]:
                citem = QtGui.QStandardItem()
                citem.setText(p)
                citem.setCheckable(True)
                citem.setTristate(True)
                item.appendRow(citem)
            model.appendRow(item)
        tree.setModel(model)
        tree.show()


    # Inefficient, and struggles with large images apparetly << fixed? Yup :)
    def update_pics_area(self, elephants):
        print "updating picture area"
        #Clear the UI
        # for e in elephants:
        #     # Check if we already have a pic of it up
        #     already_added = False
        #     for ellie in self.picture_elephants.values():
        #         if e.getID() == ellie.getID():
        #             already_added = True
        #             break
        #     if already_added:
        #         pass
        #     #otherwise:

            # lb1 = QtGui.QLabel(e.getID())
            # g = QtGui.QWidget()
            # g.setLayout(QtGui.QHBoxLayout())
            # g.layout().addWidget(lb1)
            # self.picture_elephants[lb1] = e
            # self.clickable(lb1).connect(self.show_notes)
            # for p in e.getPhotos():
            #     lb = QtGui.QLabel()
            #     lb.setGeometry(10, 10, 400, 400)
            #     lb.setPixmap(QtGui.QPixmap(p).scaled(lb.size(), QtCore.Qt.KeepAspectRatio))
            #     g.layout().addWidget(lb)
            #     self.picture_elephants[lb] = e
            #     self.clickable(lb).connect(self.show_notes)
            # self.ui.scrlw.layout().addWidget(g)
            # self.pic_area_widgets.append(g)

        # # Get rid of unwanted ones
        # to_delete = []
        # for widget in self.picture_elephants:
        #     e = self.picture_elephants[widget]
        #     keeping = False
        #     for ellie in elephants:
        #         if ellie.getID() == e.getID():
        #             keeping = True
        #     if not keeping:
        #         to_delete.append(widget)
        #         widget.deleteLater()
        # for w in to_delete:
        #     del self.picture_elephants[w]

        for widget in self.picture_elephants:
            e = self.picture_elephants[widget]
            keeping = False
            for ellie in elephants:
                if ellie.getID() == e.getID():
                    keeping = True
                    break
            if keeping:
                widget.parent().show()
            else:
                widget.parent().hide()


    #Adding the pictures, and clicking on them calls show_notes
    def init_picture_area(self, elephants):
        for e in elephants:
            lb1 = QtGui.QLabel(e.getID())
            g = QtGui.QWidget()
            g.setLayout(QtGui.QHBoxLayout())
            g.layout().addWidget(lb1)
            self.picture_elephants[lb1] = e
            self.clickable(lb1).connect(self.show_notes)
            if len(e.getSmallPhotos())!=0:
                for p in e.getSmallPhotos():
                    lb = QtGui.QLabel()
                    lb.setGeometry(10, 10, 400, 400)
                    lb.setPixmap(QtGui.QPixmap(p))
                    g.layout().addWidget(lb)
                    self.picture_elephants[lb] = e
                    self.clickable(lb).connect(self.show_notes)
            else:
                for p in e.getPhotos():
                    lb = QtGui.QLabel()
                    lb.setGeometry(10, 10, 400, 400)
                    lb.setPixmap(QtGui.QPixmap(p).scaled(lb.size(), QtCore.Qt.KeepAspectRatio))
                    g.layout().addWidget(lb)
                    self.picture_elephants[lb] = e
                    self.clickable(lb).connect(self.show_notes)
            self.ui.scrlw.layout().addWidget(g)
            self.pic_area_widgets.append(g)

    def update_herd(self, elephants):

        # #Clear the UI
        # while self.ui.scrlw.layout().count():
        #     item = self.ui.scrlw.layout().takeAt(0)
        #     widget = item.widget()
        #     widget.deleteLater()

        if len(elephants) == 0:
            print "No matches"
            return 0
        print len(elephants), "match criteria"
        # Adding the pictures, and clicking on them calls show_notes
        self.update_pics_area(elephants)

    def show_notes(self, lb):
        e = self.picture_elephants[lb]
        print "EID: ", e.getID()
        print "NOTES:", e.getNotes()
        # print e.getPhotos()
        # print e.getFeatures()

    def filter_elephants(self):
        root = self.model.invisibleRootItem() # get model properly?
        filter_values= {}
        i = 0
        while True:
            item = root.child(i)
            if item is None:
                break
            feature = str(item.text())
            filter_values[feature] = []
            v = 0
            while True:
                value = item.child(v)
                if value is None:
                    break
                state = ['UNCHECKED', 'TRISTATE',  'CHECKED'][value.checkState()]
                #print state
                if state=='CHECKED':
                    filter_values[feature].append(str(value.text()))
                v += 1
            i += 1
        filtered_elephants = self.herd.filterLoose(filter_values, 0) # <<<<<<< Change to 0 to do strict filter
        self.update_herd(filtered_elephants)

# The main loop - run if we directly run this file.
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = EID_FORM(SPREADSHEET, SHEETNUM, PHOTODIR)
    myapp.show()
    sys.exit(app.exec_())

#root.mainloop()
