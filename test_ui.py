# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test.ui'
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

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("TimAndJohnoHaveAnAdventure"))
        Form.resize(656, 462)
        self.gridLayout_3 = QtGui.QGridLayout(Form)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.splitter = QtGui.QSplitter(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.widget = QtGui.QWidget(self.splitter)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.gridLayout_2 = QtGui.QGridLayout(self.widget)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.btn_load_herd = QtGui.QPushButton(self.widget)
        self.btn_load_herd.setObjectName(_fromUtf8("btn_load_herd"))
        self.gridLayout_2.addWidget(self.btn_load_herd, 0, 2, 1, 1)
        self.btn_apply_filter = QtGui.QPushButton(self.widget)
        self.btn_apply_filter.setObjectName(_fromUtf8("btn_apply_filter"))
        self.gridLayout_2.addWidget(self.btn_apply_filter, 0, 4, 1, 1)
        self.btn_clear_filter = QtGui.QPushButton(self.widget)
        self.btn_clear_filter.setObjectName(_fromUtf8("btn_clear_filter"))
        self.gridLayout_2.addWidget(self.btn_clear_filter, 0, 3, 1, 1)
        self.scrl_features = QtGui.QScrollArea(self.widget)
        self.scrl_features.setWidgetResizable(True)
        self.scrl_features.setObjectName(_fromUtf8("scrl_features"))
        self.scrlw_features = QtGui.QWidget()
        self.scrlw_features.setGeometry(QtCore.QRect(0, 0, 473, 407))
        self.scrlw_features.setObjectName(_fromUtf8("scrlw_features"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.scrlw_features)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.treeView = QtGui.QTreeView(self.scrlw_features)
        self.treeView.setObjectName(_fromUtf8("treeView"))
        self.horizontalLayout.addWidget(self.treeView)
        self.scrl_features.setWidget(self.scrlw_features)
        self.gridLayout_2.addWidget(self.scrl_features, 1, 0, 1, 6)
        self.scrollArea = QtGui.QScrollArea(self.splitter)
        self.scrollArea.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setMinimumSize(QtCore.QSize(100, 100))
        self.scrollArea.setAutoFillBackground(True)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.scrlw = QtGui.QWidget()
        self.scrlw.setGeometry(QtCore.QRect(0, 0, 153, 442))
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

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.btn_load_herd.setText(_translate("Form", "PB3", None))
        self.btn_apply_filter.setText(_translate("Form", "Apply FIlter", None))
        self.btn_clear_filter.setText(_translate("Form", "Clear Filter", None))
