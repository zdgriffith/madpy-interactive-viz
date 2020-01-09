
import pandas as pd
from bokeh.models import ColumnDataSource
from bokeh.models.callbacks import CustomJS
from bokeh.models.widgets import Select, Slider
from bokeh.models.layouts import Tabs, Panel
from bokeh.layouts import row, widgetbox
from bokeh.plotting import curdoc, figure


df = {
    'nba': pd.read_csv('../Data/nba_players_2019.csv'),
    'wnba': pd.read_csv('../Data/wnba_players_2019.csv')
}
leagues = list(df)
alpha_slider = Slider(title='Circle Opacity', start=0, end=1, value=0.5, step=0.01)

figs = {}
sources = {}
circle_callbacks = {}
for league in leagues:
    sources[league] = ColumnDataSource({
        'x': df[league]['MP'], 'y': df[league]['PTS']
    })
    figs[league] = figure(title=f'2019 {league.upper()} Players')
    circle = figs[league].circle(source=sources[league], x='x', y='y', alpha=0.5)
    
    alpha_slider.js_on_change(
        'value',
        CustomJS(
            args=dict(circle=circle),
            code="circle.glyph.fill_alpha = cb_obj.value;" # models passed as args are magically available
        )
    )
    
figs['nba'].x_range = figs['wnba'].x_range
figs['nba'].y_range = figs['wnba'].y_range

values = list(df['nba'].columns)
x_select = Select(title='X-Axis', options=values, value='MP')
y_select = Select(title='Y-Axis', options=values, value='PTS')

# Event handler function 
def update_axis(attr, old, new):
    for league in leagues:
        sources[league].data.update(x=df[league][x_select.value], y=df[league][y_select.value])
        figs[league].xaxis.axis_label = x_select.value
        figs[league].yaxis.axis_label = y_select.value
        
# Add event handler for change of value
x_select.on_change("value", update_axis)
y_select.on_change("value", update_axis)
widget_box = widgetbox([x_select, y_select, alpha_slider])

tabs = []
for league in leagues:
    tabs.append(Panel(child=row([widget_box, figs[league]], sizing_mode='stretch_height'), title=league.upper()))
tab_layout = Tabs(tabs=tabs)
curdoc().add_root(tab_layout)

