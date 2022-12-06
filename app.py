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
        self.layout_vertical3 = None
        self.cor_widget = None
        self.layout_vertical2 = None
        self.sag_widget = None
        self.layout_vertical1 = None
        self.axial_widget = None
        self.layout_vertical4 = None
        self.img_widget = None
        self.setupUi(self)
        self.init_widget()
        self.axial = None
        self.coronal = None
        self.sagittal = None
        self.img_shape = None
        self.slices = None
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
        self.horizontalSlider_4.valueChanged.connect(partial(self.generate_slice_vertical, axis='sagittal'))
        self.verticalSlider_4.valueChanged.connect(partial(self.generate_slice_horizontal, axis='sagittal'))

    @staticmethod
    def gen_layout(x):
        """
        A function to add the widget to GUI to make initiation easier.
        params:
        x: the widget to be added to the GUI.
        return: widget, layout
        """
        widget = MatplotWidget()
        layout = QVBoxLayout(x)
        layout.addWidget(widget)
        return widget, layout

    def init_widget(self):
        """
        A function to initiate the widgets for display.
        """
        # axial - coronal - sag - oblique
        self.img_widget, self.layout_vertical4 = self.gen_layout(self.Display_4)
        self.axial_widget, self.layout_vertical1 = self.gen_layout(self.Display_1)
        self.cor_widget, self.layout_vertical2 = self.gen_layout(self.Display_2)
        self.sag_widget, self.layout_vertical3 = self.gen_layout(self.Display_3)

    @staticmethod
    def display_single_plot(img, aspect, widget, value_x, value_y):
        """
        A function to display a single image given a plane.
        params:
        :param img: the image to be displayed
        :param aspect: the aspect ratio of the image
        :param widget: the gui widget to display the image on
        :param value_x: the x position of the slider for the line
        :param value_y: the y position of the slider for the line
        :return: None
        """
        widget.axis.clear()
        widget.axis.axhline(y=img.shape[0] * (1-value_y), color='r')
        widget.axis.axvline(x=img.shape[1] * value_x, color='b')
        widget.axis.imshow(img, cmap='gray', aspect=aspect)
        widget.canvas.draw()

    def display(self, axial, coronal, sagittal):
        """
        A function to display all planes of the image.
        params:
        :param axial: the axial plane image
        :param coronal: the coronal plane image
        :param sagittal: the sagittal plane image
        :return:
        """
        self.display_single_plot(axial[0], axial[1], self.axial_widget, self.ax_value_x, self.ax_value_y)
        self.display_single_plot(coronal[0], coronal[1], self.cor_widget, self.cor_value_x, self.cor_value_y)
        self.display_single_plot(sagittal[0], sagittal[1], self.sag_widget, self.sag_value_x, self.sag_value_y)

    def browse(self):
        """
        A function to browse the file and display the image.
        :return: None
        """
        folder = QFileDialog.getExistingDirectory(self, "Choose Folder")
        if folder[0] == "":
            return
        try:
            self.slices = []
            for file in os.listdir(folder):
                self.slices.append(pydicom.dcmread(f'{folder}/{file}'))
            logging.info('self.slices Loaded')

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
        
    def generate_image(self, slices, plane=None, pos=None, pos_x=None, pos_y=None):
        """
        A function to generate the image from the slices, handle the change in the sliders and display the image
         accordingly.
        params:
        :param slices: the slices read from the dicom files
        :param plane: the plane from which the slider was moved {axial, coronal, sagittal}
        :param pos: the orientation of the slider {horizontal, vertical}
        :param pos_x: the position of the slider in the x-axis
        :param pos_y: the position of the slider in the y-axis
        :return: None
        """
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
                self.sagittal = (np.rot90(img3d[:, self.img_shape[1]//2, :]), sag_aspect)
                self.axial = (img3d[:, :, self.img_shape[2]//2], ax_aspect)

            if plane == 'axial':
                coronal = (np.rot90(img3d[self.img_shape[0] // 2, :, :]), cor_aspect)
                sagittal = (np.rot90(img3d[self.img_shape[0] // 2, :, :]), sag_aspect)

                if pos == 'x':
                    self.ax_value_x = pos_x / self.img_shape[0]
                    self.coronal = coronal
                elif pos == 'y':
                    self.ax_value_y = pos_y / self.img_shape[1]
                    self.sagittal = sagittal

            elif plane == 'coronal':
                axial = (img3d[:, :, self.img_shape[2]//2], ax_aspect)
                sagittal = (np.rot90(img3d[self.img_shape[1] // 2, :, :]), sag_aspect)

                if pos == 'x':
                    self.cor_value_x = pos_x / self.img_shape[0]
                    self.axial = axial
                elif pos == 'y':
                    self.cor_value_y = pos_y / self.img_shape[1]
                    self.sagittal = sagittal

            elif plane == 'sagittal':
                axial = (img3d[:, :, self.img_shape[2]//2], ax_aspect)
                coronal = (np.rot90(img3d[self.img_shape[2] // 2, :, :]), cor_aspect)
                if pos == 'x':
                    self.sag_value_x = pos_x / self.img_shape[0]
                    self.coronal = coronal
                elif pos == 'y':
                    self.sag_value_y = pos_y / self.img_shape[1]
                    self.axial = axial

            self.display(self.axial, self.coronal, self.sagittal)

        except Exception as e:
            logging.error(f'An error occurred in slices function ln 81: {e}')
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error, Image corrupted")
            msg.setWindowTitle("Error")
            msg.exec_()
            self.browse()

    def generate_slice_vertical(self, value, plane):
        """
        A function, more of a middleware for the change in the vertical slider. It calls the generate_image function
        given the new orientation and the plane from which the slider was moved.
        params:
        :param value: the current value of the slider
        :param plane: the plane from which the slider was moved {axial, coronal, sagittal}
        :return:
        """
        try:
            self.generate_image(slices=self.slices, pos='x', pos_x=int((value/100) * self.img_shape[0]), plane=plane)

        except Exception as e:
            print(e)

    def generate_slice_horizontal(self, value, plane):
        """
        A function, more of a middleware for the change in the horizontal slider. It calls the generate_image function
        given the new orientation and the plane from which the slider was moved.
        params:
        :param value: the current value of the slider
        :param plane: the plane from which the slider was moved {axial, coronal, sagittal}
        :return:
        """
        try:
            self.generate_image(slices=self.slices, pos='y', pos_y=int((value/100) * self.img_shape[0]), plane=plane)

        except Exception as e:
            print(e)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWidget()
    w.show()
    sys.exit(app.exec_())
