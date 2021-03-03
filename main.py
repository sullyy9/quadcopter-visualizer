#!/usr/bin/python3.9
import serial
import time
import gui


def main():
    # Setup the gui
    main_gui = gui.Gui()
    serial_port = serial.Serial(port=None, baudrate=115200)
    time_last_refresh = 0

    while main_gui.gui_running is True:

        # update the gui and get the newest serial port every 10ms
        if (time.time_ns() - time_last_refresh) > 10000000:
            main_gui.update()
            if main_gui.serial_port_new is True:
                serial_port_update(serial_port, main_gui.serial_port_get())
            time_last_refresh = time.time_ns()

        # Read data from the serial port, strip any null or carriage return characters
        if serial_port.port is not None and serial_port.in_waiting > 0:
            string = serial_port.read(serial_port.in_waiting).translate(None, b"\x00\r")
            main_gui.serial_insert(string)

    # End of main loop. Cleanup
    if serial_port.port is not None:
        serial_port.close()


def serial_port_update(serial_port, new_port):
    serial_port.close()
    try:
        serial_port.port = ("/dev/" + new_port)
        serial_port.open()

    except serial.SerialException:
        serial_port.port = None


# Execute the main function if this file is run as an application
if __name__ == "__main__":
    main()
