import pygal
from flask import render_template
from pygal.style import DarkSolarizedStyle, LightSolarizedStyle, RedBlueStyle
from collections import namedtuple

GlucoseRange = namedtuple(
    'GlucoseRange', ['within100', 'within120', 'within200', 'within300', 'greater300'])

class PlotGluco(object):

    def _getDistribution(self, yaxis):
        within100 = sum([1 for x in yaxis if x < 100])
        within120 = sum([1 for x in yaxis if x >= 100 and x <= 120])
        within200 = sum([1 for x in yaxis if x > 120 and x <= 200])
        within300 = sum([1 for x in yaxis if x > 200 and x <= 300])
        greater300 = sum([1 for x in yaxis if x > 300])
        return GlucoseRange(within100, within120, within200, within300, greater300)


    def render_graph(self, plot_type, xaxis, yaxis, renderTofile=False):
        title = 'Glucose reading from {start} to {end}:  Total data = {total}'.format(
            start=xaxis[0], end=xaxis[-1], total=len(xaxis))
        if 'pie' in plot_type:
            return self._plot_pie(title, yaxis=yaxis, file=renderTofile)
        elif 'box' in plot_type:
            return self._plot_box(title, yaxis=yaxis, file=renderTofile)
        elif 'gauge' in plot_type:
            return self._plot_gauge(title, yaxis=yaxis, file=renderTofile)
        else:
            return self._plot_line(title, xaxis=xaxis, yaxis=yaxis, file=renderTofile)


    def _plot_pie(self, title='No title', yaxis=None, file=False):
        if not yaxis:
            return "No Data"

        total = len(yaxis)
        dist = self._getDistribution(yaxis)
        pie_chart = pygal.Pie()
        pie_chart.title = title
        pie_chart.style = RedBlueStyle
        pie_chart.disable_xml_declaration = True
        pie_chart.add('< 100', (dist.within100 * 100) / total)
        pie_chart.add('< 120', (dist.within120 * 100) / total)
        pie_chart.add('< 200', (dist.within200 * 100) / total)
        pie_chart.add('< 300', (dist.within300 * 100) / total)
        pie_chart.add('> 300', (dist.greater300 * 100) / total)
        if not file:
            return render_template('plot.html', title=pie_chart.title, line_chart=pie_chart)
        return pie_chart.render()


    def _plot_gauge(self, title='No title', yaxis=None, file=False):
        if not yaxis:
            return "No Data"

        dist = self._getDistribution(yaxis)
        gauge_chart = pygal.Gauge(human_readable=True)
        gauge_chart.title = title
        gauge_chart.style = DarkSolarizedStyle
        gauge_chart.disable_xml_declaration = True
        gauge_chart.height = 600
        gauge_chart.width = 1200
        gauge_chart.range = [0, len(yaxis)]
        gauge_chart.add('< 100', dist.within100)
        gauge_chart.add('< 120', dist.within120)
        gauge_chart.add('< 200', dist.within200)
        gauge_chart.add('< 300', dist.within300)
        gauge_chart.add('> 300', dist.greater300)
        if not file:
            return render_template('plot.html', title=gauge_chart.title, line_chart=gauge_chart)
        return gauge_chart.render()


    def _plot_box(self, title='No title', yaxis=None, file=False):
        if not yaxis:
            return "No Data"

        dist = self._getDistribution(yaxis)
        box_chart = pygal.Box()
        box_chart.title = title
        box_chart.style = LightSolarizedStyle
        box_chart.disable_xml_declaration = True
        box_chart.add('< 100', dist.within100)
        box_chart.add('< 120', dist.within120)
        box_chart.add('< 200', dist.within200)
        box_chart.add('< 300', dist.within300)
        box_chart.add('> 300', dist.greater300)
        if not file:
            return render_template('plot.html', title=box_chart.title, line_chart=box_chart)
        return box_chart.render()


    def _plot_line(self, title='No title', xaxis=None, yaxis=None, file=False):
        if not xaxis and not yaxis:
            return "No Data"

        line_chart = pygal.Line()
        line_chart.title = title
        line_chart.style = DarkSolarizedStyle
        line_chart.disable_xml_declaration = True
        line_chart.x_labels = [map(str, xaxis)]
        line_chart.add('mg/dl', yaxis)
        if not file:
            return render_template('plot.html', title=title, line_chart=line_chart)
        return line_chart.render()
