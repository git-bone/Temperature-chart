from os.path import join, dirname
import datetime
import pandas as pd
import csv

from bokeh.io import curdoc
from bokeh.layouts import row, column, widgetbox, layout
from bokeh.models import Paragraph, Range1d, DataRange1d, LinearAxis,CustomJS
from bokeh.models.formatters import DatetimeTickFormatter
from bokeh.models.widgets import Tabs, Panel,Button, DatePicker, TextInput

from bokeh.plotting import figure

input_file_temp = ""  # location of csv datafile
plot_temp_title = "Temperature"
tools = 'pan,zoom_in,zoom_out,wheel_zoom,box_zoom,reset'
tab_title = "Temperature"

class Plot(object):

    """Class for plot set-up"""

    def __init__(self, title):
        self.plot = figure(x_axis_type="datetime", plot_width=600, tools=tools, toolbar_sticky=False)
        self.plot.title.text = title
        self.plot.title.align = "center"
        self.plot.title.text_font_size = "25px"
        self.plot.axis.axis_label_text_font_style = "bold"
        self.plot.xaxis.axis_label = "Date/Time"
        self.plot.xaxis.major_label_orientation = 45
        self.plot.xaxis.formatter = DatetimeTickFormatter(minutes=["%d %b %Y, %H:%M"],
                                                    hourmin = ["%d %b %Y, %H:%M"],
                                                    hours=["%d %B %Y, %H:%M"],
                                                    days=["%d %B %Y, %H:%M"],
                                                    months=["%d %B %Y"],
                                                    years=["%d %B %Y"])
        self.site_layout=layout([[self.plot],],sizing_mode='fixed')

    def get_dataset(self, source):
        with open(join(dirname(__file__), source),'r') as f:
            dataset = pd.read_csv(f, parse_dates=['date'])
        return dataset

    def getLayout(self):
        return self.site_layout

    def get_reverse_dict(self, source):
        with open(join(dirname(__file__), source),'r') as f:
            my_dict = [{k: v for k, v in row.items()}
                for row in reversed(list(csv.DictReader(f, skipinitialspace=True)))]
        return my_dict

    def first(self, iterable):
        it = (el for el in iterable if not el is "" )
        return next(it)

    def drop_warning(self):
        try:
            self.site_layout.children.remove(self.warning_layout)
        except: # Catch both AttributeError and ValueError
            pass

    def set_warning(self, text):
        paragraph = widgetbox(children=[Paragraph(text=text)])
        self.drop_warning()
        self.warning_layout = layout([[paragraph],],sizing_mode='fixed')
        self.site_layout.children.append(self.warning_layout)

    def check_int_in_list(self, checklist):
        print (str(checklist))
        appendix = []
        thing = True
        for value in checklist:
            print ("value = " + str(value))
            # TODO "0" doesn't seem to be handled correctly either
            if (value is "" or value is None):
                pass
            else:
                try:
                    if int(value):
                        if not thing:
                            thing = False
                        else:
                            thing = True
                    else:
                        thing = False
                        appendix.append(value)
                except:
                    thing = False
                    appendix.append(value)
        print ("appendix: "+ str(appendix) + "," + str(thing))
        return thing, appendix

class Plot_Temp(Plot):

    """Class for temperature plot"""

    def __init__(self,title):
        Plot.__init__(self,title)
        self.plot.yaxis.axis_label = "Temperature (C)"
        self.plot.x_range = DataRange1d(follow='end', follow_interval=19200000, range_padding=0)
        self.plot.y_range = Range1d(15,65,bounds=(15,65))

    # Line setup temperature
    def lines_temp(self, source):
        dataset = self.get_dataset(source)
        self.plot.line(x=dataset.date, y=dataset.supply, line_width=2, line_color="red", legend="Supply")
        self.plot.line(x=dataset.date, y=dataset.return, line_width=2, line_color="blue", legend="Return")

def update_plot():
    print(datetime.datetime.now().isoformat() + ": UPDATE PLOT")
    plot_temp.lines_temp(input_file_temp)

plot_temp = Plot_Temp(plot_temp_title)

update_plot()

tab1 = Panel(child=column(plot_temp.getLayout()),title=plot_temp_title)

tabs = Tabs(tabs=[tab1])
curdoc().add_root(tabs)
#curdoc().add_periodic_callback(update_plot, 20000)	# Update every 20 seconds
curdoc().title = tab_title
