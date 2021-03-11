#!/usr/bin/python3.9
import serial
import time
import gui_old

time_program_start = time.time_ns()


def main():
    # Setup the gui
    main_gui = gui_old.Gui()
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
            string = serial_port.readline().translate(None, b"\x00\r").decode("utf-8")
            main_gui.serial_insert(string)
            process_data(main_gui, string)

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


# Parse out any useful data from a line
def process_data(main_gui, string):
    # Placeholder for system time. Transmitter will eventually send its own time over
    if string.count("DATA:TIME:") > 0:
        data = string[len("DATA:TIME:"):-len("\n")]
        main_gui.graph_data("ACCEL_TIME", int(data))

    if string.count("DATA:ACCELX:") > 0:
        data = string[len("DATA:ACCELX:"):-len("\n")]
        main_gui.graph_data("ACCEL_X", int(data))

    if string.count("DATA:ACCELY:") > 0:
        data = string[len("DATA:ACCELY:"):-len("\n")]
        main_gui.graph_data("ACCEL_Y", int(data))

    if string.count("DATA:ACCELZ:") > 0:
        data = string[len("DATA:ACCELZ:"):-len("\n")]
        main_gui.graph_data("ACCEL_Z", int(data))


# Execute the main function if this file is run as an application
if __name__ == "__main__":
    main()
