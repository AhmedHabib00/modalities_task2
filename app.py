from PyQt5.QtWidgets import QWidget, QApplication, QFileDialog, QVBoxLayout, QMessageBox
import sys
import ui
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import pydicom
import logging
import numpy as np
import os
from functools import partial

logging.basicConfig(filename='logs.log', level=logging.INFO, format='%(asctime)s:%(name)s:%(message)s')


class MatplotWidget(QWidget):
    def __init__(self, parent=None):
        super(MatplotWidget, self).__init__(parent)
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.axis = self.figure.add_subplot()
        self.layout_vertical = QVBoxLayout(self)
        self.layout_vertical.addWidget(self.canvas)

    
class MainWidget(QWidget, ui.Ui_Form):
    def __init__(self):
        super(MainWidget, self).__init__()
        self.setupUi(self)
        self.init_widget()
        self.axial = None
        self.coronal = None
        self.sagital = None
        self.ax_value_x = 0.5
        self.ax_value_y = 0.5
        self.cor_value_x = 0.5
        self.cor_value_y = 0.5
        self.sag_value_x = 0.5
        self.sag_value_y = 0.5

        self.Open_Button.clicked.connect(self.browse)
        self.horizontalSlider_2.valueChanged.connect(partial(self.generate_slice_vertical, axis='axial'))
        self.verticalSlider_2.valueChanged.connect(partial(self.generate_slice_horizontal, axis='axial'))
        self.horizontalSlider_3.valueChanged.connect(partial(self.generate_slice_vertical, axis='coronal'))
        self.verticalSlider_3.valueChanged.connect(partial(self.generate_slice_horizontal, axis='coronal'))
        self.horizontalSlider_4.valueChanged.connect(partial(self.generate_slice_vertical, axis='sagital'))
        self.verticalSlider_4.valueChanged.connect(partial(self.generate_slice_horizontal, axis='sagital'))

    @staticmethod
    def gen_layout(x):
        """
        A function to add the widget to GUI to make initiation easier.
        params:
        x: the widget to be added to the GUI.
        return: widget, layout
        """
        w = MatplotWidget()
        l = QVBoxLayout(x)
        l.addWidget(w)
        return w, l

    def init_widget(self):
        """
        A function to initiate the widgets for display.
        """
        # axial - coronal - sag - oblique
        self.img_widget, self.layout_vertical4 = self.gen_layout(self.Display_4)
        self.axial_widget, self.layout_vertical1 = self.gen_layout(self.Display_1)
        self.cor_widget, self.layout_vertical2 = self.gen_layout(self.Display_2)
        self.sag_widget, self.layout_vertical3 = self.gen_layout(self.Display_3)

    def display_single_plot(self, img, aspect, widget, value_x, value_y):
        widget.axis.clear()
        widget.axis.axhline(y=self.img_shape[1] * value_y, color='r')
        widget.axis.axvline(x=self.img_shape[0] * value_x, color='b')
        widget.axis.imshow(img, cmap='gray', aspect=aspect)
        widget.canvas.draw()

    def display(self, axial, coronal, sagital):
        self.display_single_plot(axial[0], axial[1], self.axial_widget, self.ax_value_x, self.ax_value_y)
        self.display_single_plot(coronal[0], coronal[1], self.cor_widget, self.cor_value_x, self.cor_value_y)
        self.display_single_plot(sagital[0], sagital[1], self.sag_widget, self.sag_value_x, self.sag_value_y)

    def browse(self):
        self.folder = QFileDialog.getExistingDirectory(self, "Choose Folder")
        if self.folder[0] == "":
            return
        try:
            self.slices = []
            for file in os.listdir(self.folder):
                self.slices.append(pydicom.dcmread(f'{self.folder}/{file}'))
            logging.info('Slices Loaded')

            # self.img, self.axial, self.sag, self.cor = self.generate_image(self.slices)
            logging.info('CT generated')
            self.generate_image(self.slices)

            # self.display()

            logging.info("Images Displayed")

        except Exception as e:
            logging.error(f'An error occurred in browse function ln 52: {e}')
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("An error occurred, please check the log file")
            msg.setWindowTitle("Error")
            msg.exec_()
            self.browse()
        
    def generate_image(self, slices, axis=None, pos=None, pos_x=None, pos_y=None):
        try:
            # assuming all slices have the same pixel aspects, so using only the first
            # if not should be in the loop.
            ps = slices[0].PixelSpacing
            ss = slices[0].SliceThickness
            ax_aspect = ps[1]/ps[0]
            sag_aspect = ps[1]/ss
            cor_aspect = ss/ps[0]

            self.img_shape = list(slices[0].pixel_array.shape)
            self.img_shape.append(len(slices))
            img3d = np.zeros(self.img_shape)
            for i, s in enumerate(slices):
                if pos == 'x':
                    img2d = s.pixel_array[pos_x, :]
                elif pos == 'y':
                    img2d = s.pixel_array[:, pos_y]
                else:
                    img2d = s.pixel_array
                img3d[:, :, i] = img2d

            if pos is None:
                self.coronal = (np.rot90(img3d[self.img_shape[0]//2, :, :]), cor_aspect)
                self.sagital = (np.rot90(img3d[:, self.img_shape[1]//2, :]), sag_aspect)
                self.axial = (img3d[:, :, self.img_shape[2]//2], ax_aspect)

            if axis == 'axial':
                coronal = (np.rot90(img3d[self.img_shape[0] // 2, :, :]), cor_aspect)
                sagital = (np.rot90(img3d[self.img_shape[0] // 2, :, :]), sag_aspect)

                if pos == 'x':
                    self.ax_value_x = pos_x / self.img_shape[0]
                    self.coronal = coronal
                elif pos == 'y':
                    self.ax_value_y = pos_y / self.img_shape[1]
                    self.sagital = sagital

            elif axis == 'coronal':
                axial = (img3d[:, :, self.img_shape[2]//2], ax_aspect)
                sagital = (np.rot90(img3d[self.img_shape[1] // 2, :, :]), sag_aspect)

                if pos == 'x':
                    self.cor_value_x = pos_x / self.img_shape[0]
                    self.axial = axial
                elif pos == 'y':
                    self.cor_value_y = pos_y / self.img_shape[1]
                    self.sagital = sagital

            elif axis == 'sagital':
                axial = (img3d[:, :, self.img_shape[2]//2], ax_aspect)
                coronal = (np.rot90(img3d[self.img_shape[2] // 2, :, :]), cor_aspect)
                if pos == 'x':
                    self.sag_value_x = pos_x / self.img_shape[0]
                    self.coronal = coronal
                elif pos == 'y':
                    self.sag_value_y = pos_y / self.img_shape[1]
                    self.axial = axial

            self.display(self.axial, self.coronal, self.sagital)

        except Exception as e:
            logging.error(f'An error occurred in slices function ln 81: {e}')
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error, Image corrupted")
            msg.setWindowTitle("Error")
            msg.exec_()
            self.browse()

    def generate_slice_vertical(self, value, axis):
        try:
            self.generate_image(slices=self.slices, pos='x', pos_x=int((value/100) * self.img_shape[0]), axis=axis)

        except Exception as e:
            print(e)

    def generate_slice_horizontal(self, value, axis):
        try:
            self.generate_image(slices=self.slices, pos='y', pos_y=int((value/100) * self.img_shape[0]), axis=axis)

        except Exception as e:
            print(e)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWidget()
    w.show()
    sys.exit(app.exec_())
