# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1097, 823)
        self.Open_Button = QtWidgets.QPushButton(Form)
        self.Open_Button.setGeometry(QtCore.QRect(940, 400, 131, 28))
        self.Open_Button.setObjectName("Open_Button")
        self.BackGround = QtWidgets.QLabel(Form)
        self.BackGround.setGeometry(QtCore.QRect(-10, -5, 1131, 851))
        self.BackGround.setText("")
        self.BackGround.setPixmap(QtGui.QPixmap("../Task 1/simple-gray-abstract-background-wi.jpg"))
        self.BackGround.setObjectName("BackGround")
        self.Display_1 = QtWidgets.QLabel(Form)
        self.Display_1.setGeometry(QtCore.QRect(60, 20, 321, 331))
        self.Display_1.setText("")
        self.Display_1.setAlignment(QtCore.Qt.AlignCenter)
        self.Display_1.setObjectName("Display_1")
        self.Display_2 = QtWidgets.QLabel(Form)
        self.Display_2.setGeometry(QtCore.QRect(530, 20, 321, 331))
        self.Display_2.setText("")
        self.Display_2.setAlignment(QtCore.Qt.AlignCenter)
        self.Display_2.setObjectName("Display_2")
        self.Display_3 = QtWidgets.QLabel(Form)
        self.Display_3.setGeometry(QtCore.QRect(60, 430, 321, 331))
        self.Display_3.setText("")
        self.Display_3.setAlignment(QtCore.Qt.AlignCenter)
        self.Display_3.setObjectName("Display_3")
        self.horizontalSlider_2 = QtWidgets.QSlider(Form)
        self.horizontalSlider_2.setGeometry(QtCore.QRect(70, 370, 311, 22))
        self.horizontalSlider_2.setMaximum(100)
        self.horizontalSlider_2.setPageStep(50)
        self.horizontalSlider_2.setSliderPosition(50)
        self.horizontalSlider_2.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_2.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.horizontalSlider_2.setObjectName("horizontalSlider_2")
        self.verticalSlider_2 = QtWidgets.QSlider(Form)
        self.verticalSlider_2.setGeometry(QtCore.QRect(400, 40, 22, 301))
        self.verticalSlider_2.setMaximum(100)
        self.verticalSlider_2.setPageStep(50)
        self.verticalSlider_2.setProperty("value", 50)
        self.verticalSlider_2.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider_2.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.verticalSlider_2.setObjectName("verticalSlider_2")
        self.Display_4 = QtWidgets.QLabel(Form)
        self.Display_4.setGeometry(QtCore.QRect(530, 430, 321, 331))
        self.Display_4.setText("")
        self.Display_4.setAlignment(QtCore.Qt.AlignCenter)
        self.Display_4.setObjectName("Display_4")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(200, 400, 41, 21))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(670, 400, 41, 21))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(200, 800, 41, 21))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(680, 790, 41, 21))
        self.label_4.setObjectName("label_4")
        self.horizontalSlider_3 = QtWidgets.QSlider(Form)
        self.horizontalSlider_3.setGeometry(QtCore.QRect(500, 370, 311, 22))
        self.horizontalSlider_3.setMaximum(100)
        self.horizontalSlider_3.setPageStep(50)
        self.horizontalSlider_3.setSliderPosition(50)
        self.horizontalSlider_3.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_3.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.horizontalSlider_3.setObjectName("horizontalSlider_3")
        self.horizontalSlider_4 = QtWidgets.QSlider(Form)
        self.horizontalSlider_4.setGeometry(QtCore.QRect(70, 760, 311, 22))
        self.horizontalSlider_4.setMaximum(100)
        self.horizontalSlider_4.setPageStep(50)
        self.horizontalSlider_4.setSliderPosition(50)
        self.horizontalSlider_4.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_4.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.horizontalSlider_4.setObjectName("horizontalSlider_4")
        self.verticalSlider_3 = QtWidgets.QSlider(Form)
        self.verticalSlider_3.setGeometry(QtCore.QRect(830, 40, 22, 301))
        self.verticalSlider_3.setMaximum(100)
        self.verticalSlider_3.setPageStep(50)
        self.verticalSlider_3.setProperty("value", 50)
        self.verticalSlider_3.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider_3.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.verticalSlider_3.setObjectName("verticalSlider_3")
        self.verticalSlider_4 = QtWidgets.QSlider(Form)
        self.verticalSlider_4.setGeometry(QtCore.QRect(400, 460, 22, 301))
        self.verticalSlider_4.setMaximum(100)
        self.verticalSlider_4.setPageStep(50)
        self.verticalSlider_4.setProperty("value", 50)
        self.verticalSlider_4.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider_4.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.verticalSlider_4.setObjectName("verticalSlider_4")
        self.BackGround.raise_()
        self.Open_Button.raise_()
        self.Display_1.raise_()
        self.Display_2.raise_()
        self.Display_3.raise_()
        self.horizontalSlider_2.raise_()
        self.verticalSlider_2.raise_()
        self.Display_4.raise_()
        self.label.raise_()
        self.label_2.raise_()
        self.label_3.raise_()
        self.label_4.raise_()
        self.horizontalSlider_3.raise_()
        self.horizontalSlider_4.raise_()
        self.verticalSlider_3.raise_()
        self.verticalSlider_4.raise_()

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.Open_Button.setText(_translate("Form", "Browse Dicom File"))
        self.label.setText(_translate("Form", "Axial"))
        self.label_2.setText(_translate("Form", "Coronal"))
        self.label_3.setText(_translate("Form", "Sagital"))
        self.label_4.setText(_translate("Form", "Oblique"))
