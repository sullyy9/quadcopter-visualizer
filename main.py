import sys

from PyQt5 import QtCore, QtWidgets, QtSerialPort

from frame import *
from menu import *


#
# Main window. Everything is contained within this.
#
class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        # Configure the window properties: size and name
        self.setGeometry(50, 50, 1920, 1080)
        self.setWindowTitle("Quadcopter Visualizer")

        # Add a menu bar for at the top of the window
        self.menu_bar = MenuBar(self)
        self.setMenuBar(self.menu_bar)

        # Setup periodic refreshing of the menu bar.
        self.menu_bar_timer = QtCore.QTimer()
        self.menu_bar_timer.timeout.connect(self.menu_bar.refresh)
        self.menu_bar_timer.setInterval(1000)
        self.menu_bar_timer.start()

        # self.serial = QtSerialPort.QSerialPort()

        # Setup the main widget and start the GUI.
        self.main_widget = MainWidget(self)
        self.setCentralWidget(self.main_widget)
        self.show()

    #
    #
    #
    def initialise_serial(self, port_name):
        if self.serial.isOpen() is True:
            self.serial.close()

        self.serial.setPortName(port_name)
        self.serial.setBaudRate(115200)
        self.serial.readyRead.connect(self.parse_serial_data)
        self.serial.open(QtCore.QIODevice.OpenModeFlag.ReadWrite)

    #
    #
    #
    def parse_serial_data(self):
        while self.serial.canReadLine():
            string = bytes(self.serial.readLine()).decode("ascii")
            self.main_widget.terminal_frame.write_to_screen(string)

            # if string.count("flight controller - start") > 0:
            #     for key in self.main_widget.data_frame.accel_data.keys():
            #         self.main_widget.data_frame.accel_data[key] = [0]
            #     for key in self.main_widget.data_frame.gyro_data.keys():
            #         self.main_widget.data_frame.gyro_data[key] = [0]

            if string.count("DATA:TIME:") > 0:
                data = string[len("DATA:TIME:"):-len("\n")]
                self.main_widget.data_frame.accel_data.timestamp.append(
                    int(data))
                self.main_widget.data_frame.gyro_data.timestamp.append(
                    int(data))
                self.main_widget.data_frame.orientation_data.timestamp.append(
                    int(data))

            elif string.count("DATA:KBANK:") > 0:
                data = string[len("DATA:KBANK:"):-len("\n")]
                self.main_widget.data_frame.orientation_data.fields["Bank"].append(
                    int(data))

            elif string.count("DATA:KATTITUDE:") > 0:
                data = string[len("DATA:KATTITUDE:"):-len("\n")]
                self.main_widget.data_frame.orientation_data.fields["Attitude"].append(
                    int(data))

            elif string.count("DATA:KHEADING:") > 0:
                data = string[len("DATA:KHEADING:"):-len("\n")]
                self.main_widget.data_frame.orientation_data.fields["Heading"].append(
                    int(data))

            elif string.count("DATA:ACCELX:") > 0:
                data = string[len("DATA:ACCELX:"):-len("\n")]
                self.main_widget.data_frame.accel_data.fields["X"].append(
                    int(data))

            elif string.count("DATA:ACCELY:") > 0:
                data = string[len("DATA:ACCELY:"):-len("\n")]
                self.main_widget.data_frame.accel_data.fields["Y"].append(
                    int(data))

            elif string.count("DATA:ACCELZ:") > 0:
                data = string[len("DATA:ACCELZ:"):-len("\n")]
                self.main_widget.data_frame.accel_data.fields["Z"].append(
                    int(data))

            elif string.count("DATA:GYROROLL:") > 0:
                data = string[len("DATA:GYROROLL:"):-len("\n")]
                self.main_widget.data_frame.gyro_data.fields["Roll"].append(
                    int(data))

            elif string.count("DATA:GYROPITCH:") > 0:
                data = string[len("DATA:GYROPITCH:"):-len("\n")]
                self.main_widget.data_frame.gyro_data.fields["Pitch"].append(
                    int(data))

            elif string.count("DATA:GYROYAW:") > 0:
                data = string[len("DATA:GYROYAW:"):-len("\n")]
                self.main_widget.data_frame.gyro_data.fields["Yaw"].append(
                    int(data))


#
# Main windget within the main window. All other widgets are contained within this.
#
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
        self.layout.setColumnStretch(1, 5)


########################################################################################################################
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = Window()
    sys.exit(app.exec_())
