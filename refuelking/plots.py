from bokeh.plotting import figure
from bokeh.models import DatetimeTickFormatter


def get_price_plot(data):
    """
    Generates a price plot for the fuel types e10, e5 and diesel.

    * Parameters:

        :data:
            ``dict``;
            should contain a list of dates (key: ``dates``) and a list of
            price values (keys: ``diesel``, ``e10`` and ``e5``) for each fuel
            type.


    * Result:

        ``bokeh.figure``;
        returns the finished bokeh figure which thens needs to be embedded.
    """
    # Define the basic figure...
    p = figure(title="Preisentwicklung",
               x_axis_label='Datum', y_axis_label='Preis in €',
               toolbar_location=None, width=500, height=500,
               title_text_font='Lato', title_text_font_size='1.5em',
               title_text_font_style='bold')
    # ... and axis format.
    p.xaxis.formatter = DatetimeTickFormatter(formats=dict(
            hours=["%d %b"],
            days=["%d %b"],
            months=["%d %b"],
            years=["%d %b"],
        ))

    # Add a line renderer with legend and line thickness
    p.line(data['dates'], data['diesel'], legend='DIESEL', line_width=2,
           line_color='red')
    p.line(data['dates'], data['e10'], legend='E10', line_width=2,
           line_color='green')
    p.line(data['dates'], data['e5'], legend='E5', line_width=2,
           line_color='orange')
    return p