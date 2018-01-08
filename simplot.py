import random
from collections import deque

import plotly
import plotly.graph_objs as go


plotly.offline.init_notebook_mode(connected=True)


COLOR_DEFAULTS = ['#37505C', '#6D5747', '#55858B', '#94B0DA', '#000F08']


class Simplot(object):
    def __init__(self, df, name='Plot Title', font='Lato', font_size=18, colors=COLOR_DEFAULTS):

        # design
        self.name_font_data = dict(family=font, size=font_size)
        self.axes_font_data = {}
        self.colors = deque(colors)
        self.current_color = ''

        # base data
        self.name = name
        self.df = df
        self.x = df.index

        # used to declare any default arguments to axes dictionaries
        #self.base_axes_arg = dict(autorange=True, zeroline=False, autotick=True, scaleanchor="x")
        self.base_axes_arg = {}

        # axes
        self.x_data = {}
        self.y_data = {}
        self.y2_data = {}

        # staging attributes
        self.series_data = []
        self.plot_types = set()
        self.fig = None
        self.layout = {}

        # other
        self.stack = ''
        self.legend_orientation = ''

    def __repr__(self):
        return "Plot '{}'(len={}, series={}, stacked={}, X={}, Y={}, Y2={})".format(self.name,
                                                                                    len(self.x),
                                                                                    len(self.series_data),
                                                                                    bool(self.stack),
                                                                                    self.x_data.get('title'),
                                                                                    self.y_data.get('title'),
                                                                                    self.y2_data.get('title'))

    def __getitem__(self, key):
        """Access previously-plotted series by index or column-name"""
        if isinstance(key, int):
            return self.series_data[key]

        if isinstance(key, str):
            return [data for data in self.series_data if data['name'] == key][0]

    # Internal Methods - condense similarities for convenience and simplicity. Not intended to be interacted with.

    def __add_series(self, series):
        """Gatekeeper to plotting methods for providing interactivity purposes. Adding structured series to self.series_data
        to be used when plotting method is called."""

        style = series.type
        name = series.name if series.name else ''

        print(f"Plotting {name} as {style} using color {self.current_color}")

        self.plot_types.add(style)
        self.series_data.append(series)

    def __use_color(self, color):
        if not color:
            if self.colors:
                self.current_color = self.colors.popleft()
            else:
                r = lambda: random.randint(0, 255)
                self.current_color = '#%02X%02X%02X'.format((r(), r(), r()))
        return self.current_color

    def __pack_axes_data(self, title):
        """Constructs dictionary for plotting function to use within self.layout"""
        arg_dict = {'title': title, 'titlefont': self.axes_font_data}
        return dict(**arg_dict, **self.base_axes_arg)

    def __get_base_args(self, color, y_axis):
        """Parent method that runs base processes against common method args."""
        return self.__use_color(color), self.__discern_y(y_axis)

    @staticmethod
    def __conditional_y(arg_dict, y_axis):
        """Axes dicts require additional argument if a series is being plotted against a secondary Y"""
        if y_axis != 'y':
            arg_dict['yaxis'] = y_axis
        return arg_dict

    def __fill_layout_args(self):
        args = dict(title=self.name, titlefont=self.name_font_data,
                    xaxis=self.x_data, yaxis=self.y_data,
                    legend=dict(orientation=self.legend_orientation)
                    )

        if self.y2_data:
            args['yaxis2'] = self.y2_data

        if self.stack:
            args['barmode'] = 'stack'

        return args

    # Main Methods

    def draw_axes(self, x_title=None, y_title='Y Axis', y2_title=None, font='Lato', font_size=12):
        """Assigns titles and font data to axes. Also declares axes dictionaries for final plotting."""
        self.axes_font_data = dict(family=font, size=font_size)

        # Do not arbitrarily change order

        x_title = x_title or self.df.index.name or 'X Axis'
        self.x_data = self.__pack_axes_data(x_title)

        if y2_title:
            self.base_axes_arg['anchor'] = 'x'
            self.base_axes_arg['rangemode'] = 'tozero'
            self.y2_data = dict(self.__pack_axes_data(y2_title), **dict(overlaying='y', side='right'))

        self.y_data = self.__pack_axes_data(y_title)

    def bar(self, column, y_axis=1, color=None):
        color, y_axis = self.__get_base_args(color, y_axis)

        args = dict(x=self.x, y=list(self.df[column]), name=column, marker={'color': color})
        args = self.__conditional_y(args, y_axis)

        self.__add_series(go.Bar(args))

    def line(self, column, y_axis=1, color=None, line_width=.3, interpolation='spline'):
        color, y_axis = self.__get_base_args(color, y_axis)
        style_args = dict(width=line_width, shape=interpolation, color=color)

        args = dict(x=self.x, y=list(self.df[column]), name=column, line=style_args)
        args = self.__conditional_y(args, y_axis)

        self.__add_series(go.Scatter(args))

    def scatter(self, column, y_axis=1, color=None, mode='markers', size=10):
        color, y_axis = self.__get_base_args(color, y_axis)
        style_args = dict(size=size, color=color)

        args = dict(x=self.x, y=list(self.df[column]), name=column, mode=mode, marker=style_args)
        args = self.__conditional_y(args, y_axis)

        self.__add_series(go.Scatter(args))

    def windrose(self, column, color=None):
        color, _ = self.__get_base_args(color, 1)
        args = dict(t=self.df.index, r=list(self.df[column]), marker={'color': color})

        self.__add_series(go.Area(args))

    def heatmap(self, list_of_columns, cmap=None):
        """Plots dataframe values against index and columns in heatmap. Can be run without axes being drawn."""

        if not cmap: cmap = 'BuGn'

        collapsed_values = [list(self.df[col]) for col in list_of_columns]

        args = dict(z=collapsed_values, x=self.x, y=list_of_columns, colorscale=cmap)

        self.__add_series(go.Heatmap(args))

    def plot(self, stack=False, legend_orientation='h'):
        """Main function that produces visualization of plotted series on provided axes. Requires a plotting 
        method to have been run."""

        self.stack = stack
        self.legend_orientation = legend_orientation

        self.layout = go.Layout(**self.__fill_layout_args())
        self.fig = go.Figure(data=self.series_data, layout=self.layout)

        plotly.offline.iplot(self.fig)

    # Convenience Methods

    @staticmethod
    def __discern_y(y):
        """Allows user to pass in either integer or string of y_axis to plot upon"""
        return 'y2' if y in [2, '2', 'y2', 'secondary', 'right'] else 'y'
