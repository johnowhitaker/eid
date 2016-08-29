# Playing around loading ellie data.
# python3-tk, python3-xlrd


import glob, xlrd, os

class Elephant:

    def __init__(self):
        #self.photo_folder = photof
        self.photo_folder = ""#"../photos/BH003"
        self.photos = []
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
        #self.photos = glob.glob(self.photo_folder+ext)
        for ext in ['*.gif', '*.png', '*.jpg', '*.JPG', '*.JPEG', '*.jpeg']:
            self.photos.extend(glob.glob(self.photo_folder+'/'+ext))

    def getPhotos(self):
        return self.photos

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
        while row<sheet.nrows: # Column 0 is the elephant ID. If it's empty, we've reached the end
            # Next elephant (next row)
            e = Elephant()
            e.setID(sheet.cell(row, 0).value)
            e.setPhotoFolder(photo_folder)
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
            #print os.getcwd() + "/photos/" + e.getID().upper()
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
        self.filtered_elephants = []
        for e in self.elephants:
            e.zeroMismatches()
            for f in constraints.keys():
                if not ((e.getFeature(f) in constraints[f]) or constraints[f] == ""):
                        e.incMismatches()
            if e.getMisMatches() == 0:
                self.filtered_elephants.append(e)
        return self.filtered_elephants

    def filterLoose(self, constraints, n):
        self.filter(constraints)
        self.sorted_elephants = [e for e in self.filtered_elephants]
        for i in range(n):
            for e in self.elephants:
                if e.getMisMatches() == n:
                    self.sorted_elephants.append(e)
        return self.sorted_elephants

    def clearFilters():
        self.filtered_elephants = [e for e in self.elephants]

import sys
from PyQt4 import QtCore, QtGui
from test_ui import Ui_Form


class EID_FORM(QtGui.QWidget):

    piclabs = {}
    cb_filters = {}
    filter_values = {}
    pic_area_widgets = [] # Cheap late night hack - fix

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


    def clearFilters(self, btn):
        for cb in self.cb_filters:
            cb.setCurrentIndex(0)
        self.filter_elephants()

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

    def filterClicked(self, btn):
        self.filter_elephants()

    def load_herd(self, elephants):
        # Loading the data
        features = elephants[0].getFeatures().keys()
        possible_values = {f:[] for f in features}
        # for each feature, possible values has a corresponding list of values that feature can take on
        for f in features:
            possible_values[f].append("")
            for e in elephants:
                if e.getFeature(f) not in possible_values[f]:
                     possible_values[f].append(e.getFeature(f))
        #print possible_values['age']
        print "loading: " + str(len(elephants))

        #Clear the UI
        while self.ui.scrlw.layout().count():
            item = self.ui.scrlw.layout().takeAt(0)
            widget = item.widget()
            widget.deleteLater()

        # making the comboboxes for now
        for f in features:
            lb = QtGui.QLabel(f + ":")
            cb = QtGui.QComboBox()
            for p in possible_values[f]:
                cb.addItem(p)
            self.cb_filters[cb] = f
            g = QtGui.QWidget()
            g.setLayout(QtGui.QHBoxLayout())
            g.layout().addWidget(lb)
            g.layout().addWidget(cb)
            self.ui.scrlw_features.layout().addWidget(g)
        self.update_pics_area(elephants)

    def update_pics_area(self, elephants):
        print "updating picture area"
        #Clear the UI
        while self.ui.scrlw.layout().count():
            item = self.ui.scrlw.layout().takeAt(0)
            widget = item.widget()
            widget.deleteLater()
        # Adding the pictures, and clicking on them calls show_notes
        for e in elephants:
            lb1 = QtGui.QLabel(e.getID())
            g = QtGui.QWidget()
            g.setLayout(QtGui.QHBoxLayout())
            g.layout().addWidget(lb1)
            self.piclabs[lb1] = e
            self.clickable(lb1).connect(self.show_notes)
            for p in e.getPhotos():
                lb = QtGui.QLabel()
                lb.setGeometry(10, 10, 400, 400)
                lb.setPixmap(QtGui.QPixmap(p).scaled(lb.size(), QtCore.Qt.KeepAspectRatio))
                g.layout().addWidget(lb)
                self.piclabs[lb] = e
                self.clickable(lb).connect(self.show_notes)
            self.ui.scrlw.layout().addWidget(g)
            self.pic_area_widgets.append(g)

    def update_herd(self, elephants):

        #Clear the UI
        while self.ui.scrlw.layout().count():
            item = self.ui.scrlw.layout().takeAt(0)
            widget = item.widget()
            widget.deleteLater()
        if len(elephants) == 0:
            print "No matches"
            return 0
        print len(elephants), "match criteria"
        # Adding the pictures, and clicking on them calls show_notes
        self.update_pics_area(elephants)

    def show_notes(self, lb):
        e = self.piclabs[lb]
        # print e.getID()
        # print e.getNotes()
        # print e.getPhotos()
        print e.getFeatures()

    def filter_elephants(self):
        self.filter_values = {}
        for cb in self.cb_filters:
            self.filter_values[self.cb_filters[cb]] = cb.currentText()
            #print self.filter_values[self.cb_filters[cb]], cb.currentText()
        filtered_elephants = self.herd.filter(self.filter_values) #<<<<<<<<<<<<<<<<<<<<<<<<
        self.update_herd(filtered_elephants)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = EID_FORM(os.getcwd() + "/elephants.xlsx", 3, os.getcwd()+"/photos")
    myapp.show()
    sys.exit(app.exec_())

root.mainloop()


# Some old code
#
# class MyForm(QtGui.QWidget):
#
#     piclabs = {}
#     elephants = []
#     cb_filters = {}
#     filter_values = {}
#
#     def __init__(self, parent=None):
#         # UI from designer
#         QtGui.QWidget.__init__(self, parent)
#         self.ui = Ui_Form()
#         self.ui.setupUi(self)
#
#         self.elephants = load_from_spreadsheet('/home/jonathan/Projects/Ellie/elephants.xlsx', 3)
#
#         # Connect btn_load_herd to function
#         self.ui.btn_load_herd.clicked.connect(self.filterClicked)
#         self.load_herd(self.elephants)
#
#
#
#     def clickable(self, widget):
#         class Filter(QtCore.QObject):
#             clicked = QtCore.pyqtSignal(QtGui.QWidget)
#             def eventFilter(self, obj, event):
#
#                 if obj == widget:
#                     if event.type() == QtCore.QEvent.MouseButtonRelease:
#                         if obj.rect().contains(event.pos()):
#                             self.clicked.emit(obj)
#                             # The developer can opt for .emit(obj) to get the object within the slot.
#                             return True
#
#                 return False
#         filter = Filter(widget)
#         widget.installEventFilter(filter)
#         return filter.clicked
#
#     def filterClicked(self, btn):
#         self.filter_elephants()
#
#     def load_herd(self, elephants):
#         # Loading the data
#         features = elephants[0].getFeatures().keys()
#         possible_values = {f:[] for f in features}
#         # for each feature, possible values has a corresponding list of values that feature can take on
#         for f in features:
#             possible_values[f].append("")
#             for e in elephants:
#                 if e.getFeature(f) not in possible_values[f]:
#                      possible_values[f].append(e.getFeature(f))
#         #print possible_values['age']
#         print "loading: " + self.ui.txt_open_path.text() + str(len(elephants))
#
#         #Clear the UI
#         while self.ui.scrlw.layout().count():
#             item = self.ui.scrlw.layout().takeAt(0)
#             widget = item.widget()
#             # if widget has some id attributes you need to
#             # save in a list to maintain order, you can do that here
#             # i.e.:   aList.append(widget.someId)
#             widget.deleteLater()
#
#         # making the comboboxes for now
#         for f in features:
#             lb = QtGui.QLabel(f + ":")
#             cb = QtGui.QComboBox()
#             for p in possible_values[f]:
#                 cb.addItem(p)
#             self.cb_filters[cb] = f
#             g = QtGui.QWidget()
#             g.setLayout(QtGui.QHBoxLayout())
#             g.layout().addWidget(lb)
#             g.layout().addWidget(cb)
#             self.ui.scrlw_features.layout().addWidget(g)
#
#         # Adding the pictures, and clicking on them calls show_notes
#         for e in elephants:
#             lb = QtGui.QLabel()
#             if e.getPhotos() != []:
#                 lb.setGeometry(10, 10, 400, 400)
#                 lb.setPixmap(QtGui.QPixmap(e.getPhotos()[0]).scaled(lb.size(), QtCore.Qt.KeepAspectRatio)) #<<<<<<<< Add others
#             else:
#                 lb.setText(e.getID())
#             self.piclabs[lb] = e
#             self.clickable(lb).connect(self.show_notes)
#             self.ui.scrlw.layout().addWidget(lb)
#
#     def update_herd(self, elephants):
#
#         #Clear the UI
#         while self.ui.scrlw.layout().count():
#             item = self.ui.scrlw.layout().takeAt(0)
#             widget = item.widget()
#             widget.deleteLater()
#         if len(elephants) == 0:
#             print "No matches"
#             return 0
#         # Adding the pictures, and clicking on them calls show_notes
#         for e in elephants:
#             lb = QtGui.QLabel()
#             if e.getPhotos() != []:
#                 lb.setGeometry(10, 10, 400, 400)
#                 lb.setPixmap(QtGui.QPixmap(e.getPhotos()[0]).scaled(lb.size(), QtCore.Qt.KeepAspectRatio))
#             else:
#                 lb.setText(e.getID())
#             self.piclabs[lb] = e
#             self.clickable(lb).connect(self.show_notes)
#             self.ui.scrlw.layout().addWidget(lb)
#
#     def show_notes(self, lb):
#         e = self.piclabs[lb]
#         print e.getNotes()
#
#     def filter_elephants(self):
#         filtered_elephants = []
#         for cb in self.cb_filters:
#             self.filter_values[self.cb_filters[cb]] = cb.currentText()
#         print "sorting by:"
#         for f in self.filter_values:
#             print f + ":____ " + self.filter_values[f]
#         for e in self.elephants:
#             passed = True
#             for f in self.filter_values:
#                 if self.filter_values[f] != "":
#                     if e.getFeature(f) != self.filter_values[f]:
#                         passed = False
#             if passed:
#                 filtered_elephants.append(e)
#         print "Filtered to: " + str(len(filtered_elephants))
#         self.update_herd(filtered_elephants)
