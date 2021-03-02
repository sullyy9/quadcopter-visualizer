#!/usr/bin/python3.9
import serial
import time
import gui


def main():
    main_gui = gui.Gui()
    serial_port = None
    time_last_refresh = 0

    while main_gui.gui_running is True:
        # update the gui and get the newest serial port every 10ms
        if (time.time_ns() - time_last_refresh) > 10000000:
            main_gui.update()

            if main_gui.serial_port_new() is True:
                try:
                    serial_port = serial.Serial(port="/dev/" + main_gui.serial_port_get(), baudrate=115200,
                                                parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,
                                                bytesize=serial.EIGHTBITS)

                except serial.SerialException:
                    serial_port = None

                else:
                    serial_port.flushInput()

        # Read data from the serial port
        if serial_port is not None and serial_port.in_waiting != 0:
            print(serial_port.in_waiting)
            main_gui.serial_insert(serial_port.readline())

    if serial_port is not None:
        serial_port.close()
        print("serial port closed")


if __name__ == "__main__":
    main()
