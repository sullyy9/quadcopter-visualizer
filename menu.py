from PyQt5 import QtCore, QtWidgets, QtSerialPort


#
# Main menu bar of the application.
#
class MenuBar(QtWidgets.QMenuBar):
    def __init__(self, parent):
        super(MenuBar, self).__init__(parent)
        self.setGeometry(QtCore.QRect(0, 0, 1000, 25))

        self.serial = SerialMenu("Serial Port")
        self.addMenu(self.serial)

    #
    # Refresh any menus that need to be refreshed
    #
    def refresh(self):
        self.serial.refresh()


#
# Sub menu of the menu bar. Controls the current serial port.
#
class SerialMenu(QtWidgets.QMenu):
    def __init__(self, name):
        super(SerialMenu, self).__init__(name)

        # Initialise a dictionary list of options.
        self.options = {"None": self.addAction("None")}
        self.options["None"].triggered.connect(self.menu_action)
        self.options["None"].setCheckable(True)
        self.options["None"].setChecked(True)
        self.current_option = "None"

        # # Create an action group. this allows only one option to be selected at a time.
        self.group = QtWidgets.QActionGroup(self)
        self.group.addAction(self.options["None"])

        # Update options.
        self.refresh()

    #
    # Add an option to the menu.
    #
    def add_option(self, option):
        self.options[option] = self.addAction(option)
        self.options[option].triggered.connect(self.menu_action)
        self.options[option].setCheckable(True)
        self.group.addAction(self.options[option])

    #
    # Remove an option from the menu.
    #
    def remove_option(self, option):
        self.removeAction(self.options[option])
        self.group.removeAction(self.options[option])
        del self.options[option]

    #
    # Refreshes this menus options.
    #
    def refresh(self):
        ports = QtSerialPort.QSerialPortInfo.availablePorts()

        # Remove all options
        for option in list(self.options):
            self.remove_option(option)

        # Re-add the noen option
        self.add_option("None")

        # Add each port to the options list.
        for port in ports:
            self.add_option(port.portName())

        if self.current_option not in self.options.keys():
            self.current_option = "None"
        
        self.options[self.current_option].setChecked(True)

    #
    # Action when an option in this menu is selected.
    #
    def menu_action(self):
        for option in self.options:
            if self.options[option].isChecked() is True:
                self.current_option = option
