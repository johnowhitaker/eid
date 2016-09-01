# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow_EID.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(800, 600)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout_3 = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.splitter = QtGui.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.layoutWidget = QtGui.QWidget(self.splitter)
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.gridLayout_2 = QtGui.QGridLayout(self.layoutWidget)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.scrl_features = QtGui.QScrollArea(self.layoutWidget)
        self.scrl_features.setWidgetResizable(True)
        self.scrl_features.setObjectName(_fromUtf8("scrl_features"))
        self.scrlw_features = QtGui.QWidget()
        self.scrlw_features.setGeometry(QtCore.QRect(0, 0, 694, 498))
        self.scrlw_features.setObjectName(_fromUtf8("scrlw_features"))
        self.gridLayout_4 = QtGui.QGridLayout(self.scrlw_features)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.treeView = QtGui.QTreeView(self.scrlw_features)
        self.treeView.setObjectName(_fromUtf8("treeView"))
        self.gridLayout_4.addWidget(self.treeView, 0, 0, 1, 1)
        self.scrl_features.setWidget(self.scrlw_features)
        self.gridLayout_2.addWidget(self.scrl_features, 1, 0, 1, 5)
        self.txt_img_filter = QtGui.QLineEdit(self.layoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txt_img_filter.sizePolicy().hasHeightForWidth())
        self.txt_img_filter.setSizePolicy(sizePolicy)
        self.txt_img_filter.setObjectName(_fromUtf8("txt_img_filter"))
        self.gridLayout_2.addWidget(self.txt_img_filter, 0, 0, 1, 1)
        self.btn_reorder_pics = QtGui.QPushButton(self.layoutWidget)
        self.btn_reorder_pics.setMinimumSize(QtCore.QSize(10, 0))
        self.btn_reorder_pics.setObjectName(_fromUtf8("btn_reorder_pics"))
        self.gridLayout_2.addWidget(self.btn_reorder_pics, 0, 1, 1, 1)
        self.btn_clear_filter = QtGui.QPushButton(self.layoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_clear_filter.sizePolicy().hasHeightForWidth())
        self.btn_clear_filter.setSizePolicy(sizePolicy)
        self.btn_clear_filter.setObjectName(_fromUtf8("btn_clear_filter"))
        self.gridLayout_2.addWidget(self.btn_clear_filter, 0, 2, 1, 1)
        self.btn_apply_filter = QtGui.QPushButton(self.layoutWidget)
        self.btn_apply_filter.setObjectName(_fromUtf8("btn_apply_filter"))
        self.gridLayout_2.addWidget(self.btn_apply_filter, 0, 3, 1, 1)
        self.scrollArea = QtGui.QScrollArea(self.splitter)
        self.scrollArea.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setAutoFillBackground(True)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.scrlw = QtGui.QWidget()
        self.scrlw.setGeometry(QtCore.QRect(0, 0, 76, 533))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrlw.sizePolicy().hasHeightForWidth())
        self.scrlw.setSizePolicy(sizePolicy)
        self.scrlw.setObjectName(_fromUtf8("scrlw"))
        self.gridLayout = QtGui.QGridLayout(self.scrlw)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.scrollArea.setWidget(self.scrlw)
        self.gridLayout_3.addWidget(self.splitter, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.btn_reorder_pics.setText(_translate("MainWindow", "Reorder Images", None))
        self.btn_clear_filter.setText(_translate("MainWindow", "Clear Filter", None))
        self.btn_apply_filter.setText(_translate("MainWindow", "Apply FIlter", None))

