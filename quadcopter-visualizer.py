# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './qtdesigner-workspace/quadcopter-visualizer.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!

import sys
import os
import pyqtgraph
from PyQt5 import QtCore, QtGui, QtWidgets, QtSerialPort


########################################################################################################################
class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        # Configure the window properties: size and name
        self.setGeometry(50, 50, 1920, 1080)
        self.setWindowTitle("Quadcopter Visualizer")

        # Add a menu bar for at the top of the window
        self.menu_bar = QtWidgets.QMenuBar(self)
        self.menu_bar.setGeometry(QtCore.QRect(0, 0, 1000, 25))
        self.setMenuBar(self.menu_bar)

        # Add a menu bar option for changing the serial port
        self.menu_serial_port = self.menu_bar.addMenu("Serial Port")

        # Add the options to the Serial Port menu. Make them part of a group so only one can be active
        self.serial_options = {"None": self.menu_serial_port.addAction("None")}
        self.serial_options["None"].triggered.connect(self.menu_bar_action)
        self.serial_options["None"].setCheckable(True)
        self.serial_options["None"].setChecked(True)

        self.serial_options_group = QtWidgets.QActionGroup(self.menu_serial_port)
        self.serial_options_group.addAction(self.serial_options["None"])

        # Update the serial port options now and set a timer to do it periodically
        self.serial_port_list_update()
        self.serial_options_timer = QtCore.QTimer()
        self.serial_options_timer.timeout.connect(self.serial_port_list_update)
        self.serial_options_timer.setInterval(1000)
        self.serial_options_timer.start()

        self.serial = QtSerialPort.QSerialPort()

        self.main_widget = MainWidget(self)
        self.setCentralWidget(self.main_widget)
        self.show()

    ####################################################################################################################
    # send whatever option was selected through to the terminal frame
    def menu_bar_action(self):
        for name in self.serial_options:
            if self.serial_options[name].isChecked() is True:
                self.initialise_serial("/dev/" + name)

    # Call periodically to update the list of serial ports in the menu bar
    def serial_port_list_update(self):
        # Delete items that no longer exist on the system
        for name in list(self.serial_options):
            if os.path.exists("/dev/" + name) is False and name != "None":
                self.menu_serial_port.removeAction(self.serial_options[name])
                self.serial_options_group.removeAction(self.serial_options[name])
                del self.serial_options[name]

        # Add new items that don't exist in the list
        for file in os.listdir("/dev/"):
            if file[:4] == "ttyA" and file not in self.serial_options.keys():
                self.serial_options[file] = self.menu_serial_port.addAction(file)
                self.serial_options_group.addAction(self.serial_options[file])
                self.serial_options[file].setCheckable(True)
                self.serial_options[file].triggered.connect(self.menu_bar_action)

    ####################################################################################################################
    def initialise_serial(self, port_name):
        if self.serial.isOpen() is True:
            self.serial.close()

        self.serial.setPortName(port_name)
        self.serial.setBaudRate(115200)
        self.serial.readyRead.connect(self.parse_serial_data)
        self.serial.open(QtCore.QIODevice.OpenModeFlag.ReadWrite)

    def parse_serial_data(self):
        while self.serial.canReadLine():
            string = bytes(self.serial.readLine()).translate(None, b"\x00\r").decode("utf-8")
            self.main_widget.terminal_frame.write_to_screen(string)

            if string.count("DATA:TIME:") > 0:
                data = string[len("DATA:TIME:"):-len("\n")]
                self.main_widget.data_frame.accel_data["ACCEL_TIME"].append(int(data))
                self.main_widget.data_frame.gyro_data["GYRO_TIME"].append(int(data))

            if string.count("DATA:ACCELX:") > 0:
                data = string[len("DATA:ACCELX:"):-len("\n")]
                self.main_widget.data_frame.accel_data["ACCEL_X"].append(int(data))

            if string.count("DATA:ACCELY:") > 0:
                data = string[len("DATA:ACCELY:"):-len("\n")]
                self.main_widget.data_frame.accel_data["ACCEL_Y"].append(int(data))

            if string.count("DATA:ACCELZ:") > 0:
                data = string[len("DATA:ACCELZ:"):-len("\n")]
                self.main_widget.data_frame.accel_data["ACCEL_Z"].append(int(data))

            if string.count("DATA:GYROX:") > 0:
                data = string[len("DATA:GYROX:"):-len("\n")]
                self.main_widget.data_frame.gyro_data["GYRO_ROLL"].append(int(data))

            if string.count("DATA:GYROY:") > 0:
                data = string[len("DATA:GYROY:"):-len("\n")]
                self.main_widget.data_frame.gyro_data["GYRO_PITCH"].append(int(data))

            if string.count("DATA:GYROZ:") > 0:
                data = string[len("DATA:GYROZ:"):-len("\n")]
                self.main_widget.data_frame.gyro_data["GYRO_YAW"].append(int(data))


########################################################################################################################
class MainWidget(QtWidgets.QWidget):
    def __init__(self, parent):
        super(MainWidget, self).__init__(parent)
        self.layout = QtWidgets.QGridLayout(self)

        # Create the 4 frames: terminal, error, data, instrument. Add them to their respective quadrants
        self.instrument_frame = InstrumentFrame(self)
        self.terminal_frame = TerminalFrame(self)
        self.error_frame = ErrorFrame(self)
        self.data_frame = DataFrame(self)

        self.layout.addWidget(self.instrument_frame, 1, 1, 1, 1)
        self.layout.addWidget(self.terminal_frame, 1, 0, 1, 1)
        self.layout.addWidget(self.error_frame, 2, 0, 1, 1)
        self.layout.addWidget(self.data_frame, 2, 1, 1, 1)

        self.layout.setRowStretch(1, 3)
        self.layout.setRowStretch(2, 2)
        self.layout.setColumnStretch(0, 2)
        self.layout.setColumnStretch(1, 3)


########################################################################################################################
class TemplateFrame(QtWidgets.QFrame):
    def __init__(self, parent):
        super(TemplateFrame, self).__init__(parent)
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Raised)
        self.layout = QtWidgets.QGridLayout(self)

        # Add the frames title
        self.title = QtWidgets.QLabel(self)
        self.title.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.layout.addWidget(self.title, 0, 1, 1, 1)


########################################################################################################################
class InstrumentFrame(TemplateFrame):
    def __init__(self, parent):
        super(InstrumentFrame, self).__init__(parent)
        self.title.setText("Instruments")


########################################################################################################################
class TerminalFrame(TemplateFrame):
    def __init__(self, parent):
        super(TerminalFrame, self).__init__(parent)
        self.title.setText("Terminal")

        # Add the terminal screen
        self.screen = QtWidgets.QTextBrowser(self)
        self.layout.addWidget(self.screen, 1, 1, 1, 1)

    def write_to_screen(self, string):
        self.screen.append(string)


########################################################################################################################
class ErrorFrame(TemplateFrame):
    def __init__(self, parent):
        super(ErrorFrame, self).__init__(parent)
        self.title.setText("Errors")

        # Add the error screen
        self.screen = QtWidgets.QTextBrowser(self)
        self.layout.addWidget(self.screen, 1, 1, 1, 2)


########################################################################################################################
class DataFrame(TemplateFrame):
    def __init__(self, parent):
        super(DataFrame, self).__init__(parent)
        self.title.setText("Data")

        # Create a graph widget
        self.graph_window = pyqtgraph.GraphicsWindow()
        self.layout.addWidget(self.graph_window, 1, 1, 1, 1)

        # Create the separate graphs and set the initial view area
        self.accel_graph = self.graph_window.addPlot()
        self.accel_graph.setXRange(0, 60000)
        self.accel_graph.setYRange(-2000, 2000)
        self.graph_window.nextCol()
        self.gyro_graph = self.graph_window.addPlot()
        self.gyro_graph.setXRange(0, 60000)
        self.gyro_graph.setYRange(-500, 500)

        # Create the curves for each graph
        self.accel_x_curve = self.accel_graph.plot(pen=pyqtgraph.mkPen("r"))
        self.accel_y_curve = self.accel_graph.plot(pen=pyqtgraph.mkPen("g"))
        self.accel_z_curve = self.accel_graph.plot(pen=pyqtgraph.mkPen("b"))

        self.gyro_roll_curve = self.gyro_graph.plot(pen=pyqtgraph.mkPen("r"))
        self.gyro_pitch_curve = self.gyro_graph.plot(pen=pyqtgraph.mkPen("g"))
        self.gyro_yaw_curve = self.gyro_graph.plot(pen=pyqtgraph.mkPen("b"))

        # Initialise data sets for each graph
        self.accel_data = {
            "ACCEL_TIME": [0],
            "ACCEL_X": [0],
            "ACCEL_Y": [0],
            "ACCEL_Z": [0],
        }
        self.gyro_data = {
            "GYRO_TIME": [0],
            "GYRO_ROLL": [0],
            "GYRO_PITCH": [0],
            "GYRO_YAW": [0],
        }

        self.graph_timer = QtCore.QTimer()
        self.graph_timer.timeout.connect(self.update_accel_graph)
        self.graph_timer.timeout.connect(self.update_gyro_graph)
        self.graph_timer.start(100)

    def update_accel_graph(self):
        limit = min(len(self.accel_data["ACCEL_TIME"]), len(self.accel_data["ACCEL_X"]),
                    len(self.accel_data["ACCEL_Y"]), len(self.accel_data["ACCEL_Z"]))
        self.accel_x_curve.setData(self.accel_data["ACCEL_TIME"][:limit], self.accel_data["ACCEL_X"][:limit])
        self.accel_y_curve.setData(self.accel_data["ACCEL_TIME"][:limit], self.accel_data["ACCEL_Y"][:limit])
        self.accel_z_curve.setData(self.accel_data["ACCEL_TIME"][:limit], self.accel_data["ACCEL_Z"][:limit])

        self.accel_graph.setXRange(self.accel_data["ACCEL_TIME"][-1] - 30000,
                                   self.accel_data["ACCEL_TIME"][-1] + 30000)

    def update_gyro_graph(self):
        limit = min(len(self.gyro_data["GYRO_TIME"]), len(self.gyro_data["GYRO_ROLL"]),
                    len(self.gyro_data["GYRO_PITCH"]), len(self.gyro_data["GYRO_YAW"]))
        self.gyro_roll_curve.setData(self.gyro_data["GYRO_TIME"][:limit], self.gyro_data["GYRO_ROLL"][:limit])
        self.gyro_pitch_curve.setData(self.gyro_data["GYRO_TIME"][:limit], self.gyro_data["GYRO_PITCH"][:limit])
        self.gyro_yaw_curve.setData(self.gyro_data["GYRO_TIME"][:limit], self.gyro_data["GYRO_YAW"][:limit])

        self.gyro_graph.setXRange(self.gyro_data["GYRO_TIME"][-1] - 30000,
                                  self.gyro_data["GYRO_TIME"][-1] + 30000)


########################################################################################################################
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = Window()
    sys.exit(app.exec_())
