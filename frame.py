from PyQt5 import QtCore, QtWidgets
import pyqtgraph as pg


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

        # Create sets of data
        self.accel_data = DataSet(name="Acceleration", units="mg0", fields=["X", "Y", "Z"],
                                  min_range=-2000, max_range=2000)

        self.gyro_data = DataSet(name="Rotation Rate", units="dps", fields=["Roll", "Pitch", "Yaw"],
                                 min_range=-500, max_range=500)

        self.orientation_data = DataSet(name="Orientation", units="degrees", fields=["Bank", "Attitude", "Heading"],
                                        min_range=-180, max_range=180)

        # Create a graph widget
        self.graph_widget = pg.GraphicsLayoutWidget()
        self.layout.addWidget(self.graph_widget, 1, 1, 1, 1)

        # Create plots
        self.accel_plot = DataPlot(self.accel_data)
        self.graph_widget.ci.addItem(self.accel_plot, row=0, col=0)

        self.gyro_plot = DataPlot(self.gyro_data)
        self.graph_widget.ci.addItem(self.gyro_plot, row=0, col=1)

        self.orientation_plot = DataPlot(self.orientation_data)
        self.graph_widget.ci.addItem(self.orientation_plot, row=0, col=2)

        # Setup a timer to refresh the graphs periodically
        self.graph_timer = QtCore.QTimer()
        self.graph_timer.timeout.connect(self.update_graphs)
        self.graph_timer.start(100)

    def update_graphs(self):
        self.accel_plot.update(self.accel_data)
        self.gyro_plot.update(self.gyro_data)
        self.orientation_plot.update(self.orientation_data)


########################################################################################################################
class DataSet:
    def __init__(self, name="None", units="None", fields=None, max_range=4000, min_range=-4000):
        self.name = name
        self.units = units
        self.min_range = min_range
        self.max_range = max_range

        self.timestamp = [0]
        self.fields = {}
        for field in fields:
            self.fields[field] = [0]


########################################################################################################################
class DataPlot(pg.PlotItem):
    def __init__(self, data_set: DataSet):
        # Create the plot (PlotItem) and set the view area
        super(DataPlot, self).__init__(title=data_set.name,
                                       labels={"left": data_set.name + data_set.units, "bottom": "Time (ms)"})
        self.setRange(xRange=[0, 60000], yRange=[data_set.max_range, data_set.min_range])
        self.setMouseEnabled(x=False, y=True)

        # Create the curves (PlotDataItem) and legend for the plot
        colours = ["r", "g", "b", "c", "m", "y"]
        colour = 0

        self.legend = self.addLegend(offset=[1, 1])
        self.plot_curves = {}
        for field in data_set.fields.keys():
            self.plot_curves[field] = self.plot(pen=pg.mkPen(colours[colour]))
            self.legend.addItem(self.plot_curves[field], field)
            colour += 1

    def update(self, data_set: DataSet):
        # Only plot data up to where we have a complete set and timestamp
        limit = len(data_set.timestamp)
        for field in data_set.fields.keys():
            if len(data_set.fields[field]) < limit:
                limit = len(data_set.fields[field])

        for field in data_set.fields.keys():
            self.plot_curves[field].setData(data_set.timestamp[:limit], data_set.fields[field][:limit])

        self.setXRange(data_set.timestamp[-1] - 30000,
                       data_set.timestamp[-1] + 30000)
