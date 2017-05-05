# App for rapid photo identification of elephants
# Copyright (c) 2016 Jonathan Whitaker, johnowhitaker@gmail.com
# Licenced under the GPL, available at https://www.gnu.org/licenses/gpl-3.0.en.html

import glob, xlrd, os, sys, re
from PyQt4 import QtCore, QtGui
from eid_mainwindow import Ui_MainWindow
from einfo_dialog import Ui_Dialog
from collections import OrderedDict
import exifread
import argparse


#************************************************************************************
#   THE IMPORTANT BITS - WILL ADD OTHER PARAMETERS HERE FOR EASY CONFIGURATION     **
#************************************************************************************
# NB - These are overwritten by config.py, so rather edit there. Here just in case
# config.py is not present.
SPREADSHEET = "/home/jonathan/Elephant_MAY/raw_data/Elephants.xlsx"
SHEETNUM = 0
PHOTODIR = "/home/jonathan/Elephant_MAY/HIP_ID_PHOTOS_TIM_MAY"
VERBOSE = False
SCALE_SMALLS = False
SHOW_EXIF_DATA = False

GENERATE_SMALLS = False

DEFAULT_ORDER = ''

MAIN_WINDOW_SIZE = (1200, 800)
PHOTO_SIZE = 600


E_INSPECTOR_SIZE = (1200, 800)


if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
elif __file__:
    application_path = os.path.dirname(__file__)

execfile(application_path+"/config.py")

#######################################################################################

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
        self.features = OrderedDict()
        self.notes = OrderedDict()
        self.photos = []#glob.glob(self.photo_folder+"/*.jpg")
        self.mismatches = 0
        self.hidden = False # Allow hiding the elephants

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
        self.possible_values = OrderedDict([(f, []) for f in self.features])
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
                if not "*" in heading: # Add a * to a heading for special treatment <<<<<<<<< Add a photo folder option here <<<<<<
                    e.setFeature(str(heading), val)
                else:
                    e.setNote(str(heading), val)
                column +=1
            # :( don't like this - will be fixed if we add a photo folder column (we should)
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

    # Not currently using this as we decided '*' worked better.
    # def filterLoose(self, constraints, n):
    #     self.filter(constraints)
    #     self.sorted_elephants = [e for e in self.filtered_elephants]
    #     near = 0
    #     for i in range(n):
    #         for e in self.elephants:
    #             if e.mismatches == n:
    #                 self.sorted_elephants.append(e)
    #                 near += 1
    #     print "including "+str(near)+" near misses"
    #     return self.sorted_elephants

    def clearFilters():
        for e in self.elephants:
            e.hidden = False # Un-hide all
        self.filtered_elephants = [e for e in self.elephants]

#######################################################################################
# The GUI side of things, currently holding most of the logic

# The main window - criteria on the left and pics on the right.
class EID_MAINWINDOW(QtGui.QMainWindow):

    picture_elephants = OrderedDict()
    photo_height = PHOTO_SIZE

    def __init__(self, spreadsheet, sheet_num,  photo_folder, parent=None):
        # UI from designer
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # For info on specific ellies (separate window opened on click)
        self.e_info_diag = E_INFO_DIALOG(self)
        self.selected_e = None

        # Where the elephants are stored
        self.herd = Herd(spreadsheet, sheet_num, photo_folder)

        self.n_filtered = len(self.herd.getElephants())
        self.n_hidden = 0

        # Connect buttons to appropriate functions
        self.ui.btn_apply_filter.clicked.connect(self.filterClicked)
        self.ui.btn_clear_filter.clicked.connect(self.clearFilters)
        self.ui.btn_reorder_pics.clicked.connect(self.show_text_filtered_images)
        self.ui.btn_hide_all.clicked.connect(self.hide_all)
        self.ui.btn_unhide_all.clicked.connect(self.unhide_all)
        self.ui.btn_load_target.clicked.connect(self.load_target)

        # Menu
        self.statusBar()
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        #zoom in
        exitAction = QtGui.QAction('&Zoom In', self)
        exitAction.setShortcut('Ctrl+K')
        exitAction.setStatusTip('Zoom in on potential matches')
        exitAction.triggered.connect(self.zoom_in_images)
        fileMenu.addAction(exitAction)
        #zoom out
        exitAction = QtGui.QAction('&Zoom Out', self)
        exitAction.setShortcut('Ctrl+J')
        exitAction.setStatusTip('Zoom out on potential matches')
        exitAction.triggered.connect(self.zoom_out_images)
        fileMenu.addAction(exitAction)
        #exit
        exitAction = QtGui.QAction(QtGui.QIcon('exit.png'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(QtGui.qApp.quit)
        fileMenu.addAction(exitAction)
        self.load_herd(self.herd.getElephants())
        self.statusBar().showMessage("Displaying "+str(self.n_filtered) + " matches")
        self.resize(1200, 800) ## Starting with a fixed size for now. <<<<<<<<<<<<<<<<<<<<<<<<<<<<<< FIX TO USE MAIN_WINDOW_SIZE!!<<<<<<<

        if GENERATE_SMALLS:
            print "Generating smalls - may take some time if this is the first run"
            self.pic = QtGui.QLabel()
            for e in self.herd.getElephants():
                for p in e.photos:
                    outfile = p+ ".small"
                    if p != outfile and not os.path.exists(outfile):
                        try:
                            pixmap = QtGui.QPixmap(p)
                            pixmap_resized = pixmap.scaled(PHOTO_SIZE, PHOTO_SIZE, QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.SmoothTransformation)
                            pixmap_resized.save(outfile, "JPEG")
                            print "Saved: ", outfile
                        except IOError:
                            print "cannot create thumbnail for '%s'" % p

        self.init_picture_area(self.herd.getElephants()) # this should be in load herd?
    # GO through every item in the tree view and set to un-checked. Doeasn't apply filter
    # Also unhides any hidden elephants
    def clearFilters(self, btn):
        root = self.model.invisibleRootItem() # get model properly?
        filter_values= OrderedDict()
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
        self.unhide_all("not_a_button")

    #Ignore - UI stuff. Allows labels to be clickable
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

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Escape:
            self.close()
        else:
            print e.key()

    # Run when the "Apply Filter" button is clicked
    def filterClicked(self, btn):
        print "Applying filter"
        self.filter_elephants()

    # Loads data from a spreadsheet into a herd, and create the filter options.
    def load_herd(self, elephants):
        # Loading the data
        features = elephants[0].features.keys()
        possible_values = OrderedDict([(f, []) for f in features])
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

    # Inefficient, and struggles with large images apparetly << fixed? Yup :) This comment kept for entertainment
    def update_pics_area(self, elephants):
        print "updating picture area"
        for widget in self.picture_elephants:
            e = self.picture_elephants[widget]
            keeping = False
            for ellie in elephants:
                if (ellie.getID() == e.getID()) and not ellie.hidden:
                    keeping = True
                    break
            if keeping:
                widget.parent().show()
            else:
                widget.parent().hide()
        self.statusBar().showMessage("%i Matches "%self.n_filtered + " (%i hidden)" % self.n_hidden)

    #Adding the pictures, and clicking on them calls show_notes
    def init_picture_area(self, elephants):
        for e in elephants:
            g = QtGui.QWidget()
            lay = QtGui.QHBoxLayout()
            g.setLayout(lay)
            small = False
            if len(e.small_photos)!=0:
                small = True
            elif len(e.photos)!=0:
                e.small_photos = e.photos
            #print e.small_photos

            #Uncomment this for a name before each pic
            # lb1 = QtGui.QLabel(e.getID())
            # self.picture_elephants[lb1] = e
            # self.clickable(lb1).connect(self.show_notes)
            # g.layout().addWidget(lb1)

            # Put smallest pic (usually template) first. Dont use
            # for i in range(len(pics)):
            #     p = pics[i]
            #     if os.stat(p).st_size<os.stat(pics[0]).st_size:
            #         pics[0], pics[i] = pics[i], pics[0]

            for p in e.small_photos:
                lb = QtGui.QLabel()
                if not small:
                    lb.setGeometry(10, 10, PHOTO_SIZE, PHOTO_SIZE)
                    lb.setPixmap(QtGui.QPixmap(p).scaled(lb.size(), QtCore.Qt.KeepAspectRatio))
                else:
                    if SCALE_SMALLS:
                        lb.setGeometry(10, 10, PHOTO_SIZE, PHOTO_SIZE)
                        lb.setPixmap(QtGui.QPixmap(p).scaled(lb.size(), QtCore.Qt.KeepAspectRatio,transformMode=QtCore.Qt.SmoothTransformation))
                    else:
                        lb.setPixmap(QtGui.QPixmap(p)) # Whatever size the smalls are. Speeds up startup

                lb.setToolTip(str(e.small_photos.index(p))) # Used for keeping track of which image is which << Try without now that main issue fixed?
                #Overlay the elephant name and optionally date taken
                lb1 = QtGui.QLabel(lb) # Using a label as a frame - not the best idea but functional.
                lb1.setText(e.getID())
                if SHOW_EXIF_DATA:
                    f = open(p[:-6], 'rb') # use the large images
                    tags = exifread.process_file(f) #Investigate piexif ?
                    date = ''
                    if 'EXIF DateTimeDigitized' in tags.keys():
                        date = str(tags['EXIF DateTimeDigitized'])
                    lb1.setText(e.getID() + " - " +date)
                lb1.setStyleSheet("QLabel { background-color : white; color : black; }")

                g.layout().addWidget(lb)
                self.picture_elephants[lb] = e
                self.clickable(lb).connect(self.show_notes)
            lay.addStretch(1)
            self.ui.scrlw.layout().addWidget(g)

    # Let the user enter a string. If there is an image with that in it's name it appears first.
    def show_text_filtered_images(self, w): # currently not working
        btn = QtGui.QPushButton("Open Input Dialog")
        text, result = QtGui.QInputDialog.getText(self, "Re-order images", "Enter text filter")
        if result:
            print "Reordering images: \"" + text + "\""
            for e in self.herd.getElephants():
                index = 0
                for pic in e.photos:
                    if text in pic:
                        index = e.photos.index(pic)
                        break
                if index != 0:
                    print e.getID(), index
                    e.photos[0], e.photos[0+index] = e.photos[0+index], e.photos[0]
                index = 0
                for pic in e.small_photos:
                    if text in pic:
                        index = e.small_photos.index(pic)
                        break
                if index != 0:
                    print e.getID(), index
                    e.small_photos[0], e.small_photos[0+index] = e.small_photos[0+index], e.small_photos[0]
            for i in reversed(range(self.ui.scrlw.layout().count())):
                self.ui.scrlw.layout().itemAt(i).widget().setParent(None)
            self.picture_elephants = {}
            self.init_picture_area(self.herd.getElephants())

    def update_herd(self, elephants):
        if len(elephants) == 0:
            print "No matches"
            return 0
        print len(elephants), "match criteria"
        self.update_pics_area(elephants)

    def show_notes(self, lb):
        #print int(lb.toolTip())
        e = self.picture_elephants[lb]
        pic_num = int(lb.toolTip())
        #print e.small_photos
        # for label in lb.parent().children(): <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<!!!!!!!!!
        #     if label == lb:
        #         pic_num = lb.parent().children().index(lb)-1
        #         break
        print "Examining EID: ", e.getID()
        self.selected_e = e
        self.e_info_diag.setElephant(e, pic_num)
        self.e_info_diag.exec_()

    def scaleImages(self, width, height):
        for lb in self.picture_elephants.keys(): #the labels with pictures
            lb.setPixmap(lb.pixmap().scaled(height, height, QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.SmoothTransformation))

    def zoom_in_images(self):
        self.photo_height += 100
        self.scaleImages(self.photo_height, self.photo_height)

    def zoom_out_images(self):
        self.photo_height -= 100
        self.scaleImages(self.photo_height, self.photo_height)

    def filter_elephants(self):
        print "filtering elephants"
        root = self.model.invisibleRootItem() # get model properly?
        filter_values= OrderedDict()
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
        filtered_elephants = self.herd.filter(filter_values)
        self.n_filtered = len(filtered_elephants)
        self.n_hidden = 0
        for e in filtered_elephants:
            if e.hidden:
                self.n_hidden += 1
        self.update_herd(filtered_elephants)

    def hide_all(self, btn): #Hides all currently visible elephants (i.e. all matches)
        print "Hiding all"
        for widget in self.picture_elephants:
            for ellie in self.herd.filtered_elephants:
                if (ellie.getID() == self.picture_elephants[widget].getID()):
                    self.picture_elephants[widget].hidden = True
        print "Filtering"
        self.filter_elephants()

    def unhide_all(self, btn):
        for e in self.herd.elephants:
            e.hidden=False
        self.filter_elephants()

    def load_target(self, btn): # A separate pic, of the target we're trying to identify
        fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file', PHOTODIR,"Image files (*.jpg *.png)")
        #self.ui.label_target_text.setText(fname)
        self.ui.label_target.setGeometry(10, 10, PHOTO_SIZE, PHOTO_SIZE)
        pixmap = QtGui.QPixmap(fname)
        scaled_pixmap = pixmap.scaled(PHOTO_SIZE, PHOTO_SIZE, QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.SmoothTransformation)
        self.ui.label_target.setPixmap(scaled_pixmap)


# On clicking a picture, this window pops up
class E_INFO_DIALOG(QtGui.QDialog):
    elephant = None
    def __init__(self, parent=None):
        super(E_INFO_DIALOG, self).__init__(parent)
        self.ui = Ui_Dialog()

        self.ui.setupUi(self)


        self.splitter = QtGui.QSplitter()
        self.ui.horizontalLayout.addWidget(self.splitter)
        self.viewer = PhotoViewer(self)
        self.splitter.addWidget(self.viewer)
        self.textBrowser = QtGui.QTextBrowser()
        self.splitter.addWidget(self.textBrowser)
        self.splitter.setSizes([1000, 200])

        self.resize(1200, 800)
        self.setGeometry(PHOTO_SIZE, 0, 1200, 800)

        self.ui.btn_next.clicked.connect(self.next)
        self.ui.btn_hide.clicked.connect(self.hide)

        self.pic_num = 0
        if self.elephant != None:
            self.setElephant(self.elephant)
        self.viewer.fitInView()

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Escape:
            self.close()
        elif e.key() == QtCore.Qt.Key_N:
            self.next("not_a_button") #yuk :)

    def next(self, btn): # Go to the next pic of this elephant
        self.pic_num += 1
        if len(self.elephant.photos) <= self.pic_num:
            self.pic_num = 0
        self.setPhoto(self.elephant.photos[self.pic_num])

    def prev(self): # Go to the next pic of this elephant not used
        self.pic_num -= 1
        if 0 > self.pic_num:
            self.pic_num = len(self.elephant.photos)
        self.setPhoto(self.elephant.photos[self.pic_num])

    def hide(self, btn): #hide the elephant we're currently looking at, and exit
        self.elephant.hidden = True
        self.parent().filter_elephants()
        self.close()

    def setElephant(self, e, pic_num):
        self.elephant = e
        self.setWindowTitle(e.getID())
        self.pic_num = pic_num
        self.setPhoto(e.small_photos[self.pic_num][:-6]) # for some reason, small photos order is right but not photos order. Sowe deduce the name from the small (-last six chars)
        notes = OrderedDict()
        for n in e.getNotes():
            notes[n] = e.getNotes()[n]
        for f in e.features:
            notes[f] = e.getFeature(f)
        self.setNotes(notes)

    def setPhoto(self, p):
        self.viewer.setPhoto(QtGui.QPixmap(p))
        self.viewer.fitInView()
    def setNotes(self, n):
        self.textBrowser.setText("")
        for note in n:
            self.textBrowser.append(note +": "+ n[note] + "\n")

## This class taken from stackoverflow, user ekhumoro, and edited a little
class PhotoViewer(QtGui.QGraphicsView):
    def __init__(self, parent):
        super(PhotoViewer, self).__init__(parent)
        self._zoom = 0
        self._scene = QtGui.QGraphicsScene(self)
        self._photo = QtGui.QGraphicsPixmapItem()
        self._scene.addItem(self._photo)
        self.setScene(self._scene)
        self.setTransformationAnchor(QtGui.QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QtGui.QGraphicsView.AnchorUnderMouse)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setBackgroundBrush(QtGui.QBrush(QtGui.QColor(30, 30, 30)))
        self.setFrameShape(QtGui.QFrame.NoFrame)

    def fitInView(self):
        rect = QtCore.QRectF(self._photo.pixmap().rect())
        if not rect.isNull():
            unity = self.transform().mapRect(QtCore.QRectF(0, 0, 1, 1))
            self.scale(1 / unity.width(), 1 / unity.height())
            viewrect = self.viewport().rect()
            scenerect = self.transform().mapRect(rect)
            factor = min(viewrect.width() / scenerect.width(),
                         viewrect.height() / scenerect.height())
            self.scale(factor, factor)
            self.centerOn(rect.center())
            self._zoom = 0

    def setPhoto(self, pixmap=None):
        self._zoom = 0
        if pixmap and not pixmap.isNull():
            self.setDragMode(QtGui.QGraphicsView.ScrollHandDrag)
            self._photo.setPixmap(pixmap)
            self.fitInView()
        else:
            self.setDragMode(QtGui.QGraphicsView.NoDrag)
            self._photo.setPixmap(QtGui.QPixmap())

    def zoomFactor(self):
        return self._zoom

    def zoom(self, f): #<< I added this
        self._zoom += f

    def wheelEvent(self, event):
        if not self._photo.pixmap().isNull():
            if event.delta() > 0:
                factor = 1.25
                self._zoom += 1
            else:
                factor = 0.8
                self._zoom -= 1
            if self._zoom > 0:
                self.scale(factor, factor)
            elif self._zoom == 0:
                self.fitInView()
            else:
                self._zoom = 0

# The main loop - run if we directly run this file.
if __name__ == "__main__":

    # Parse comand line arguments - work in progress
    parser = argparse.ArgumentParser(description='Elephantphotoidentification app')
    parser.add_argument('-d', '--data', nargs='?', help='Spreadsheet or .csv')
    parser.add_argument('-s', '--sheetnum', nargs='?', help='Only if using spreadsheet')
    parser.add_argument('-p', '--photodir', nargs='?', help='Base folder with photos')
    parser.add_argument('-w', '--windowsize', nargs='?', help='Size of the main window (X, Y)')
    parser.add_argument('-v', '--verbose', help='increase output verbosity', action='store_true')
    args = parser.parse_args(sys.argv[1:])
    PHOTODIR = args.photodir if (args.photodir != None) else PHOTODIR
    SPREADSHEET = args.data if args.data != None else SPREADSHEET
    SHEETNUM = int(args.sheetnum) if args.sheetnum != None else SHEETNUM
    MAIN_WINDOW_SIZE = tuple(int(v) for v in re.findall("[0-9]+", args.windowsize)) if args.windowsize != None else MAIN_WINDOW_SIZE
    VERBOSE = args.verbose

    # If -v, show starting PARAMETERS
    if VERBOSE:
        print "Starting pachydentify..."
        print "Using data", SPREADSHEET
        print "Using photos in", PHOTODIR

    # Start the app
    app = QtGui.QApplication(sys.argv)
    myapp = EID_MAINWINDOW(SPREADSHEET, SHEETNUM, PHOTODIR)
    myapp.show()
    sys.exit(app.exec_())



    #self.ui.statusBar().showMessage("Hello")
