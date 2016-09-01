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
from eid_mainwindow import Ui_MainWindow
from einfo_dialog import Ui_Dialog
import exifread


#************************************************************************************
#   THE IMPORTANT BITS - WILL ADD OTHER PARAMETERS HERE FOR EASY CONFIGURATION     **
#************************************************************************************
SPREADSHEET = os.getcwd() + "/../photo_id_29_aug.xlsm"
SHEETNUM = 3
PHOTODIR = os.getcwd() + "/../Cropped"

DEFAULT_ORDER = 'left'

MAIN_WINDOW_SIZE = (1200, 800)
PHOTO_HEIGHT = 400 #<< Add width?


E_INSPECTOR_SIZE = (1200, 800)


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

    def setPhotoFolder(self, folder):
        self.photo_folder = folder
        # Are these enough extensions? Who knows...
        for ext in ['*.gif', '*.png', '*.PNG', '*.jpg', '*.JPG', '*.JPEG', '*.jpeg']:
            self.photos.extend(glob.glob(self.photo_folder+'/'+ext))

    def setSmallPhotoFolder(self, folder): # merge into setPhotoFolder?
        self.small_photos = glob.glob(folder+'/*.small')
        for p in self.small_photos:
            p = p[:-6] #remove the .small part

    def getPhotos(self): # Is this needed? Or am i being a java guy?
        return self.photos

    def getSmallPhotos(self):
        return self.small_photos

    def printSelf(self):
        print(self.photos)
        for f in self.features:
            if self.features[f]!= '':
                print(f + ": " + self.features[f])

    # def showPhoto(self, n):
    #     im = Image.open(self.photos[n])
    #     im.show()

    def setFeature(self, fname, value):
        self.features[fname] = str(value)

    def getFeature(self, fname):
        return self.features[fname]

    def getFeatures(self): #?safe?
        return self.features

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

            # fix this <<<
            if os.path.isdir(photo_folder+"/" + e.getID().upper()):
                e.setSmallPhotoFolder(photo_folder+"/" + e.getID().upper())
            elif os.path.isdir(photo_folder+"/" + e.getID()):
                e.setSmallPhotoFolder(photo_folder+"/" + e.getID())

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
class EID_MAINWINDOW(QtGui.QMainWindow):

    picture_elephants = {}
    photo_height = 400

    def __init__(self, spreadsheet, sheet_num,  photo_folder, parent=None):
        # UI from designer
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # For info on specific ellies
        self.e_info_diag = E_INFO_DIALOG(self)
        self.selected_e = None

        self.herd = Herd(spreadsheet, 3, photo_folder)

        # Connect btn_load_herd to function
        self.ui.btn_apply_filter.clicked.connect(self.filterClicked)
        self.ui.btn_clear_filter.clicked.connect(self.clearFilters)
        self.ui.btn_reorder_pics.clicked.connect(self.show_text_filtered_images)

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
        self.init_picture_area(self.herd.getElephants()) # this should be in load herd?

        self.resize(1200, 800) ## Fix <<<

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

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Escape:
            self.close()
        else:
            print e.key()

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

            g = QtGui.QWidget()
            lay = QtGui.QHBoxLayout()
            g.setLayout(lay)
            pics = []
            small = False
            if len(e.getSmallPhotos())!=0:
                pics = e.getSmallPhotos()
                small = True
            elif len(e.getPhotos())!=0:
                pics = e.getPhotos()

            #Uncomment this for a name before each pic
            # lb1 = QtGui.QLabel(e.getID())
            # self.picture_elephants[lb1] = e
            # self.clickable(lb1).connect(self.show_notes)
            # g.layout().addWidget(lb1)

            # Put smallest pic (template) first
            for i in range(len(pics)):
                p = pics[i]
                if os.stat(p).st_size<os.stat(pics[0]).st_size:
                    pics[0], pics[i] = pics[i], pics[0]

            # Put left or right pic first
            text = self.ui.txt_img_filter.text()
            if text == '':
                text = DEFAULT_ORDER
            #text_appearences = 0
            for i in range(len(pics)):
                p = pics[i]
                if str(text) in str(p):
                    #text_appearences += 1
                    pics[1], pics[i] = pics[i], pics[1]

            for p in pics:
                lb = QtGui.QLabel()
                if not small:
                    lb.setGeometry(10, 10, 400, 400)
                    lb.setPixmap(QtGui.QPixmap(p).scaled(lb.size(), QtCore.Qt.KeepAspectRatio))
                else:
                    lb.setPixmap(QtGui.QPixmap(p).scaled(self.photo_height, self.photo_height, QtCore.Qt.KeepAspectRatio))
                #Overlay the elephant name and date taken
                # f = open(p, 'rb')
                # tags = exifread.process_file(f)
                date = ''
                # if 'EXIF DateTimeDigitized' in tags.keys():
                #     date = str(tags['EXIF DateTimeDigitized'])
                lb1 = QtGui.QLabel(lb) # Using a label as a frame - not the best idea but functional.
                lb1.setText(e.getID() + " - " +date)
                lb1.setStyleSheet("QLabel { background-color : white; color : black; }")

                g.layout().addWidget(lb)
                self.picture_elephants[lb] = e
                self.clickable(lb).connect(self.show_notes)
            lay.addStretch(1)
            self.ui.scrlw.layout().addWidget(g)

    def show_text_filtered_images(self, w):
        # for widget in self.picture_elephants:
        #     widget.deleteLater()
        # self.init_picture_area(self.herd.filtered_elephants)
        self.scaleImages(200, 200)

    def update_herd(self, elephants):

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
        self.selected_e = e
        self.e_info_diag.setElephant(e)
        self.e_info_diag.exec_()

    def scaleImages(self, width, height):
        #self.ui.statusBar().showMessage("Hello")
        for lb in self.picture_elephants.keys(): #the labels with pictures
            lb.setPixmap(lb.pixmap().scaled(height, height, QtCore.Qt.KeepAspectRatio))

    def zoom_in_images(self):
        self.photo_height += 100
        self.scaleImages(self.photo_height, self.photo_height)
    def zoom_out_images(self):
        self.photo_height -= 100
        self.scaleImages(self.photo_height, self.photo_height)

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
        self.setGeometry(400, 0, 1200, 800)


        self.pic_num = 0
        if self.elephant != None:
            self.setElephant(self.elephant)
        self.viewer.fitInView()

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Escape:
            self.close()
        elif e.key() == QtCore.Qt.Key_N:
            self.pic_num += 1
            if len(self.elephant.getPhotos()) <= self.pic_num:
                self.pic_num = 0
            self.setPhoto(self.elephant.getPhotos()[self.pic_num])

    def setElephant(self, e):
        self.elephant = e
        self.setWindowTitle(e.getID())
        self.setPhoto(e.getPhotos()[self.pic_num])
        self.setNotes(e.getNotes())

    def setPhoto(self, p):
        self.viewer.setPhoto(QtGui.QPixmap(p))
        self.viewer.zoom(20)
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
    app = QtGui.QApplication(sys.argv)
    myapp = EID_MAINWINDOW(SPREADSHEET, SHEETNUM, PHOTODIR)
    myapp.show()
    sys.exit(app.exec_())
