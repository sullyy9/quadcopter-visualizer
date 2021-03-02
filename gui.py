#!/usr/bin/python3.9
from tkinter import *


class Gui:
    gui_running = True
    new_serial = False

    def __init__(self):
        # Setup the root widget with 5 cells
        self.root_widget = Tk()
        self.root_widget.title("Quadcopter Visualizer")
        self.root_widget.geometry("1536x1024")
        self.root_widget.rowconfigure(1, weight=0)
        self.root_widget.rowconfigure(1, weight=5)
        self.root_widget.rowconfigure(2, weight=1)
        self.root_widget.columnconfigure(0, weight=1)
        self.root_widget.columnconfigure(1, weight=0)
        self.root_widget.columnconfigure(2, weight=0)
        self.root_widget.columnconfigure(3, weight=5)

        # Setup the serial port section
        self.serial_port = "None"
        self.label_serial_port = Label(self.root_widget, width=20, text="Serial Port: " + self.serial_port)
        self.label_serial_port.grid(row=0, column=0, sticky=W)
        self.entry_serial_port = Entry(self.root_widget)
        self.entry_serial_port.grid(row=0, column=1)
        self.button_serial_port = Button(self.root_widget, text="Update", command=self.button_serial_port_function)
        self.button_serial_port.grid(row=0, column=2)

        # Setup frames
        self.debug_frame = self.DebugFrame(self.root_widget)
        self.error_frame = self.ErrorFrame(self.root_widget)
        self.visualisation_frame = self.VisualisationFrame(self.root_widget)
        self.graph_frame = self.GraphFrame(self.root_widget)

        # Setup window closed event handler
        self.root_widget.protocol("WM_DELETE_WINDOW", self.gui_closed)

    # refresh the gui
    def update(self):
        self.root_widget.update_idletasks()
        self.root_widget.update()

    def button_serial_port_function(self):
        self.serial_port = self.entry_serial_port.get()[:8]
        self.label_serial_port.config(text="Serial Port: " + self.serial_port)
        self.new_serial = True

    # return true if the serial port has been updated
    def serial_port_new(self):
        return self.new_serial

    # get the currently set serial port
    def serial_port_get(self):
        self.new_serial = False
        return self.serial_port

    # add debug output into the debug frame
    def serial_insert(self, string):
        self.debug_frame.debug_insert(string)

    # handler for when the gui window has been closed
    def gui_closed(self):
        self.gui_running = False

    class DebugFrame:
        debug_index = 1.0

        def __init__(self, parent_widget):
            # Create raw debug output frame
            self.frame_debug = LabelFrame(parent_widget)
            self.frame_debug.grid(row=1, column=0, columnspan=3, sticky=N + W + S + E)
            self.frame_debug.rowconfigure(0, weight=0)
            self.frame_debug.rowconfigure(1, weight=1)
            self.frame_debug.columnconfigure(0, weight=0)
            self.frame_debug.columnconfigure(1, weight=1)

            self.label_title = Label(self.frame_debug, text="Debug Output")
            self.label_title.grid(row=0, column=1)

            self.scrollbar = Scrollbar(self.frame_debug, width=20)
            self.scrollbar.grid(row=1, column=0, sticky=W + S + N, ipadx=0)
            self.text_debug = Text(self.frame_debug, state=DISABLED, yscrollcommand=self.scrollbar.set)
            self.text_debug.grid(row=1, column=1, sticky=N + S + E + W)

        def debug_insert(self, string):
            self.text_debug.config(state=NORMAL)
            self.text_debug.insert(self.debug_index, string)
            self.text_debug.config(state=DISABLED)
            self.debug_index += len(string)

    class ErrorFrame:
        def __init__(self, parent_widget):
            # Create error log output frame
            self.frame_error = LabelFrame(parent_widget)
            self.frame_error.grid(row=2, column=0, columnspan=3, sticky=N + W + S + E)
            self.label_title = Label(self.frame_error, text="Errors")
            self.label_title.grid(row=0, column=0)

    class VisualisationFrame:
        def __init__(self, parent_widget):
            # Create 3D Visualisation frame
            self.frame_visualisation = LabelFrame(parent_widget)
            self.frame_visualisation.grid(row=1, column=3, sticky=N + W + S + E)
            self.label_title = Label(self.frame_visualisation, text="3D Visualisation")
            self.label_title.grid(row=0, column=0)

    class GraphFrame:
        def __init__(self, parent_widget):
            # Create Graphing frame
            self.frame_graph = LabelFrame(parent_widget)
            self.frame_graph.grid(row=2, column=3, sticky=N + W + S + E)
            self.label_title = Label(self.frame_graph, text="Graphs")
            self.label_title.grid(row=0, column=0)
