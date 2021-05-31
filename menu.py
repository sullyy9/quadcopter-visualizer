from typing import Callable
from PyQt5 import QtCore, QtWidgets, QtSerialPort


class MenuBar(QtWidgets.QMenuBar):
    """
    Menu bar class which inherits from QMenuBar. Should go at the top of the main window.

    Attributes
    ----------
    serial : SerialMenu
        Menu for selecting the serial port.

    Methods
    ----------
    set_serial_callback(callback: Callable)
        Sets the serial menu callback function.

    def refresh()
        Refreshes all menus, removing non-valid options and adding new ones.

    """

    def __init__(self):
        super(MenuBar, self).__init__()
        self.setGeometry(QtCore.QRect(0, 0, 1000, 25))

        self.serial = SerialMenu("Serial Port")
        self.addMenu(self.serial)

    def set_serial_callback(self, callback: Callable):
        """
        Set the function to be called when an option is selected in the serial menu.

        Parameters
        ----------
        callback: function
            Function to be called when an option is selected.

        """

        self.serial.set_callback_function(callback)

    def refresh(self):
        """
        Refresh all menus, removing non-valid options and adding new ones.

        """

        self.serial.refresh()


#
# Sub menu of the menu bar. Controls the current serial port.
#
class SerialMenu(QtWidgets.QMenu):
    """
    Menu class which inherits from QMenu. Element of the menu bar.

    Attributes
    ----------
    callback_function : Callable
        Function to be called when an option is selected.

    options : Dictionary {str : QAction}
        Contains option names as keys and their corresponding actions as values.

    group : QActionGroup
        Group of all actions in options. Allows only one option to be selected.

    Methods
    ----------
    add_option(option: str)
        Add an option to the menu.

    remove_option(option: str)
        Remove an option to the menu.

    refresh()
        Refreshes the options, removing non-valid ones and adding new ones.

    set_callback_function(callback: Callable)
        Sets the callback function.

    menu_action()
        Called when an option is selected. Calls the callback function.

    """

    def __init__(self, name):
        super(SerialMenu, self).__init__(name)

        # Initialise the callback function with a dummy.
        self.callback_function = lambda port: None

        self.options = {}

        # Initialise an action group which all option's actions will be assigned to.
        self.group = QtWidgets.QActionGroup(self)

        # Initialise options.
        self.add_option("None")
        self.options["None"].setChecked(True)
        self.refresh()

    def add_option(self, option: str):
        """
        Add an option to the options list.

        Parameters
        ----------
        option : str
            Name of the option. This will also be the key.

        """

        self.options[option] = self.addAction(option)
        self.options[option].triggered.connect(self.menu_action)
        self.options[option].setCheckable(True)
        self.group.addAction(self.options[option])

    def remove_option(self, option: str):
        """
        Remove an option from the options list.

        Parameters
        ----------
        option : str
            Name of the option. This will also be the key.

        """

        self.removeAction(self.options[option])
        self.group.removeAction(self.options[option])
        del self.options[option]

    def refresh(self):
        """
        Refresh all options, removing non-valid ones and adding new ones.

        """
        ports = QtSerialPort.QSerialPortInfo.availablePorts()

        # Gather the port names into a list.
        port_names = []
        for port in ports:
            port_names.append(port.portName())

        # Remove all options that are no longer available.
        for option in list(self.options):
            if option not in port_names and option != "None":
                if self.options[option].isChecked():
                    self.options["None"].setChecked(True)
                self.remove_option(option)

        # Add new ports to the options.
        for port in port_names:
            if port not in self.options.keys():
                self.add_option(port)

    def set_callback_function(self, callback_function: Callable):
        """
        Set the callback function.

        Parameters
        ----------
        callback_function : Callable
            function to be called when an option is selected

        """

        self.callback_function = callback_function

    def menu_action(self):
        """
        Called when an option is selected. Calls the callback function and passes it the selected
        option.

        """
        for option in list(self.options):
            if self.options[option].isChecked():
                self.callback_function(option)
                break
